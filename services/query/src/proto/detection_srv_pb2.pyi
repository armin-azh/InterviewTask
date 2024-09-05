import face_pb2 as _face_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from face_pb2 import Angle as Angle
from face_pb2 import BBox as BBox
from face_pb2 import Keypoint as Keypoint
from face_pb2 import Face as Face

DESCRIPTOR: _descriptor.FileDescriptor

class Config(_message.Message):
    __slots__ = ("hasHP",)
    HASHP_FIELD_NUMBER: _ClassVar[int]
    hasHP: bool
    def __init__(self, hasHP: bool = ...) -> None: ...

class DetectSingleImageRequest(_message.Message):
    __slots__ = ("image", "config")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    config: Config
    def __init__(self, image: _Optional[bytes] = ..., config: _Optional[_Union[Config, _Mapping]] = ...) -> None: ...

class DetectSingleImageResponse(_message.Message):
    __slots__ = ("faces",)
    FACES_FIELD_NUMBER: _ClassVar[int]
    faces: _containers.RepeatedCompositeFieldContainer[_face_pb2.Face]
    def __init__(self, faces: _Optional[_Iterable[_Union[_face_pb2.Face, _Mapping]]] = ...) -> None: ...

class DetectImagesReqeust(_message.Message):
    __slots__ = ("images", "config")
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    images: _containers.RepeatedScalarFieldContainer[bytes]
    config: Config
    def __init__(self, images: _Optional[_Iterable[bytes]] = ..., config: _Optional[_Union[Config, _Mapping]] = ...) -> None: ...

class DetectImagesResponse(_message.Message):
    __slots__ = ("faces",)
    FACES_FIELD_NUMBER: _ClassVar[int]
    faces: _containers.RepeatedCompositeFieldContainer[_face_pb2.Face]
    def __init__(self, faces: _Optional[_Iterable[_Union[_face_pb2.Face, _Mapping]]] = ...) -> None: ...
