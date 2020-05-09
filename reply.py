import tweepy
import logging
from config import createAPI
from config import PARENT_FOLDER
from config import LOGGER
import time
import os.path
import data


#--> log to file



def replyToMentions(api, sinceId):
    new_sinceId = sinceId
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=sinceId).items():
        new_sinceId = max(tweet.id,new_sinceId)
        if tweet.in_reply_to_status_id is not None:
            continue        
        LOGGER.info(f"Replying to {tweet.user.name}")
        
        # -->if retweet

        # --> if comment

        # --> if main tweet
        

        # -->call another API to get response

        try:
            api.update_status(status="Hello!",in_reply_to_status_id=tweet.id,auto_populate_reply_metadata=True)
        except tweepy.TweepError as twError:
            LOGGER.info(twError)        

    return new_sinceId


def main():
    api = createAPI()
    
    sinceId = data.getSinceId() # -->get since id from file, if not 1
    while True:
        sinceId = replyToMentions(api, sinceId)
        data.setSinceId(sinceId) # save new since id in a file.
        LOGGER.info(f"New Since Id:{sinceId}")
        time.sleep(60)

if __name__ == "__main__":
    main()

