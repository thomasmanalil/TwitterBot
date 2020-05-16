
from unittest.mock import Mock
import unittest
import reply
from unittest.mock import patch
from unittest.mock import create_autospec
import array
import tweepy
from tweepy import User
from twitter import Twitter
import os

PARENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
class ReplyTest(unittest.TestCase):

    
    def getAllTweets(self,since_id):        
        tweets = []
        for id in range(10):
            tweet = tweepy.Status()
            tweet.id = id       
            tweet.user = User()
            tweet.user.name = "User-"+str(id)  
            tweet.in_reply_to_status_id=None            
            tweets.append(tweet)               
        return tweets

    def getOneComment(self,since_id):
        print("from mock getTweets")
        tweets = []

        tweet = tweepy.Status()
        tweet.id = since_id       
        tweet.user = User()
        tweet.user.name = "User-"+str(tweet.id)  
        tweet.in_reply_to_status_id=None      

        tweets.append(tweet)               

        tweet = tweepy.Status()
        tweet.id = since_id+1       
        tweet.user = User()
        tweet.user.name = "User-"+str(tweet.id)  
        tweet.in_reply_to_status_id=since_id-1      

        tweets.append(tweet)

        return tweets

    def get_all_comments(self,since_id):
        print("from mock getTweets")
        tweets = []

        tweet = tweepy.Status()
        tweet.id = since_id       
        tweet.user = User()
        tweet.user.name = "User-"+str(tweet.id)  
        tweet.in_reply_to_status_id=since_id-1      

        tweets.append(tweet)               

        tweet = tweepy.Status()
        tweet.id = since_id+1       
        tweet.user = User()
        tweet.user.name = "User-"+str(tweet.id)  
        tweet.in_reply_to_status_id=since_id-2    

        tweets.append(tweet)

        return tweets

    def sendTweet(self, stat, replyId):
        print("replying "+str(stat)+" to tweet "+str(replyId))    
        
    
    
    @patch.object(Twitter, 'getMentions')
    @patch.object(Twitter, 'tweetReply')
    # patched parameters are from bottom to up order
    def test_reply_for_all_tweets(self, mock_tweetReply, mock_getMentions):   
        mock_getMentions.side_effect=self.getAllTweets
        mock_tweetReply.side_effect=self.sendTweet    
        reply.replyToMentions(1)
        self.assertEqual(10,mock_tweetReply.call_count)
    
    
    @patch.object(Twitter, 'getMentions')
    @patch.object(Twitter, 'tweetReply')
    # patched parameters are from bottom to up order
    def test_no_reply_for_one_comment(self, mock_tweetReply, mock_getMentions):        
        
        mock_getMentions.side_effect=self.getOneComment
        mock_tweetReply.side_effect=self.sendTweet    
        reply.replyToMentions(1)
        # shouldn't reply to comment - call count should be totaltweet count -1
        self.assertEqual(1,mock_tweetReply.call_count)
    
    @patch.object(Twitter, 'getMentions')
    @patch.object(Twitter, 'tweetReply')
    # patched parameters are from bottom to up order
    def test_no_reply_for_all_coments(self, mock_tweetReply, mock_getMentions):        
        
        mock_getMentions.side_effect=self.get_all_comments
        mock_tweetReply.side_effect=self.sendTweet    
        reply.replyToMentions(1)
        # all comments - so no call should be made
        self.assertEqual(0,mock_tweetReply.call_count)

if __name__ == "__main__":
    unittest.main()