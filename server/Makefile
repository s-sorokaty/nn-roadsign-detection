start:
	poetry run python main.py

build_container:
	docker build . --tag darknet_server

server_in_docker:
	docker run --runtime=nvidia --rm -v ${PWD}:/workspace -v ${PWD}/../darknet:/workspace/darknet -p 8000:8000 darknet_server poetry run python main.py
predict_image_in_docker:
	docker run --runtime=nvidia --rm -v ${PWD}:/workspace -v ${PWD}/darknet/data:/workspace/data -w /workspace darknet darknet detector test obj.data yolov7-darknet.cfg yolov7-darknet_best.weights test5.jpg -thresh .2
predict_video_in_docker:
	docker run --runtime=nvidia --rm -v ${PWD}:/workspace -v ${PWD}/darknet/data:/workspace/data -w /workspace darknet darknet detector demo obj.data yolov7-darknet.cfg yolov7-darknet_best.weights test.mp4 -i 0 -dont_show -out_filename prediction/res.mp4