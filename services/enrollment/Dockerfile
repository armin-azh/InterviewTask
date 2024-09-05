FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    g++ \
    python3-numpy \
    gcc \
    make \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

CMD python3 run.py

