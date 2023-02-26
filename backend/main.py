import cv2
import shutil
from darknet import darknet_video
from fastapi import FastAPI, UploadFile, responses
import uvicorn
import numpy as np

app = FastAPI()

@app.post("/image_detection")
async def root(image: UploadFile):
    with open("raw_data/test.jpg", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    img = cv2.imread("raw_data/test.jpg")
    row_shape = img.shape
    new_img = darknet_video.detect_on_frame(img)
    print(new_img[1])
    cv2.imwrite('prediction/test.jpg', 
                #new_img[0]
                cv2.resize(new_img[0], (row_shape[1], row_shape[0]))
            )
    return responses.FileResponse('prediction/test.jpg')

if __name__=="__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=4557, reload=True, workers=3)



#
#print('here', type(img))
##darknet_video.detect_on_video()

