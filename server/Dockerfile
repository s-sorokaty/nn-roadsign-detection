FROM daisukekobayashi/darknet:gpu-cv-cc86

RUN apt update

RUN apt install python3 python3-pip -y
RUN pip install poetry opencv-python

RUN apt install ffmpeg -y
COPY pyproject.toml poetry.lock /workspace/
RUN cd /workspace/ && poetry install
RUN apt install libavcodec-dev libavformat-dev libswscale-dev \
libgstreamer-plugins-base1.0-dev \
libgstreamer1.0-dev libgtk-3-dev \
libpng-dev libjpeg-dev libopenexr-dev libtiff-dev libwebp-dev \
libopencv-dev x264 libx264-dev libssl-dev -y
WORKDIR /workspace