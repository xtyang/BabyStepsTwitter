'''
Created on May 9, 2013

@author: Yang
'''

import twitter

api = twitter.Api(consumer_key='d3UzxZGL1nHnij6N3vTKA',
                      consumer_secret='Z11fcmiwNCW7JI8l4g6cIhDG1w6ZsLS2uApTpVnRo',
                      access_token_key='54065003-PPp1hbbt02oL4rzZ82vVL6i6ry1SVdcayMEtlRwC3',
                      access_token_secret='ouqVXw0nJCg7OrVH1hqYZtwuRTrP6wFqblaYE8qHI')

api.PostDirectMessage("yangxiaotong", "Hello! Welcome to Baby Steps!")

