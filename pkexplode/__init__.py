import typing
from collections.abc import ByteString
from io import BytesIO, IOBase
from mmap import mmap
from warnings import warn
from zlib import crc32 as crc32_zlib

from pklib_base import PklibError

from .ctypes import _decompressStream

__all__ = ("decompressStreamToStream", "decompressStreamToBytes", "decompressBytesWholeToStream", "decompressBytesWholeToBytes", "decompressBytesChunkedToStream", "decompressBytesChunkedToBytes", "decompress")

def crc32(data: ByteString, value: int = 0) -> int:
	return (~crc32_zlib(data, value)) & 0xffffffff


def decompressStreamToStream(inputStream: IOBase, outputStream: IOBase) -> None:
	"""Used to do streaming decompression. The first arg is the stream to read from, the second ard is the stream to write to.
	May be a memory map. `chunkSize` is the hint"""

	errorCode = _decompressStream(inputStream, outputStream)

	if errorCode:
		raise Exception(PklibError(errorCode))


def decompressBytesChunkedToStream(compressed: ByteString, outputStream: IOBase) -> int:
	"""Compresses `compressed` into `outputStream`."""
	with BytesIO(compressed) as inputStream:
		return decompressStreamToStream(inputStream, outputStream)


def decompressBytesChunkedToBytes(compressed: ByteString) -> int:
	"""Compresses `compressed` into `bytes`."""
	with BytesIO() as outputStream:
		decompressBytesChunkedToStream(compressed, outputStream)
		return outputStream.getvalue()


def decompressStreamToBytes(inputStream: IOBase) -> int:
	"""Compresses `inputStream` into `outputStream`. Processes the whole data."""
	with BytesIO() as outputStream:
		decompressStreamToStream(inputStream, outputStream)
		return outputStream.getvalue()


_functionsUseCaseMapping = (
	decompressStreamToStream,
	decompressBytesChunkedToStream,
	decompressStreamToBytes,
	decompressBytesChunkedToBytes,
)


def decompress(compressed: typing.Union[ByteString, IOBase], outputStream: typing.Optional[IOBase] = None) -> int:
	"""A convenience function. It is better to use the more specialized ones since they have less overhead. It decompresses `compressed` into `outputStream` and returns a tuple `(left, output)`.
	`compressed` can be either a stream, or `bytes`-like stuff.
	If `outputStream` is None, then it returns `bytes`. If `outputStream` is a stream, it writes into it.
	`left` returned is the count of bytes in the array/stream that weren't processed."""

	isOutputBytes = outputStream is None
	isInputBytes = isinstance(compressed, (ByteString, mmap))
	selector = isOutputBytes << 1 | int(isInputBytes)
	func = _functionsUseCaseMapping[selector]
	argz = [compressed]
	if not isOutputBytes:
		argz.append(outputStream)
	_efficiencyDeprecationMessage(decompress, func)
	return func(*argz)
