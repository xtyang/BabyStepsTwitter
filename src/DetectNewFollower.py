'''
Created on May 2, 2013

@author: Chun-Ku
reference http://peter-hoffmann.com/2012/simple-twitter-streaming-api-access-with-python-and-oauth.html
'''
import json
import twitter
import tweepy
import oauth2
import sys

# user keys
consumer_key = "XCyXHzIUUJx5YuJ2fysNA"
consumer_secret = "wuxBc0s3W5SDoA3rthCdpyW44kxOOszQabP2MSlecw"
access_key = "89890379-rJ671utfeJIAJ6yEn28pQf8XqTzDCR3IFEKTUylg4"
access_secret = "zXIdEEsxx2LClb7rDJepE9vjRithggJkc19cHeJLmOo"

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


def main():
    # create twitter API object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
    sapi.filter(follow=['babystepsuw']) # this looks like track the tweet that contains babystepsuw



if __name__ == '__main__':
    main()
