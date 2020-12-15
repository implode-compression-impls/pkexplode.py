import ctypes

from pklib_base import ReadFunT, WriteFunT, _initLibrary, getStreamCallbacks

__all__ = ("TDcmpStruct", "sizeConstants", "_decompressStream")


specializedSizeConstantsFields = (
	("internalStructSize", None),
	("IN_BUFF_SIZE", 2048),
	("CODES_SIZE", 256),
	("OFFSS_SIZE", 256),
	("OFFSS_SIZE1", 128),
	("CH_BITS_ASC_SIZE", 256),
	("LENS_SIZES", 16)
)


def _getFieldsForInternalStateStructure(sizeConstants):
	return (
		("offs0000", ctypes.c_ulong),
		("ctype", ctypes.c_ulong),
		("outputPos", ctypes.c_ulong),
		("dsize_bits", ctypes.c_ulong),
		("dsize_mask", ctypes.c_ulong),
		("bit_buff", ctypes.c_ulong),
		("extra_bits", ctypes.c_ulong),
		("in_pos", ctypes.c_uint),
		("in_bytes", ctypes.c_ulong),
		("param", ctypes.POINTER(None)),
		("read_buf", ReadFunT),
		("write_buf", WriteFunT),
		("out_buff", ctypes.c_ubyte * int(sizeConstants.common.OUT_BUFF_SIZE)),
		("in_buff", ctypes.c_ubyte * int(sizeConstants.IN_BUFF_SIZE)),
		("DistPosCodes", ctypes.c_ubyte * int(sizeConstants.CODES_SIZE)),
		("LengthCodes", ctypes.c_ubyte * int(sizeConstants.CODES_SIZE)),
		("offs2C34", ctypes.c_ubyte * int(sizeConstants.OFFSS_SIZE)),
		("offs2D34", ctypes.c_ubyte * int(sizeConstants.OFFSS_SIZE)),
		("offs2E34", ctypes.c_ubyte * int(sizeConstants.OFFSS_SIZE1)),
		("offs2EB4", ctypes.c_ubyte * int(sizeConstants.OFFSS_SIZE)),
		("ChBitsAsc", ctypes.c_ubyte * int(sizeConstants.CH_BITS_ASC_SIZE)),
		("DistBits", ctypes.c_ubyte * int(sizeConstants.common.DIST_SIZES)),
		("LenBits", ctypes.c_ubyte * int(sizeConstants.LENS_SIZES)),
		("ExLenBits", ctypes.c_ubyte * int(sizeConstants.LENS_SIZES)),
		("LenBase", ctypes.c_ushort * int(sizeConstants.LENS_SIZES)),
	)


TDcmpStruct = None


def explode(read_buf: ReadFunT, write_buf: WriteFunT, work_buf: ctypes.POINTER(TDcmpStruct), arbitraryData: ctypes.POINTER(None)) -> ctypes.c_uint:
	return lib.explode(read_buf, write_buf, work_buf, arbitraryData)


lib, TDcmpStruct, sizeConstants = _initLibrary(explode, "TDcmpStruct", specializedSizeConstantsFields, _getFieldsForInternalStateStructure)


def _decompressStream(inputStream, outputStream) -> int:
	s = TDcmpStruct()

	return explode(
		*getStreamCallbacks(inputStream, outputStream),
		work_buf=ctypes.byref(s),
		arbitraryData=None
	)
