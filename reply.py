import tweepy
import logging
from config import createAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def replyToMentions(api, sinceId):
    new_sinceId = sinceId
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=sinceId).items():
        new_sinceId = max(tweet.id,new_sinceId)
        if tweet.in_reply_to_status_id is not None:
            continue        
        logger.info(f"Replying to {tweet.user.name}")
        api.update_status(status="Hello!",in_reply_to_status_id=tweet.id,auto_populate_reply_metadata=True)

    return new_sinceId


def main():
    api = createAPI()
    sinceId = 1
    while True:
        sinceId = replyToMentions(api, sinceId)
        logger.info(f"New Since Id:{sinceId}")
        time.sleep(60)


if __name__ == "__main__":
    main()


#api  = createAPI()

#for tweet in tweepy.Cursor(api.home_timeline).items(10):
 #   print(f"{tweet.user.name} said {tweet.text}")




