import json
import os.path
import tweepy
import logging

def verifyLogin():
    logger = logging.getLogger()
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "config/config.json")
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

    try:
        #verifying credentials
        api.verify_credentials()
    except Exception as ex:
        logger.log("Error Creating API. Check log.")
        raise ex
    logger.log("API Created.")
    return api







