import json
import os.path
import tweepy
import logging

PARENT_FOLDER = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

def createAPI():
    
    path = os.path.join(PARENT_FOLDER, "config/config.json")
    with open(path) as configFile:
        #reading tokens from config file
        configData=json.load(configFile)
        CONSUMER_KEY = str(configData['CONSUMER_KEY'])
        CONSUMER_SECRET = str(configData['CONSUMER_SECRET'])
        ACCESS_TOKEN = str(configData['ACCESS_TOKEN'])
        ACCESS_TOKEN_SECRET = str(configData['ACCESS_TOKEN_SECRET'])
    #setting twitter tokens
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    #creating api
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    return api

#use this to test login credentials. 
def verifyLogin():
    logger = logging.getLogger()
    api = createAPI()
    try:
        #verifying credentials
        api.verify_credentials()
    except Exception as ex:
        logger.log("Failed to verify credentials. Check log.")
        raise ex
    logger.log("Tokens are valid. Credentials verified.")





