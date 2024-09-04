import os
import sys
from pathlib import Path

# Add src to python system path
root_dir = Path(os.path.dirname(__file__)).absolute()
sys.path.append(str(root_dir))
sys.path.append(str(root_dir.joinpath('src/proto')))

import logging

from argparse import Namespace, ArgumentParser

from PIL import Image
import io

import grpc

from src.utils import get_env
from src.proto.enrollment_pb2 import Person
from src.proto.detection_srv_pb2_grpc import DetectionServiceStub
from src.proto.detection_srv_pb2 import DetectSingleImageRequest, Config
from src.rpc.detection import DetectionRPC

from confluent_kafka import Consumer, KafkaError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enrollment")

def main(args:Namespace)->None:
    
    # TOOD: Default value will be removed
    media_root = Path(get_env('MEDIA_ROOT', '/home/ixion/Projects/InterviewTask/services/app/media'))
    det_rpc_host = get_env('DET_RPC_HOST', '0.0.0.0:50052')

    conf = {
    'bootstrap.servers': 'localhost:9093',
    'group.id': 'enrollment-group',
    'auto.offset.reset': 'earliest'
    }

    det_rpc = DetectionRPC(det_rpc_host)

    consumer = Consumer(conf)

    consumer.subscribe(['cmp.enrollment.image'])

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logger.info('Reached end of partition')
            else:
                logger.error('Error: {}'.format(msg.error()))

        # Read message from kafka
        person = Person()
        person.ParseFromString(msg.value())

        image_path = media_root.joinpath(person.path)
        
        # Read images
        with Image.open(image_path) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)

            img_bytes = img_byte_arr.getvalue()

        # Detect
        response = det_rpc.request(img_bytes)

        logger.info(response)

        # Get embeddings

        # Pull to vector db

    consumer.close()


if __name__ == '__main__':
    parser = ArgumentParser()

    main(args=parser.parse_args())