from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Query(_message.Message):
    __slots__ = ("id", "prime", "path")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRIME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    id: int
    prime: str
    path: str
    def __init__(self, id: _Optional[int] = ..., prime: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...
