import os
import sys
from pathlib import Path

# Add src to python system path
root_dir = Path(os.path.dirname(__file__)).absolute()
sys.path.append(str(root_dir))
sys.path.append(str(root_dir.joinpath('src/proto')))

import logging
import cv2

import io
from PIL import Image
import numpy as np

from argparse import Namespace, ArgumentParser

from src.utils import get_env
from src.proto.query_pb2 import Query
from src.proto.data_forwarding_pb2 import DataForwarding, DataForwardingStatus
from src.rpc.detection import DetectionRPC
from src.rpc.embedding import EmbeddingRPC
from src.tracker import FaceTracker

from confluent_kafka import Consumer, KafkaError, Producer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("query")


# Angles
PITCH = 30.
YAW = 30.
ROLL = 30.

def main(args:Namespace)->None:
    
    # TOOD: Default value will be removed
    media_root = Path(get_env('MEDIA_ROOT', '/home/ixion/Projects/InterviewTask/storage/media'))
    det_rpc_host = get_env('DET_RPC_HOST', '0.0.0.0:50052')
    embedding_rpc = get_env('EM_RPC_HOST', '0.0.0.0:50053')
    kafka_bootstrap = get_env('KAFKA_HOST', 'localhost:9093')

    conf = {
        'bootstrap.servers': kafka_bootstrap,
        'group.id': 'query-group',
        'auto.offset.reset': 'earliest'
    }

    det_rpc = DetectionRPC(det_rpc_host)
    em_rpc = EmbeddingRPC(embedding_rpc)

    consumer = Consumer(conf)

    consumer.subscribe(['cmp.session.videos'])

    conf = {
            'bootstrap.servers': kafka_bootstrap
        }
    producer = Producer(conf)

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logger.info('Reached end of partition')
            else:
                logger.error('Error: {}'.format(msg.error()))

            continue

        # Read message from kafka
        query = Query()
        query.ParseFromString(msg.value())

        video_path = media_root.joinpath(query.path)
        logger.info(video_path)
        src = cv2.VideoCapture(str(video_path))

        tracker = FaceTracker()
        while src.isOpened():
            ret,frame = src.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image)

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr,format='JPEG')

            img_bytes = img_byte_arr.getvalue()

            # Detect
            det_response = det_rpc.request(img_bytes)

            # Filter Faces
            faces = []
            for face in det_response.faces:
                if abs(face.pose.pitch)<=PITCH and abs(face.pose.yaw) <= YAW and abs(face.pose.roll) <= ROLL:
                    faces.append(face)

            # Get embeddings and pull to vector db
            if len(faces) > 0:
 
                em_response = em_rpc.request(img_bytes, faces)

                faces = em_response.faces

                embeds = []

                for face in faces:
                    embeds.append(list(face.embedding))

                ids, keep = tracker.update(np.array(embeds))

                forwarding = DataForwarding(image=img_bytes,id=query.id, prime=query.prime)
                for t,idx in enumerate(keep):
                    face = faces[idx]
                    face.track_id = int(ids[t].squeeze())
                    forwarding.faces.append(face)

                producer.produce("cmp.forwarding.results", forwarding.SerializeToString())

        # Finalize the request session
        status = DataForwardingStatus(id=query.id, prime=query.prime, status=True)
        producer.produce("cmp.forwarding.finalize", status.SerializeToString())

        producer.flush()
    consumer.close()


if __name__ == '__main__':
    parser = ArgumentParser()

    main(args=parser.parse_args())