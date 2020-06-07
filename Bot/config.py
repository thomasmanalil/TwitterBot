import json
import os.path
import tweepy
import logging

def read_json_file(file_path):
    with open(file_path) as configFile:
        json_data=json.load(configFile)
    return json_data


class Config ():
    PARENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
    logging.basicConfig(level=logging.INFO, filename='.\Log/twitterbot.log', filemode='a', format='%(asctime)s- %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    LOGGER = logging.getLogger()
    def __init__(self):
        path = os.path.join(Config.PARENT_FOLDER, os.pardir , "config/config.json")
        self.CONSUMER_KEY = ""
        self.CONSUMER_SECRET = ""
        self.ACCESS_TOKEN = ""
        self.ACCESS_TOKEN_SECRET = ""
        try:
            if(os.path.exists(path)):
                #reading tokens from config file
                configData=read_json_file(path)
                self.CONSUMER_KEY = str(configData['CONSUMER_KEY'])
                self.CONSUMER_SECRET = str(configData['CONSUMER_SECRET'])
                self.ACCESS_TOKEN = str(configData['ACCESS_TOKEN'])
                self.ACCESS_TOKEN_SECRET = str(configData['ACCESS_TOKEN_SECRET'])
        except Exception as ex:
            Config.LOGGER.info(ex)
            raise ex








