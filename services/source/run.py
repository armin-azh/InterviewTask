import os
import sys
from pathlib import Path

# Add src to python system path
root_dir = Path(os.path.dirname(__file__)).absolute()
sys.path.append(str(root_dir))
sys.path.append(str(root_dir.joinpath('src/proto')))

import asyncio
from argparse import ArgumentParser, Namespace

import grpc

import logging

from src.utils import get_env
from src.rpc import DetectionInferenceService
from src.proto.detection_srv_pb2_grpc import add_DetectionServiceServicer_to_server
from src.logger import setup_logging

setup_logging()

logger = logging.getLogger('runner')

async def main(args: Namespace)->None:

    host = get_env('HOST', '0.0.0.0')
    port = get_env('PORT', 50052)

    detector_weights = './models/detector.onnx'
    landmark_weights = './models/landmarks.onnx'
    mean_calibration = './models/means.pkl'

    server = grpc.aio.server()

    add_DetectionServiceServicer_to_server(DetectionInferenceService(model_file=detector_weights, landmark_file=landmark_weights, mk_file=mean_calibration), server)

    address = f"{host}:{port}"

    server.add_insecure_port(address)
    
    logger.info(f"[📡] Starting server on {address}")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    parser = ArgumentParser()
    asyncio.run(main(parser.parse_args()))