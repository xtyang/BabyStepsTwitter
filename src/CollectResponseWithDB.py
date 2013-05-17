'''
Created on May 9, 2013

@author: Tien
'''
import time
import twitter
import MySQLdb
from decimal import *


db = MySQLdb.connect(host="db.babystepsuw.org",user="babystepsdbadmin",
passwd="vNRLtLf2Rhyy",db="babystepsdb") 
#host= db.babystepsuw.org

cursor  = db.cursor()
api     = None


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
    global api
    print "getQuestionIDfromSource() started. "
    print api
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
      
 
def getAccountID(screenName):
    # -1 for null
    print "getAccountID() started."
    query = cursor.execute('SELECT accountID FROM contactinfo WHERE twitter=%s',(screenName))
    tmpID   = -1
    for accountID in cursor.fetchall() :
        print "accountID:"
        print accountID[0]
        tmpID   = accountID[0]
    return tmpID


def getChildID(hashtagSet, accountID):
    #-1 == null
    #the data format of childInfos :{child_id accountID laName fiName miName birthD gen image laID laTime}
    print "getChildID started."
    print "with paras",hashtagSet,accountID
    childRowNum = cursor.execute('SELECT * FROM child WHERE accountID =%s', (accountID))
    childInfos  = cursor.fetchall()
    childID   = -1
    for childData in childInfos:
        #print childData
        if childData[3] in hashtagSet:
            childID = childData[0]
    print "childID:"
    print childID
    return childID
        
          
def writeResponseToDb(accountID, childID, questionID, answer, responseTime, screenName):
    # DB: responseID, childID, questionID, answer, accountID, date
    print("writeResponseToDb() started.")
    tmpS    = "INSERT INTO questionnaireresponses (childID, questionID, answer, accountID, date) VALUES('%s','%s','%s','%s','%s')"% (childID, questionID, answer, accountID, responseTime)
    print tmpS
    cursor.execute(tmpS)
    #tmpS    = "UPDATE `babystepsdb`.`twitteraccount` SET `lastchecked` = '%s' WHERE `account_name` = '%s'"% (responseTime, screenName)
    #print tmpS
    #cursor.execute(tmpS)
    db.commit()
    print("insert response to DB succeed. ")
 
def userRegistered(screenName):
    twitterRowNum   = cursor.execute('SELECT * FROM contactinfo')
    twitterInfos    = cursor.fetchall()
    tmpTwitter      = []
    for twitter in twitterInfos:
        #print twitter
        tmpTwitter.append(twitter[3])
    if screenName in tmpTwitter:
        return True
    return False     
    
def sendErrorDM(screenName):
    global api
    api.PostDirectMessage(screenName, "Reminder: respond to questions with #yes #sometimes or #notyet and #firstname and #babycode.")

def timeToDate(timeS):
    #Sat May 11 06:49:04 +0000 2013  to date 2013-05-12 00:00:00
    t   = time.strptime(timeS, "%a %b %d %H:%M:%S +0000 %Y") 
    ts  = time.strftime("%Y-%m-%d %H:%M:%S",t)
    return ts

def main():
    global api
    twitterAccountRowNum    = cursor.execute("SELECT * FROM twitteraccount")
    print "twitterAccountRowNum" ,twitterAccountRowNum
    twitterAccountLt    = []
    while True:
        tmpTwitter  = cursor.fetchone()
        if tmpTwitter == None:
            break
        twitterAccountLt.append(tmpTwitter)
        
    for twitterAccount in twitterAccountLt:
        
        if twitterAccount == None:
            print "twitterAccount" , twitterAccount
            break
        print   twitterAccount
        api     = twitter.Api(  consumer_key=twitterAccount[2],
                                consumer_secret=twitterAccount[3],
                                access_token_key=twitterAccount[4],
                                access_token_secret=twitterAccount[5])

        mentions = api.GetMentions(None, None, None)
        print api
        for mention in mentions: 
            print "--------------------------------------------------------"
            responseTime = timeToDate(mention.GetCreatedAt())
            print responseTime
            hashtagSet = getHashtagSet(mention)
            
            print 'hashtagset',hashtagSet 
            questionID = getQuestionID(hashtagSet)
            print 'questionID',questionID
            if (questionID != 0):
                print api
                answer = getAnswer(hashtagSet)
                screenName = mention.GetUser().GetScreenName()
                print "Screen Name: " + screenName
                accountID = getAccountID(screenName) 
                childID = getChildID(hashtagSet, accountID)
                print "childID",childID
                print "prepare to write data into DB"
                if childID != -1:
                    writeResponseToDb(accountID, childID, questionID, answer, responseTime, screenName)
                
            else:
                print api 
                questionID = getQuestionIDfromSource(mention)
                if (questionID != 0): 
                    answer = getAnswer(hashtagSet)
                    screenName = mention.GetUser().GetScreenName()
                    accountID = getAccountID(screenName)
                    childID = getChildID(hashtagSet, accountID)
                    if childID !=-1:
                        writeResponseToDb(accountID, childID, questionID, answer, responseTime, screenName)
                        pass
                    
                else: 
                    screenName = mention.GetUser().GetScreenName()
                    if (userRegistered(screenName)): 
                        sendErrorDM(screenName)
            print "========================================================"
        print 'end of loop'
    db.close()
if __name__ == '__main__':
    main()
    #print timeToDate("Sat May 11 06:49:04 +0000 2013")
    #print userRegistered('aaaaaaaaa')
    #print userRegistered('tien0730')