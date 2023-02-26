import cv2, os
from starlette.responses import FileResponse
from darknet import darknet_video
from fastapi import FastAPI, UploadFile, responses
import uvicorn


ROW_DATA_PATH='raw_data'
PREDICTION_DATA_PATH='prediction'

app = FastAPI()

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

if __name__=="__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True, workers=3)

