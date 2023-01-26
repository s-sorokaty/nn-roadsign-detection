run_notebook:
	docker run --gpus all -p 8888:8888 -v ${PWD}:/home/jovyan/work -v /media/s-sorokaty/DCD24506D244E5FC:/home/jovyan/data  -e GRANT_SUDO=yes -e JUPYTER_ENABLE_LAB=yes --user root cschranz/gpu-jupyter:v1.4_cuda-11.6_ubuntu-20.04_python-only

start:
	poetry run python main.py
