'''
Created on May 9, 2013

@author: Yang
'''

import twitter
import MySQLdb
from decimal import *


api = twitter.Api(consumer_key='d3UzxZGL1nHnij6N3vTKA',
                      consumer_secret='Z11fcmiwNCW7JI8l4g6cIhDG1w6ZsLS2uApTpVnRo',
                      access_token_key='54065003-PPp1hbbt02oL4rzZ82vVL6i6ry1SVdcayMEtlRwC3',
                      access_token_secret='ouqVXw0nJCg7OrVH1hqYZtwuRTrP6wFqblaYE8qHI')



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
        if (hashtag.lower().startswith('baby0') or hashtag.lower().startswith('baby1')
            or hashtag.lower().startswith('baby2') or hashtag.lower().startswith('baby4')
            or hashtag.lower().startswith('baby5') or hashtag.lower().startswith('baby6')
            or hashtag.lower().startswith('baby7') or hashtag.lower().startswith('baby8')
            or hashtag.lower().startswith('baby9')): 
            questionIDstr = hashtag[4:]
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

def getQuestionIDfromSource(status):
    print "getQuestionIDfromSource() started. "
    sourceId = status.GetInReplyToStatusId()
    if(sourceId == None): 
        questionIDnum = 0
    else: 
        source = api.GetStatus(sourceId)
        hashtagSet = getHashtagSet(source)
        questionIDnum = getQuestionID(hashtagSet)
    print "getQuestionIDfromSource() ended. Result questionIDnum: "
    print questionIDnum
    return questionIDnum
   
    
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
    
    
def sendErrorDM(screenName):
    api.PostDirectMessage("yangxiaotong", "Reminder: respond to questions with #yes #sometimes or #notyet and #firstname and #babycode.")
   

mentions = api.GetMentions(None, None, None)
for mention in mentions: 
    print "--------------------------------------------------------"
    responseTime = mention.GetCreatedAt()
    print responseTime
    hashtagSet = getHashtagSet(mention)
    questionID = getQuestionID(hashtagSet)
    if (questionID != 0):
        answer = getAnswer(hashtagSet)
        screenName = mention.GetUser().GetScreenName()
        print "Screen Name: " + screenName
        accountID = getAccountID(screenName)
        childID = getChildID(hashtagSet, accountID)
        
        #writeResponseToDb(accountID, responseDate, childID, questionID, answer, responseTime, twitterAccountID)
        
    else: 
        questionID = getQuestionIDfromSource(mention)
        if (questionID != 0): 
            answer = getAnswer(hashtagSet)
            screenName = mention.GetUser().GetScreenName()
            accountID = getAccountID(screenName)
            childID = getChildID(hashtagSet, accountID)
            
            #writeResponseToDb(accountID, responseDate, childID, questionID, answer, responseTime, twiterAccountID)
            
        else: 
            screenName = mention.GetUser().GetScreenName()
            if (userRegistered(screenName)): 
                sendErrorDM(screenName)
    print "========================================================"
