import logging
import io
import onnxruntime as ort

ort.set_default_logger_severity(3)

from PIL import Image
import numpy as np

# Model
from src.models import Embedding

from src.proto.data_processing_srv_pb2_grpc import EmbeddingService
from src.proto import data_processing_srv_pb2 as dpb

from annoy import AnnoyIndex

logger = logging.getLogger('rpc')

class DataProcessingInferenceService(EmbeddingService):

    def __init__(self, model_file:str) -> None:
        super().__init__()
        self.model = Embedding(model_file)
        self.registery = None

        self.ids = []
        self.embeds = []
        self.index = None


    async def Register(self, request: dpb.RegisterFaceRequest,context)->dpb.RegisterFaceResponse:
        """
        This route is responsible to get embedding and register that embedding
        """
        logger.info('Register method is called')
        image = request.image
        image = Image.open(io.BytesIO(image))
        image = np.array(image)

        keypoints = []
        for face in request.faces:
            points = []
            for pt in face.keypoints:
                points.append([pt.x, pt.y])
            keypoints.append(points)
        keypoints = np.array(keypoints)

        if len(keypoints) > 0:
            embeds,_ = self.model.get(image, keypoints)
            self.embeds += embeds.tolist()
        

            # Create new tree
            n_index = AnnoyIndex(self.model.embed_dim,'dot')

            for i, em in enumerate(self.embeds):
                n_index.add_item(i, em)

            n_index.build(10)
            self.index = n_index
        return dpb.RegisterFaceResponse()


    async def GetEmbedding(self, request: dpb.GetEmbeddingRequest,context)->dpb.GetEmbeddingResponse:
        """
        This route is responsible to get embedding and search the registery
        """
        logger.info('Search method is called')

        