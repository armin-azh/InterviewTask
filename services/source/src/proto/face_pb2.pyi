from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Angle(_message.Message):
    __slots__ = ("pitch", "yaw", "roll")
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    pitch: float
    yaw: float
    roll: float
    def __init__(self, pitch: _Optional[float] = ..., yaw: _Optional[float] = ..., roll: _Optional[float] = ...) -> None: ...

class BBox(_message.Message):
    __slots__ = ("x", "y", "w", "h")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    H_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    w: int
    h: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., w: _Optional[int] = ..., h: _Optional[int] = ...) -> None: ...

class Face(_message.Message):
    __slots__ = ("bbox", "hasHP", "timestamp", "pose")
    BBOX_FIELD_NUMBER: _ClassVar[int]
    HASHP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    bbox: BBox
    hasHP: bool
    timestamp: int
    pose: Angle
    def __init__(self, bbox: _Optional[_Union[BBox, _Mapping]] = ..., hasHP: bool = ..., timestamp: _Optional[int] = ..., pose: _Optional[_Union[Angle, _Mapping]] = ...) -> None: ...
