'''
Created on Feb 21, 2013

@author: Yang
'''

import twitter

api = twitter.Api()

api = twitter.Api(consumer_key='d3UzxZGL1nHnij6N3vTKA',
                      consumer_secret='Z11fcmiwNCW7JI8l4g6cIhDG1w6ZsLS2uApTpVnRo',
                      access_token_key='54065003-PPp1hbbt02oL4rzZ82vVL6i6ry1SVdcayMEtlRwC3',
                      access_token_secret='ouqVXw0nJCg7OrVH1hqYZtwuRTrP6wFqblaYE8qHI')

#status = api.PostUpdate('I love python-twitter!')
#print status.text

def findReplySource(reply):
    sourceId = reply.GetInReplyToStatusId()
    source = api.GetStatus(sourceId)
    #sourceUser = source.GetUser()
    print 'Source ID: '
    print sourceId
    print 'Source Content: '
    print source.text
    
def printStatus(statusSet):
    i=1
    for status in statusSet:
        currentUser = status.GetUser()
        currentUserId = currentUser.GetId()
        currentUserScreenName = currentUser.GetScreenName()
        statusContent = status.text
        print str(i) + '. (' + str(currentUserId) + ') @' + currentUserScreenName + ': ' + statusContent
        printHashtags(status)
        findReplySource(status)
        i = i+1
    print '\n'
    #print 'Total Entries Count: %d' % i + '\n'

def printDirectMsg(directMsgSet):
    i=1
    for msg in directMsgSet:
        msgSenderId = msg.GetSenderId()
        msgSenderScreenName = msg.GetSenderScreenName()
        msgContent = msg.text
        print str(i) + '. (' + str(msgSenderId) + ') @' + msgSenderScreenName + ': ' + msgContent
        printHashtags(msg)
        i = i+1
    print '\n'
    
def printHashtags(status):
    s = status.text
    hashtagSet = set(part[1:] for part in s.split() if part.startswith('#'))
    print 'Hashtags: '
    for hashtag in hashtagSet:
        print hashtag
    
    

replies = api.GetReplies(api, None, None)
print 'Replies to @yangxiaotong'
printStatus(replies)


mentions = api.GetMentions(None, None, None)
print 'Mentions of @yangxiaotong'
printStatus(mentions)

directMsgs = api.GetDirectMessages(None, None, None)
print 'Direct Messages of @yangxiaotong'
printDirectMsg(directMsgs)

if __name__ == '__main__':
    pass