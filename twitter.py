import tweepy
from config import CONSUMER_KEY
from config import CONSUMER_SECRET
from config import ACCESS_TOKEN
from config import ACCESS_TOKEN_SECRET

def createAPI():      
    #setting twitter tokens
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #creating api
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    return api


class Twitter(object):
    
    def __init__(self):
        self.api = createAPI()   

    def getMentions(self, since_id):
        return tweepy.Cursor(self.api.mentions_timeline, since_id=since_id).items()
    
    def tweetReply(self, status, in_reply_to_status_id):
        return self.api.update_status(status=status, in_reply_to_status_id=in_reply_to_status_id, auto_populate_reply_metadata = True)

    def verifyLogin(self):
        try:
            #verifying credentials
            self.api.verify_credentials()           
        except Exception as ex:
            #logger.log("Failed to verify credentials. Check log.")
            print("Failed to verify.")
            raise ex
        print("Tokens are valid. Credentials verified.")

if __name__ == "__main__":
    tw = Twitter()
    tw.verifyLogin()