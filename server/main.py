import cv2, os
from starlette.responses import FileResponse
from darknet import darknet_video
from fastapi import FastAPI, UploadFile, responses, Request
import uvicorn
import logging
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse

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
logger = logging.getLogger("pc")
ROOT = os.path.dirname(__file__)

allow_origin = ["*"]
app.add_middleware(
    CORSMiddleware, allow_origins=allow_origin, allow_headers=["*"], allow_methods=["*"]
)

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

@app.get("/list/image_detection/")
async def root():
    return [image.split('.')[0] for image in os.listdir(f'{PREDICTION_DATA_PATH}/') if image.split('.')[1] =='jpg' or image.split('.')[1] =='jpeg' or image.split('.')[1] == 'png']

@app.delete("/image_detection/{filename}")
async def root(filename:str):
    return os.remove(f'{PREDICTION_DATA_PATH}/{filename}.jpg')
                     
@app.post("/video_detection/{filename}")
async def root(video_file: UploadFile,filename: str):
    with open(f"{ROW_DATA_PATH}/{filename}.mp4", "wb") as buffer:
            contents = await video_file.read()
            buffer.write(contents)
    darknet_video.video_prediction(f"{ROW_DATA_PATH}/{filename}.mp4", f'{PREDICTION_DATA_PATH}/{filename}.webm')
    return 'OK'

@app.get("/video_detection/{filename}")
def get_video(filename: str):
    return FileResponse(f'{PREDICTION_DATA_PATH}/{filename}.webm', media_type='application/octet-stream',filename=f'{filename}.webm')

@app.get("/video_stream/{filename}")
def get_video(filename: str):
    def iterfile(): 
        with open(f"{PREDICTION_DATA_PATH}/{filename}.webm", mode="rb") as file_like: 
            yield from file_like 
    return responses.StreamingResponse(iterfile(), media_type="video/webm")

@app.get("/list/video_detection/")
async def root():
    return [image.split('.')[0] for image in os.listdir(f'{PREDICTION_DATA_PATH}/') if image.split('.')[1] =='webm']

@app.delete("/video_detection/{filename}")
def get_video(filename: str):
    os.remove(f'{PREDICTION_DATA_PATH}/{filename}.webm')
    return 'OK'

@app.get("/readtime_prediction", response_class = responses.RedirectResponse, status_code=302)
def root():
    return 'http://localhost:8080/'

if __name__=="__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, workers=2)

