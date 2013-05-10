'''
Created on May 2, 2013

@author: Yang
'''

import twitter
#import MySQLdb
from decimal import *


api = twitter.Api(consumer_key='d3UzxZGL1nHnij6N3vTKA',
                      consumer_secret='Z11fcmiwNCW7JI8l4g6cIhDG1w6ZsLS2uApTpVnRo',
                      access_token_key='54065003-PPp1hbbt02oL4rzZ82vVL6i6ry1SVdcayMEtlRwC3',
                      access_token_secret='ouqVXw0nJCg7OrVH1hqYZtwuRTrP6wFqblaYE8qHI')


'''
get mention
    get hashtags
        get question_number
            if question_number exists
                get answer, child_id?, respondant's twitter_id, message date
                write to questionnaireresponses_db
            else
                find reply source
                    if source exists
                        get hashtags
                            get question_number
                                if question_number exists
                                    get answer, child_id?, respondant's twitter_id, message date
                                    write to questionnaireresponses_db
                                else (question_number does not exist in source)
                                    source not valid, ignore
                    else (source does not exist)
                        ignore? 
'''

'''
Q1: child_id? use first name? pseudo-name, done when registering
Q2: question number hashtag format? #BabyQ123
Q3: what we should do if parent forget to include question number hashtag? default error message sent via DM
Q4: use other hashtags? match the pseudo-name with database one-by-one. 
Q5: no way to mark the responses that are already collected? Just collect replies that posted in last 2 hours. 
Q6: add "last time checked" time stamp in twitter_account table? use Coralbells to auto-run script
'''


def getHashtagSet(status):
    print "getHashtagSet() started. "
    s = status.text
    hashtagSet = set(part[1:] for part in s.split() if part.startswith('#'))
    print 'Hashtags: '
    for hashtag in hashtagSet:
        print hashtag
    print "getHashtagSet() ended. "
    return hashtagSet
    
def getQuestionID(hashtagSet):
    print "getQuestionID() started. "
    flag = False
    for hashtag in hashtagSet: 
        if (hashtag.lower().startswith('babyq')): 
            questionIDstr = hashtag[5:]
            questionIDnum = Decimal(questionIDstr)
            print hashtag + ":" + questionIDstr
            print questionIDnum
            flag = True
            break
    if (flag): 
        print "Found. getQuestionID() ended. "
        return questionIDnum
    else: 
        print "Not found. getQuestionID() ended. "
        return 0
    
    '''We use #BabyQ123 for milestone number hashtags'''

def questionIDfromSource(status):
    print
    sourceId = status.GetInReplyToStatusId()
    source = api.GetStatus(sourceId)
    hashtagSet = getHashtagSet(source)
    questionIDnum = getQuestionID(hashtagSet)
    return questionIDnum

    ''' If question number hashtag not found, trace to the original message to find it. '''
    
    
def getAnswer(hashtagSet):
    print "getAnswer() started. "
    answer = "none"
    for hashtag in hashtagSet:
        if (hashtag.lower().startswith('yes')): 
            answer = "Yes"
            break
        elif (hashtag.lower().startswith('no')):
            answer = "Not Yet"
            break
        elif (hashtag.lower().startswith('sometimes') or hashtag.lower() == 's'): 
            answer = "Sometimes"
            break
    print "getAnswer() ended. Answer is: " + answer
    return answer
    
    '''What's the answer we should write in to database?'''

def getChildID(hashtagSet, accountID):
    print
    '''
        childFirstNames = 'select firstName from child where accountID=accountID'
        for hashtag in hashtagSet: 
            for childFirstname in childFirstNames: 
                if(hashtag == childFirstName): 
                    childID = 'select childID from child where childPseudoName=currChildPseudoName'
        return childID
    '''
    
    ''' Where's the psuedo-name stored in database? Specify the format of Child hashtag? '''

def getAccountID(screenName):
    '''
        accountID = 'select accountID from contactInfo where twitter=screenName'
        return accountID
    '''
    print

def writeResponseToDb(accountID, responseDate, childID, questionID, answer, responseTime, twiterAccountID):
    ''' insert into questionnaireresponses accountID, responseDate, childID, questionID, answer '''
    ''' insert into twitteraccount lastchecked=responseTime where id=twitterAccountID'''
    print

def userRegistered(screenName):
    '''
        twitterAccounts = 'select twitter from contactinfo'
        found = False
        for twitterAccount in twitterAccounts: 
            if(screenName == twitterAccount): 
                found = True
                break
        return found          
    '''
    
    print
    
    ''' 
        Check if the user is registered with us, 
        if so, when they forget to add #BabyQ123, send error message. 
        Question: what if the user just want to play around with our twitter accounts...? 
    '''
    
def sendErrorDM(screenName):
    print
   

mentions = api.GetMentions(None, None, None)
for mention in mentions: 
    hashtagSet = getHashtagSet(mention)
    questionID = getQuestionID(hashtagSet)
    if (questionID != 0):
        answer = getAnswer(hashtagSet)
        screenName = mention.GetUser().GetScreenName()
        print "Screen Name: " + screenName
        accountID = getAccountID(screenName)
        childID = getChildID(hashtagSet, accountID)
        responseTime = mention.GetCreatedAt()
        print responseTime
        
        #writeResponseToDb(accountID, responseDate, childID, questionID, answer, responseTime, twitterAccountID)
        
    else: 
        questionID = questionIDfromSource(mention)
        if (questionID != 0): 
            answer = getAnswer(hashtagSet)
            screenName = mention.GetUser().GetScreenName()
            accountID = getAccountID(screenName)
            childID = getChildID(hashtagSet, accountID)
            responseTime = mention.GetCreatedAt()
            
            #writeResponseToDb(accountID, responseDate, childID, questionID, answer, responseTime, twiterAccountID)
            
        else: 
            if (userRegistered(screenName)): 
                sendErrorDM(screenName)
    

''' Once a week, retweet the help message. Broadcasting. '''
    
#print 'Mentions of @yangxiaotong'
#printStatus(mentions)
