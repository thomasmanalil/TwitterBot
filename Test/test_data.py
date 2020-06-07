import unittest
import sys
import os
import Bot.data as data
from shutil import copy

class DataTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(DataTest, self).__init__(*args, **kwargs)
        self.file = data.DATA_FILE
        self.file_copy_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, "data/data_copy.txt")

    def setUp(self):
        if(os.path.exists(self.file)):
            copy(self.file, self.file_copy_path)

    def tearDown(self):
        if(os.path.exists(self.file_copy_path)):
            copy(self.file_copy_path, self.file)
            os.remove(self.file_copy_path)


    def test_resetSinceId_noFile(self):
        data.resetSinceId()
        self.assertFalse(os.path.exists(self.file))

    def test_resetSinceId_FilePresent(self):
        data.setSinceId(100)
        self.assertTrue(os.path.exists(self.file))
        data.resetSinceId()
        self.assertFalse(os.path.exists(self.file))

    def test_getSinceId_noFIle(self):
        data.resetSinceId()
        self.assertEqual(1,int(data.getSinceId()))

    def test_getSinceId_EmptyFile(self):
        try:
            emptyFile=open(self.file,"w+")
            emptyFile.close()
            self.assertEqual(1,data.getSinceId())
        except Exception as e:
            raise e
        finally:
            emptyFile.close()

    def test_getSinceId_readFromFile(self):
        data.setSinceId(100)
        self.assertEqual(100, data.getSinceId())

    def test_setSinceId_TruncatingAndAWrittingNewValue(self):
        data.setSinceId(100)
        self.assertEqual(100,data.getSinceId())
        data.setSinceId(1500)
        self.assertEqual(1500, data.getSinceId())


if __name__ == "__main__":
    unittest.main()

