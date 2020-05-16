import json
import os.path
import tweepy
import logging

PARENT_FOLDER = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

path = os.path.join(PARENT_FOLDER, "config/config.json")
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
try:
    if(os.path.exists(path)):
        with open(path) as configFile:
            #reading tokens from config file
            configData=json.load(configFile)
            CONSUMER_KEY = str(configData['CONSUMER_KEY'])
            CONSUMER_SECRET = str(configData['CONSUMER_SECRET'])
            ACCESS_TOKEN = str(configData['ACCESS_TOKEN'])
            ACCESS_TOKEN_SECRET = str(configData['ACCESS_TOKEN_SECRET'])
except Exception as ex:
    LOGGER.info(ex)








