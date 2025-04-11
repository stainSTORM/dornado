FROM python:3.11-slim-buster

RUN pip install numpy requests git+https://github.com/dorna-robotics/dorna2-python.git

RUN pip install "arkitekt-next[all]>=0.8.82"

RUN mkdir /app
WORKDIR /app
COPY .arkitekt_next /app/.arkitekt_next
COPY app.py /app/app.py
