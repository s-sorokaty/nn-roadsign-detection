run_notebook:
	docker run --gpus all -p 8888:8888 -v ${PWD}:/home/jovyan/work -v /media/s-sorokaty/DCD24506D244E5FC:/home/jovyan/data  -e GRANT_SUDO=yes -e JUPYTER_ENABLE_LAB=yes --user root cschranz/gpu-jupyter:v1.4_cuda-11.6_ubuntu-20.04_python-only

start:
	poetry run python main.py
train:
	./darknet detector train /mnt/HDD/archive/rtsd-frames/obj.data /mnt/HDD/archive/rtsd-frames/yolov4-custom.cfg /mnt/HDD/archive/rtsd-frames/yolov4.conv.137 -map -show_imgs

train_v7:
	./darknet detector train /mnt/HDD/archive/rtsd-frames/obj.data /mnt/HDD/archive/rtsd-frames/yolov7-darknet.cfg -map #/mnt/HDD/archive/rtsd-frames/backup/yolov7-darknet_last.weights 

detect:
	./darknet detector demo /mnt/HDD/archive/rtsd-frames/obj.data /mnt/HDD/archive/rtsd-frames/yolov7-darknet.cfg /mnt/HDD/archive/rtsd-frames/backup/yolov7-darknet_best.weights test.mp4

test:
	./darknet detector test /mnt/HDD/archive/rtsd-frames/obj.data /mnt/HDD/archive/rtsd-frames/yolov7-darknet.cfg /mnt/HDD/archive/rtsd-frames/backup/yolov7-darknet_best.weights test.jpg
