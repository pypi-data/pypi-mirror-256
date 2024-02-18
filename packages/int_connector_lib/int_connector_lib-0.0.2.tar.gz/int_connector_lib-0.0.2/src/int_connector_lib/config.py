import typing

import pydantic
from google.protobuf.struct_pb2 import Struct

T = typing.TypeVar("T", bound=pydantic.BaseModel)


class PluginConfig(pydantic.BaseModel):
    """Base config model to handle grpc config structs."""

    @classmethod
    def from_struct(cls: type[T], struct: Struct) -> T:
        """Convert google protobuf.Struct to a config object."""
        data = dict(struct.items())
        return cls(**data)
