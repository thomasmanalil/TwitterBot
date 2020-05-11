import tweepy
import logging
from config import PARENT_FOLDER
from config import LOGGER
import time
import os.path
import data
from twitter import Twitter

#--> log to file
twitter = Twitter()

def replyToMentions(sinceId):
    new_sinceId = sinceId
    for tweet in twitter.getMentions(new_sinceId):
        new_sinceId = max(tweet.id,new_sinceId)
        if tweet.in_reply_to_status_id is not None:
            continue        
        LOGGER.info(f"Replying to {tweet.user.name}")
        
        # -->if retweet

        # --> if comment

        # --> if main tweet
        

        # -->call another API to get response

        try:
            #api.update_status(status="Hello!",in_reply_to_status_id=tweet.id,auto_populate_reply_metadata=True)
            #tweetReply(status="Hello!",in_reply_to_status_id=tweet.id,auto_populate_reply_metadata=True)
            twitter.tweetReply("Hello!",tweet.id)
            
        except tweepy.TweepError as twError:
            LOGGER.info(twError)        

    return new_sinceId


def main():
       
    sinceId = data.getSinceId() # -->get since id from file, if not 1

    while True:
        sinceId = replyToMentions(sinceId)
        data.setSinceId(sinceId) # save new since id in a file.
        LOGGER.info(f"New Since Id:{sinceId}")
        time.sleep(60)

if __name__ == "__main__":
    main()

