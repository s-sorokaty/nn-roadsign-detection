import cv2, os
from starlette.responses import FileResponse
from darknet import darknet_video
from fastapi import FastAPI, UploadFile, responses, Request
import uvicorn
import logging
from fastapi.templating import Jinja2Templates

from av import VideoFrame
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay

from pydantic import BaseModel
from fastapi.responses import JSONResponse
class Offer_model(BaseModel):
    sdp:object
    type:object
    video_transform:object
ROW_DATA_PATH='raw_data'
PREDICTION_DATA_PATH='prediction'

try: os.mkdir(ROW_DATA_PATH)
except: pass
try: os.mkdir(PREDICTION_DATA_PATH)
except: pass

templates = Jinja2Templates(directory="templates")

app = FastAPI()

pcs = set()
relay = MediaRelay()
logger = logging.getLogger("pc")
ROOT = os.path.dirname(__file__)

class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform

    async def recv(self):
        frame = await self.track.recv()
        #cv2.imshow('test', frame.to_ndarray(format="bgr24"))
        print('here')
        return frame



@app.post("/image_detection/{filename}")
async def root(image_file: UploadFile, filename:str):
    with open(f"{ROW_DATA_PATH}/{filename}.jpg", "wb") as buffer:
            contents = await image_file.read()
            buffer.write(contents)

    img = cv2.imread(f"{ROW_DATA_PATH}/{filename}.jpg")
    row_shape = img.shape
    new_img = darknet_video.detect_on_frame(img)
    print(new_img[1])
    cv2.imwrite(f'{PREDICTION_DATA_PATH}/{filename}.jpg', 
                #new_img[0]
                cv2.resize(new_img[0], (row_shape[1], row_shape[0]))
            )
    return 'OK'

@app.get("/image_detection/{filename}")
async def root(filename: str):
    return responses.FileResponse(f'{PREDICTION_DATA_PATH}/{filename}.jpg')

@app.post("/video_detection/{filename}")
async def root(video_file: UploadFile,filename: str):
    with open(f"{ROW_DATA_PATH}/{filename}.mp4", "wb") as buffer:
            contents = await video_file.read()
            buffer.write(contents)
    darknet_video.detect_on_video(f'{PREDICTION_DATA_PATH}/{filename}.mp4')
    return 'OK'

@app.get("/video_detection/{filename}")
def root(filename: str):
    return FileResponse(f'{PREDICTION_DATA_PATH}/{filename}.mp4', media_type='application/octet-stream', filename='{filename}.mp4')


@app.post("/offer_cv")
async def offer(params: Offer_model):
    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)
    recorder = MediaBlackhole()

    relay = MediaRelay()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # open media source
    # audio, video = create_local_tracks()

    @pc.on("track")
    def on_track(track):

        # if track.kind == "audio":
        #     pc.addTrack(player.audio)
        #     recorder.addTrack(track)
        if track.kind == "video":
            pc.addTrack(
                VideoTransformTrack(relay.subscribe(track), transform=params.video_transform)
            )
            # if args.record_to:
            #     recorder.addTrack(relay.subscribe(track))

        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setRemoteDescription(offer)
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

@app.get('/')
async def offer(request: Request):
    return templates.TemplateResponse('index.html', {'request':request})
@app.get('/client.js')
async def offer(request: Request):
    return templates.TemplateResponse('client.js', {'request':request})

if __name__=="__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True)

