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

class DataForwarding(_message.Message):
    __slots__ = ("image", "faces", "id", "prime")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    FACES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRIME_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    faces: _containers.RepeatedCompositeFieldContainer[_face_pb2.Face]
    id: int
    prime: str
    def __init__(self, image: _Optional[bytes] = ..., faces: _Optional[_Iterable[_Union[_face_pb2.Face, _Mapping]]] = ..., id: _Optional[int] = ..., prime: _Optional[str] = ...) -> None: ...

class DataForwardingStatus(_message.Message):
    __slots__ = ("id", "prime", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    prime: str
    status: bool
    def __init__(self, id: _Optional[int] = ..., prime: _Optional[str] = ..., status: bool = ...) -> None: ...
