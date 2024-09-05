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
            self.ids.append(face.person_id)
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

        if len(keypoints) > 0 and self.index is not None:
            embeds,_ = self.model.get(image, keypoints)
            
            for i, face in enumerate(request.faces):
                embed = embeds[i]
                
                n_ids, n_dists = self.index.get_nns_by_vector(embed, 1, search_k=-1, include_distances=True)
                n_ids = n_ids[0]
                _, max_dists = self.index.get_nns_by_vector(self.index.get_item_vector(n_ids), 1, search_k=-1,
                                                             include_distances=True)
                norm_dists = n_dists[0] / max_dists[0]
                person_id = self.ids[n_ids]

                face.embedding[:] = embed
                face.person_id = person_id
                face.similarity = norm_dists

        return dpb.GetEmbeddingResponse(faces=request.faces)
