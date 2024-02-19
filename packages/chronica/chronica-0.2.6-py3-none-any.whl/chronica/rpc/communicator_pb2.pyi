from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Schedule(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    STATIC: _ClassVar[Schedule]
    DYNAMIC: _ClassVar[Schedule]
    GUIDED: _ClassVar[Schedule]
STATIC: Schedule
DYNAMIC: Schedule
GUIDED: Schedule

class InitRequest(_message.Message):
    __slots__ = ["rank", "batch_size", "seed", "sizes", "groups", "partition", "kind"]
    RANK_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    SIZES_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    rank: int
    batch_size: int
    seed: int
    sizes: _containers.RepeatedScalarFieldContainer[int]
    groups: _containers.RepeatedScalarFieldContainer[int]
    partition: bool
    kind: Schedule
    def __init__(self, rank: _Optional[int] = ..., batch_size: _Optional[int] = ..., seed: _Optional[int] = ..., sizes: _Optional[_Iterable[int]] = ..., groups: _Optional[_Iterable[int]] = ..., partition: bool = ..., kind: _Optional[_Union[Schedule, str]] = ...) -> None: ...

class BcastRequest(_message.Message):
    __slots__ = ["epoch", "rank", "coefficient", "intercept"]
    EPOCH_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    INTERCEPT_FIELD_NUMBER: _ClassVar[int]
    epoch: int
    rank: int
    coefficient: float
    intercept: float
    def __init__(self, epoch: _Optional[int] = ..., rank: _Optional[int] = ..., coefficient: _Optional[float] = ..., intercept: _Optional[float] = ...) -> None: ...

class BcastResponse(_message.Message):
    __slots__ = ["indices"]
    INDICES_FIELD_NUMBER: _ClassVar[int]
    indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, indices: _Optional[_Iterable[int]] = ...) -> None: ...
