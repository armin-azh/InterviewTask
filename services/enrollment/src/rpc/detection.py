import grpc

# Proto
from src.proto.detection_srv_pb2 import DetectSingleImageRequest, DetectSingleImageResponse, Config
from src.proto.detection_srv_pb2_grpc import DetectionServiceStub

__all__ = [
    'DetectionRPC'
]

class DetectionRPC:
    def __init__(self, host: str) -> None:
        self.channel = grpc.insecure_channel(host)
        self.stub = DetectionServiceStub(channel=self.channel)


    def request(self,image)->DetectSingleImageResponse:
        request = DetectSingleImageRequest(
            image=image,
            config= Config(hasHP=False)
        )

        return self.stub.DetectSingleImage(request)
    
