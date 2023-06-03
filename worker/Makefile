build_container:
	docker build . --tag darknet_worker --no-cache

worker_in_docker:
	docker run --runtime=nvidia --rm -v ${PWD}:/workspace -v ${PWD}/../darknet:/workspace/darknet -p 8080:8080 darknet_server poetry run python worker.py

display:
	docker run -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix <image>