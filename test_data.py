import unittest
import sys
import os
import data

class DataTest(unittest.TestCase): 

    def __init__(self, *args, **kwargs):
        super(DataTest, self).__init__(*args, **kwargs)
        self.file = data.DATA_FILE

    def tearDown(self):
        if(os.path.exists(self.file)):
            os.remove(self.file)


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
            emptyFile=open(self.file,"w")
            emptyFile.close()
            self.assertEqual(1,data.getSinceId())            
        except Exception as e:
            raise e
        finally:
            emptyFile.close()
                    
    def test_getSinceId_readFromFile(self):
        data.setSinceId(100)
        self.assertEqual(100, data.getSinceId())
        

if __name__ == "__main__":
    unittest.main()
    
