import math
from abc import ABCMeta, abstractmethod
from typing import Callable, Optional, TypeVar
from warnings import warn

from sqlalchemy.engine import Dialect
from sqlalchemy.types import LargeBinary, Numeric, TypeDecorator, TypeEngine

from atlantiscore.types.evm import (
    ByteEncoding as PythonByteEncoding,
    LiteralByteEncoding,
)

T = TypeVar("T", bound=PythonByteEncoding)
Y = TypeVar("Y", int, bytes)


class ByteEncoding(TypeDecorator, metaclass=ABCMeta):
    impl: TypeEngine = LargeBinary
    cache_ok: bool = True
    _decode: Callable[[T], Y] = bytes

    def __init__(self, byte_count: int, as_numeric: bool = True) -> None:
        if as_numeric:
            self.impl = Numeric(_calculate_required_precision(byte_count))
            self._decode = int
            warn(
                "as_numeric=True is deprecated and will be removed in a later version",
                DeprecationWarning,
                stacklevel=2,
            )
        else:
            super().__init__(byte_count)

    def process_bind_param(
        self,
        value: Optional[T | LiteralByteEncoding],
        dialect: Dialect,
    ) -> Y:
        if value is None:
            return value
        return self._decode(self._parse(value))

    def process_result_value(
        self,
        value: Optional[Y],
        dialect: Dialect,
    ) -> T:
        if value is None:
            return value
        return self._parse(self._decode(value))

    @staticmethod
    @abstractmethod
    def _parse(value: T | LiteralByteEncoding) -> T:
        """Parses value to T."""


def _calculate_required_precision(byte_count: int) -> int:
    bit_count = byte_count * 8
    return math.ceil(math.log10(2**bit_count))
