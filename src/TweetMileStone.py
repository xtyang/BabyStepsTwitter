'''
Created on Feb 28, 2013

@author: Chun-Ku
'''

import twitter
from threading import Timer

def tweetMileStone(i):
    '''
    TODO: change the consumer_key to reflect the actual twitter account
    need to find a way to tweets only use user name and password
    '''
    api = twitter.Api(consumer_key='XCyXHzIUUJx5YuJ2fysNA', consumer_secret='wuxBc0s3W5SDoA3rthCdpyW44kxOOszQabP2MSlecw', access_token_key='89890379-rJ671utfeJIAJ6yEn28pQf8XqTzDCR3IFEKTUylg4', access_token_secret='zXIdEEsxx2LClb7rDJepE9vjRithggJkc19cHeJLmOo')
    api.PostUpdate('post 1 #baby_steps_123' + i)
    

def main():
    Timer(5, tweetMileStone, ("1")).start()
    Timer(100, tweetMileStone,("2")).start()
    '''
    although you can see TwitterError: Status is a duplicate in console, you can still see the tweets on twitter. 
    '''
    '''
    test how to merge
    '''

if __name__ == "__main__":
    main()