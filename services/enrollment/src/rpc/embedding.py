import grpc

# Proto
from src.proto.data_processing_srv_pb2 import RegisterFaceRequest, RegisterFaceResponse
from src.proto.data_processing_srv_pb2_grpc import EmbeddingServiceStub


__all__ = [
    'EmbeddingRPC'
]

class EmbeddingRPC:
    def __init__(self, host: str)->None:
        self.channel = grpc.insecure_channel(host)
        self.stub = EmbeddingServiceStub(channel=self.channel)

    def request(self,image, faces)-> RegisterFaceResponse:
        request = RegisterFaceRequest(
            image=image,
            faces=faces
        )

        return self.stub.Register(request)