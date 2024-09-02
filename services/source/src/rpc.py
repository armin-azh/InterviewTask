# This component is responsible to implement gRPC
import logging
from src.proto.detection_srv_pb2_grpc import DetectionService
from src.proto import detection_srv_pb2 as d_pb

logger = logging.getLogger('rpc')

__all__ = [
    'DetectionInferenceService'
]


class DetectionInferenceService(DetectionService):
    async def DetectSingleImage(self, request: d_pb.DetectSingleImageRequest, context)->d_pb.DetectSingleImageResponse:
        logger.info('detect single image is called')
        return d_pb.DetectSingleImageResponse()
    
    async def DetectImages(self, request: d_pb.DetectImagesReqeust, context)->d_pb.DetectImagesResponse:
        logger.info('detect image list is called')
        return d_pb.DetectImagesResponse()