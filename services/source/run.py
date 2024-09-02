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

from src.rpc import DetectionInferenceService
from src.proto.detection_srv_pb2_grpc import add_DetectionServiceServicer_to_server

logging.basicConfig(level=logging.INFO)

async def main(args: Namespace)->None:

    server = grpc.aio.server()

    add_DetectionServiceServicer_to_server(DetectionInferenceService(), server)

    address = f"[::]:{args.port}"

    server.add_insecure_port(address)

    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-gpu', help='Enable on gpu', action='store_true')
    parser.add_argument('-host', help='Host name', type=str, default='0.0.0.0')
    parser.add_argument('-port', help='Server Port number', type=int, default=50052)
    asyncio.run(main(parser.parse_args()))