import face_pb2 as _face_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from face_pb2 import Angle as Angle
from face_pb2 import BBox as BBox
from face_pb2 import Face as Face

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterFaceRequest(_message.Message):
    __slots__ = ("image", "faces")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    FACES_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    faces: _containers.RepeatedCompositeFieldContainer[_face_pb2.Face]
    def __init__(self, image: _Optional[bytes] = ..., faces: _Optional[_Iterable[_Union[_face_pb2.Face, _Mapping]]] = ...) -> None: ...

class RegisterFaceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetEmbeddingRequest(_message.Message):
    __slots__ = ("image", "faces")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    FACES_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    faces: _containers.RepeatedCompositeFieldContainer[_face_pb2.Face]
    def __init__(self, image: _Optional[bytes] = ..., faces: _Optional[_Iterable[_Union[_face_pb2.Face, _Mapping]]] = ...) -> None: ...

class GetEmbeddingResponse(_message.Message):
    __slots__ = ("faces",)
    FACES_FIELD_NUMBER: _ClassVar[int]
    faces: _containers.RepeatedCompositeFieldContainer[_face_pb2.Face]
    def __init__(self, faces: _Optional[_Iterable[_Union[_face_pb2.Face, _Mapping]]] = ...) -> None: ...
