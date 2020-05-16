import unittest
import json
import config
from config import Config
from unittest.mock import patch
import os
from shutil import copy

file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config/config.json")
file_copy_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config/config_copy.json")

# mock json data function
def return_json(path):
    return json.loads(
        '''
        {
        "CONSUMER_KEY":"CSK-1",
        "CONSUMER_SECRET" :"CS-1",
        "ACCESS_TOKEN":"AT-1",
        "ACCESS_TOKEN_SECRET":"ATS-1"
        }
        ''')
class TestConfig(unittest.TestCase):
    
    def setUp(self):        
        # make a copy of config.json 
        copy(file_path,file_copy_path)        

    def tearDown(self):
        # replace config.json with backu taken in setup  
        copy(file_copy_path,file_path)
        os.remove(file_copy_path)            

    ''' Positive test case'''
    @patch.object(config, 'read_json_file')
    def test_read_from_file(self, mock_json):
        # values to compare
        sample_json = return_json("") 
        # mock function to return json
        mock_json.side_effect = return_json
        conf_test =Config()

        self.assertEqual(sample_json['ACCESS_TOKEN'], conf_test.ACCESS_TOKEN)
        self.assertEqual(sample_json['ACCESS_TOKEN_SECRET'], conf_test.ACCESS_TOKEN_SECRET)
        self.assertEqual(sample_json['CONSUMER_KEY'], conf_test.CONSUMER_KEY)
        self.assertEqual(sample_json['CONSUMER_SECRET'], conf_test.CONSUMER_SECRET)        


    ''' Exception handling test case'''
    @patch.object(config, 'read_json_file')
    def test_file_exception(self, mock_json):
        # mock file not found error
        mock_json.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            conf_test =Config()

    ''' no file test case '''
    def test_no_file(self):
        # file removed
        os.remove(file_path)
        # function to be tested
        conf_test = Config()
        
        # values should be empty strings
        self.assertEqual("", conf_test.ACCESS_TOKEN)
        self.assertEqual("", conf_test.ACCESS_TOKEN_SECRET)
        self.assertEqual("", conf_test.CONSUMER_KEY)
        self.assertEqual("", conf_test.CONSUMER_SECRET)        
        


if __name__ == "__main__":
    unittest.main()

    
    