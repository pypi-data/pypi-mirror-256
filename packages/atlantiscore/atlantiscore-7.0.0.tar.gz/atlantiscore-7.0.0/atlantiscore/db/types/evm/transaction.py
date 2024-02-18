from atlantiscore.db.types.evm.base import ByteEncoding
from atlantiscore.types.evm import (
    EVMTransactionHash as PythonTransactionHash,
    LiteralByteEncoding,
)

BYTE_COUNT = 32


class EVMTransactionHash(ByteEncoding):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(BYTE_COUNT, *args, **kwargs)

    @staticmethod
    def _parse(
        value: PythonTransactionHash | LiteralByteEncoding,
    ) -> PythonTransactionHash:
        return PythonTransactionHash(value)
