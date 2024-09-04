# This component is responsible to implement gRPC
import logging
import io
from datetime import datetime

import onnxruntime

onnxruntime.set_default_logger_severity(3)

from PIL import Image
import numpy as np

from src.proto.detection_srv_pb2_grpc import DetectionService
from src.proto import detection_srv_pb2 as d_pb
from src.proto.face_pb2 import Face

# Models
from src.models import Detector, Landmark

logger = logging.getLogger('rpc')

__all__ = [
    'DetectionInferenceService'
]


class DetectionInferenceService(DetectionService):
    def __init__(self, model_file:str, landmark_file:str, mk_file:str) -> None:
        super().__init__()
        self.model = Detector(model_file)
        self.hpe = Landmark(landmark_file, mk_file)

    async def DetectSingleImage(self, request: d_pb.DetectSingleImageRequest, context)->d_pb.DetectSingleImageResponse:
        logger.info('detect single image is called')

        is_hpe = request.config.hasHP

        image = request.image
        image = Image.open(io.BytesIO(image))
        image = np.array(image)
        _,bbox,_ = self.model.detect(image)

        if is_hpe:
            poses, _ = self.hpe.get(image, bbox)
        else:
            poses = None     

        response = d_pb.DetectSingleImageResponse()
        current = datetime.now()

        for i, box in enumerate(bbox):
            face = Face()

            x1,y1,x2,y2 = box
            
            face.bbox.x = int(x1)
            face.bbox.y = int(y1)
            face.bbox.w = int(x2-x1)
            face.bbox.h = int(y2-y1)

            face.timestamp = int(current.timestamp() * 10e3)

            face.hasHP = True if is_hpe else False

            if is_hpe:
                pitch,yaw,roll = poses[i]
                face.pose.pitch = pitch
                face.pose.yaw = yaw
                face.pose.roll = roll
            

            response.faces.append(face)
            
        return response
    
    async def DetectImages(self, request: d_pb.DetectImagesReqeust, context)->d_pb.DetectImagesResponse:
        logger.info('detect image list is called')
        return d_pb.DetectImagesResponse()