'''
Created on May 9, 2013

@author: Xiaotong Yang, Li-Tien Ou
'''
import time
import twitter
import MySQLdb
from decimal import *

# Connect to the database
db = MySQLdb.connect(host="140.117.179.157",user="babystepsdbadmin",
passwd="vNRLtLf2Rhyy",db="babystepsdb") 
cursor  = db.cursor()
api     = None
#140.117.179.157
#db.babystepsuw.org
# Filter out all the hashtags in a tweet, return the hashtag set. 
def getHashtagSet(status):
    print "getHashtagSet() started. "
    s = status.text
    hashtagSet = set(part[1:] for part in s.split() if part.startswith('#'))
    print 'Hashtags: '
    for hashtag in hashtagSet:
        print hashtag
    print "getHashtagSet() ended. "
    return hashtagSet

# Filter out the hashtag that contains the baby code, then get the question number. 
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

# If the baby code hashtag was not containted in the reply, try finding the baby code tag in its source tweet (the tweet this reply is replying to)
# This module is not used in the actual process. We left it here as a back-up
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
   
# Filter out the "yes", "not yet", "sometimes" answer from the hashtag set. 
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
        else: 
            answer = None
    print "getAnswer() ended. Answer is: " + answer
    return answer
      
# Retrieve the user's Baby Steps accountId from the database, using her twitter screen name
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

# Get the id of the user's child mentioned in the reply tweet. 
# If this user has registered only one child, we will retrive this child's id even if the user forgot to mention her child's name in her response. 
# If this user has registered multiple children, she must mention the child's name in her replying tweet. 
def getChildID(hashtagSet, accountID):
    #-1 == null
    #the data format of childInfos :{child_id accountID laName fiName miName birthD gen image laID laTime}
    print "getChildID started."
    print "with paras",hashtagSet,accountID
    childRowNum = cursor.execute('SELECT * FROM child WHERE accountID =%s', (accountID))
    childInfos  = cursor.fetchall()
    childID   = -1
    if(len(childInfos) == 1): 
        childID = childInfos[0][0]
    else: 
        for childData in childInfos:
            #print childData
            if childData[3] in hashtagSet:
                childID = childData[0]
    print "childID:"
    print childID
    return childID
        
      
def writeResponseToDb(accountID, childID, questionID, answer, responseTime):
    # DB: responseID, childID, questionID, answer, accountID, date
    print("writeResponseToDb() started.")
    tmpS    = "INSERT INTO questionnaireresponses (childID, questionID, answer, accountID, date) VALUES('%s','%s','%s','%s','%s')"% (childID, questionID, answer, accountID, responseTime)
    print tmpS
    cursor.execute(tmpS)
    db.commit()
    print("insert response to DB succeed.")

# Write the id of the last checked tweet into the database. Next time we will start processing the tweets newer than the last checked tweet. 
def writeLastCheckToDb(screenName, newLastMentionId):
    print("writeLastCheckToDb() started.")
    tmpS    = "UPDATE `babystepsdb`.`twitteraccount` SET `lastMentionId` = '%s' WHERE `account_name` = '%s'"% (newLastMentionId, screenName)
    print tmpS
    cursor.execute(tmpS)
    db.commit()
    print("insert lastcheck to DB succeed. ")

# Check if the user has registered her twitter account with us. 
def userRegistered(screenName):
    twitterRowNum   = cursor.execute('SELECT * FROM contactinfo')
    twitterInfos    = cursor.fetchall()
    tmpTwitter      = []
    for twitter in twitterInfos:
        tmpTwitter.append(twitter[3])
    if screenName in tmpTwitter:
        return True
    return False     

# Send a reminder through direct message if the user forgot to answer the question in its right format. 
def sendErrorDM(screenName):
    global api
    api.PostDirectMessage(screenName, "Reminder: respond to questions with #yes #sometimes or #notyet and #firstname and #babycode.")

def timeToDate(timeS):
    #Sat May 11 06:49:04 +0000 2013  to date 2013-05-12 00:00:00
    t   = time.strptime(timeS, "%a %b %d %H:%M:%S +0000 %Y") 
    ts  = time.strftime("%Y-%m-%d %H:%M:%S",t)
    return ts

# Collect and process every reply we received since last check. 
def processReplies(accountScreenName, mentions): 
    i=1
    newestMention = True
    newLastMentionId = 0
    for mention in mentions: 
        if(userRegistered(mention.GetUser().GetScreenName())): 
            if(newestMention):
                newLastMentionId = mention.GetId()
                print "newLastMentionId",newLastMentionId
                newestMention = False
            print "newLastMentionId: " + str(newLastMentionId)
            print str(i) + "--------------------------------------------------------"
            i=i+1
            print "Friend's Screen Name: " + mention.GetUser().GetScreenName()
            print "Tweet ID: " + str(mention.GetId())
            responseTime = timeToDate(mention.GetCreatedAt())
            print responseTime
            
            hashtagSet = getHashtagSet(mention)
            questionID = getQuestionID(hashtagSet)
            if (questionID != 0):
                print api
                answer = getAnswer(hashtagSet)
                if(answer != None): 
                    screenName = mention.GetUser().GetScreenName()
                    print "Screen Name: " + screenName
                    accountID = getAccountID(screenName) 
                    childID = getChildID(hashtagSet, accountID)
                    print "childID: ", childID
                    print "prepare to write data into DB"
                    if childID != -1:
                        writeResponseToDb(accountID, childID, questionID, answer, responseTime)
                else: 
                    sendErrorDM(mention.GetUser().GetScreenName())
    
            print "========================================================"
    writeLastCheckToDb(accountScreenName, newLastMentionId)
    print 'end of loop'

# Collect and process every direct message since last check. 
def processDMs(accountScreenName, mentions): 
    i=1
    newestMention = True
    newLastMentionId = 0
    for mention in mentions: 
        if(userRegistered(mention.GetUser().GetScreenName())): 
            if(newestMention):
                newLastMentionId = mention.GetId()
                print "newLastMentionId",newLastMentionId
                newestMention = False
            print "newLastMentionId: " + str(newLastMentionId)
            print str(i) + "--------------------------------------------------------"
            i=i+1
            print "Friend's Screen Name: " + mention.GetSenderScreenName()
            print "Tweet ID: " + str(mention.GetId())
            responseTime = timeToDate(mention.GetCreatedAt())
            print responseTime
            
            hashtagSet = getHashtagSet(mention)
            questionID = getQuestionID(hashtagSet)
            if (questionID != 0):
                print api
                answer = getAnswer(hashtagSet)
                if(answer != None): 
                    screenName = mention.GetSenderScreenName()
                    print "Screen Name: " + screenName
                    accountID = getAccountID(screenName) 
                    childID = getChildID(hashtagSet, accountID)
                    print "childID: ", childID
                    print "prepare to write data into DB"
                    if childID != -1:
                        writeResponseToDb(accountID, childID, questionID, answer, responseTime)
                else: 
                    sendErrorDM(mention.GetUser().GetScreenName())
    
    print "========================================================"
    writeLastCheckToDb(accountScreenName, newLastMentionId)
    print 'end of loop'

# Get newly received user replies since last check. 
def getUserReplies(sinceId):
    page = 1
    limit = 2000
    mentions = api.GetFriendsTimeline(None, 100, page, sinceId, False, False)
    
    if(len(mentions) != 0):
        oldLastId = mentions[-1].GetId()
        newLastId = 0
        isNotLast = True
        while(isNotLast and len(mentions) < limit):
            page = page + 1
            moreMentions = api.GetFriendsTimeline(None, 100, page, sinceId, False, False)
            for moreMention in moreMentions: 
                mentions.append(moreMention)
            newLastId = mentions[-1].GetId()
            if(newLastId == oldLastId): 
                isNotLast = False
            else: 
                oldLastId = newLastId
            print "newLastId: " + str(newLastId) + ", oldLastId: " + str(oldLastId)  
            print "sinceId: " + str(sinceId)
            print "Appended 100! "
            print "mentions length: " + str(len(mentions))
        
    return mentions

def main():
    # Set the name of "api" to global so that rest functions can share accountData
    global api
    #===========================================================================
    # get twitterAcount data
    #===========================================================================
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
            print "twitterAccount is None"
            break
        print   twitterAccount
        
        #=======================================================================
        # get api by twitterAccount data, for later use 
        #=======================================================================
        
        api     = twitter.Api(  consumer_key=twitterAccount[2],
                                consumer_secret=twitterAccount[3],
                                access_token_key=twitterAccount[4],
                                access_token_secret=twitterAccount[5])
        
        accountScreenName = twitterAccount[1]

        lastMentionId = twitterAccount[10]
        print "lastMentionId", lastMentionId

        #=======================================================================
        # no lastMentionId skip to next account
        #=======================================================================
        if '0'==lastMentionId:continue     
     
        

        #=======================================================================
        # let sinceID = lastMentionID
        #=======================================================================
        #query   = 'SELECT lastMentionId FROM twitteraccount WHERE account_name="%s"'%(accountScreenName)
        #rowNum  = cursor.execute(query)
        #infos   = cursor.fetchall()
        #sinceId = infos[0][0]
        sinceId  = lastMentionId
        
        directMsgs = api.GetDirectMessages(None, sinceId, 1)
        replies = getUserReplies(sinceId)

        if(len(replies) != 0):
            processReplies(accountScreenName, replies)
            
        if(len(directMsgs) != 0):
            processDMs(accountScreenName, directMsgs)
        
        
    db.close()
if __name__ == '__main__':
    main()
    #print timeToDate("Sat May 11 06:49:04 +0000 2013")
    #print userRegistered('aaaaaaaaa')
    #print userRegistered('tien0730')
