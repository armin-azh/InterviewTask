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
    apt-get install -y sudo && \
    adduser --disabled-password --gecos '' vscode && \
    echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    usermod -aG sudo vscode && \
    rm -rf /var/lib/apt/lists/*

USER vscode
WORKDIR /home/vscode

RUN pip install --no-cache-dir --upgrade pip
