# This component is responsible to implement gRPC
from src.proto.detection_srv_pb2_grpc import DetectionService
from src.proto import detection_srv_pb2 as d_pb

__all__ = [
    'DetectionInferenceService'
]


class DetectionInferenceService(DetectionService):
    async def DetectSingleImage(self, request: d_pb.DetectSingleImageRequest, context)->d_pb.DetectSingleImageResponse:
        return d_pb.DetectSingleImageResponse()
    
    async def DetectImages(self, request: d_pb.DetectImagesReqeust, context)->d_pb.DetectImagesResponse:
        return d_pb.DetectImagesResponse()