import unittest
import sys
import os

import data

class DataTest(unittest.TestCase): 

    def test_resetSinceId_noFile(self):
        data.resetSinceId()
        self.assertFalse(os.path.exists(data.DATA_FILE))

    def test_resetSinceId_FilePresent(self):
        data.setSinceId(100)
        self.assertTrue(os.path.exists(data.DATA_FILE))
        data.resetSinceId()
        self.assertFalse(os.path.exists(data.DATA_FILE))

    def test_getSinceId_noFIle(self):
        data.resetSinceId()
        self.assertEqual(1,int(data.getSinceId()))
    
    def test_getSinceId_EmptyFile(self):
        try:
            emptyFile=open(data.DATA_FILE,"w")
            emptyFile.close()
            self.assertEqual(1,data.getSinceId())            
        except Exception as e:
            raise e
        finally:
            emptyFile.close()
            data.resetSinceId()
        
    def test_getSinceId_readFromFile(self):
        data.setSinceId(100)
        self.assertEqual(100, data.getSinceId())
        data.resetSinceId()
    

if __name__ == "__main__":
    unittest.main()
    
