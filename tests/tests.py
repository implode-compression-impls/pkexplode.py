#!/usr/bin/env python3
import os
import sys
import unittest
from pathlib import Path
import mmap
from secrets import token_bytes

from fileTestSuite.unittest import FileTestSuiteTestCaseMixin

thisDir = Path(__file__).resolve().absolute().parent
repoRootDir = thisDir.parent

sys.path.insert(0, str(repoRootDir))

from collections import OrderedDict
dict = OrderedDict

from pkexplode import decompress, decompressBytesChunkedToBytes, decompressStreamToBytes


class Tests(unittest.TestCase, FileTestSuiteTestCaseMixin):
	@property
	def fileTestSuiteDir(self) -> Path:
		return thisDir / "testDataset"

	def _testProcessorImpl(self, challFile: Path, respFile: Path, paramsDict=None) -> None:
		self._testChallengeResponsePair(respFile.read_bytes(), challFile.read_bytes())

	def _testPack(self, chall: bytes, resp: bytes):
		tpName = chall.__class__.__name__
		#with self.subTest("decompress " + tpName):
		#	self.assertEqual(resp, decompress(chall))
		with self.subTest("decompressBytesChunkedToBytes " + tpName):
			self.assertEqual(resp, decompressBytesChunkedToBytes(chall))
		#with self.subTest("decompressBytesChunkedToBytes " + tpName):
		#	self.assertEqual(resp, decompressBytesChunkedToBytes(chall))
		#with self.subTest("compressBytesWholeToBytes " + tpName):
		#	self.assertEqual(resp, compressBytesWholeToBytes(chall))

	def _testChallengeResponsePair(self, chall, resp):
		self._testPack(chall, resp)

		#with mmap.mmap(-1, len(chall), access=mmap.ACCESS_READ|mmap.ACCESS_WRITE) as mm:
		#	mm.write(chall)
		#	mm.seek(0)
		#	self._testPack(mm, resp)

if __name__ == '__main__':
	unittest.main()
