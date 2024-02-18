from atlantiscore.db.types.evm.base import ByteEncoding
from atlantiscore.types.evm import EVMAddress as PythonEVMAddress, LiteralByteEncoding

BYTE_COUNT = 20


class EVMAddress(ByteEncoding):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(BYTE_COUNT, *args, **kwargs)

    @staticmethod
    def _parse(value: PythonEVMAddress | LiteralByteEncoding) -> PythonEVMAddress:
        return PythonEVMAddress(value)
