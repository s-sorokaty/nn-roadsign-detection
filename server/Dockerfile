FROM daisukekobayashi/darknet:gpu-cv-cc86

RUN apt update

RUN apt install python3 python3-pip -y
RUN pip install poetry opencv-python

RUN apt install ffmpeg -y
COPY pyproject.toml poetry.lock /workspace/
RUN cd /workspace/ && poetry install

WORKDIR /workspace