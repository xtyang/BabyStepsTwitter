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
account_name="Chun_Ku"
consumer_key = "XCyXHzIUUJx5YuJ2fysNA"
consumer_secret = "wuxBc0s3W5SDoA3rthCdpyW44kxOOszQabP2MSlecw"
access_key = "89890379-rJ671utfeJIAJ6yEn28pQf8XqTzDCR3IFEKTUylg4"
access_secret = "zXIdEEsxx2LClb7rDJepE9vjRithggJkc19cHeJLmOo"

class CustomStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        decoded_data = json.loads(data)
        print decoded_data
        print decoded_data["event"]
        print decoded_data["source"]["screen_name"]
        print decoded_data["target"]["screen_name"]
        
    def on_status(self, status):
        print "on status"
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
    #stream = tweepy.Stream(auth, CustomStreamListener())
    #stream.userstream()
    #api.send_direct_message(user="ChunKuLin", text="hello from tweepy") send direct message to your follower
    #data='{"source":{"name":"Lin Chun-Ku","screen_name":"Chun_Ku","contributors_enabled":false,"default_profile_image":true,"profile_background_color":"C0DEED","time_zone":"Pacific Time (US & Canada)","followers_count":1,"id":89890379,"favourites_count":0,"profile_image_url_https":"https:\/\/twimg0-a.akamaihd.net\/sticky\/default_profile_images\/default_profile_5_normal.png","profile_background_image_url_https":"https:\/\/twimg0-a.akamaihd.net\/images\/themes\/theme1\/bg.png","url":null,"profile_background_image_url":"http:\/\/a0.twimg.com\/images\/themes\/theme1\/bg.png","notifications":false,"profile_link_color":"0084B4","statuses_count":58,"lang":"en","location":null,"utc_offset":-28800,"geo_enabled":false,"id_str":"89890379","profile_use_background_image":true,"default_profile":true,"profile_text_color":"333333","friends_count":2,"protected":false,"description":"","follow_request_sent":false,"is_translator":false,"following":false,"profile_image_url":"http:\/\/a0.twimg.com\/sticky\/default_profile_images\/default_profile_5_normal.png","profile_sidebar_border_color":"C0DEED","listed_count":0,"verified":false,"profile_background_tile":false,"created_at":"Sat Nov 14 07:04:28 +0000 2009","profile_sidebar_fill_color":"DDEEF6"},"event":"follow","target":{"name":"Chun-Ku Lin","screen_name":"ChunKuLin","contributors_enabled":false,"default_profile_image":true,"profile_background_color":"C0DEED","time_zone":null,"followers_count":1,"id":1398065154,"favourites_count":0,"profile_image_url_https":"https:\/\/twimg0-a.akamaihd.net\/sticky\/default_profile_images\/default_profile_3_normal.png","profile_background_image_url_https":"https:\/\/twimg0-a.akamaihd.net\/images\/themes\/theme1\/bg.png","url":null,"profile_background_image_url":"http:\/\/a0.twimg.com\/images\/themes\/theme1\/bg.png","notifications":false,"profile_link_color":"0084B4","statuses_count":1,"lang":"en","location":null,"utc_offset":null,"geo_enabled":false,"id_str":"1398065154","profile_use_background_image":true,"default_profile":true,"profile_text_color":"333333","friends_count":6,"protected":false,"description":"","follow_request_sent":false,"is_translator":false,"following":false,"profile_image_url":"http:\/\/a0.twimg.com\/sticky\/default_profile_images\/default_profile_3_normal.png","profile_sidebar_border_color":"C0DEED","listed_count":0,"verified":false,"profile_background_tile":false,"created_at":"Thu May 02 20:03:11 +0000 2013","profile_sidebar_fill_color":"DDEEF6"},"created_at":"Thu May 16 20:04:47 +0000 2013"}'
    

if __name__ == '__main__':
    main()
