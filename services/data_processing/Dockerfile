FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    ca-certificates \
    g++ \
    python3-numpy \
    gcc \
    make \
    git \
    python3-setuptools \
    python3-wheel \
    python3-packaging \
    python3-pip \
    python3-venv \
    libglib2.0-0 \
    libopencv-dev \
    python3-opencv \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt


CMD python3 run.py

