'''
Created on Apr 22, 2013

@author: Chun-Ku
'''

#=========================import library=======================================
import twitter
import threading
import datetime
import MySQLdb

def calculateCurrentAge(bornYear, bornMonth):
    now = datetime.datetime.now()
    currentAge = (now.year - bornYear) * 12 + now.month - bornMonth
    return currentAge

def selectMilestoneQuery(currentAge, most_recent_milestone):
    query = "SELECT questionID, text FROM questionnairecontent WHERE month = " + str(currentAge) + " AND questionID > " + str(most_recent_milestone) + " ORDER BY questionID ASC;"
    return query

def postTweet(database, account):
    print "postTweet for account " + account[1]
    '''
    twitteraccount table
    account[0]: id
    account[1]: account_name
    account[2]: consumter_key
    account[3]: consumer_secret
    account[4]: access_token_key
    account[5]: access_token_secret
    account[6]: bornYear
    account[7]: bornMonth
    account[8]: most_recent_milestone
    
    TODO: use macro to for table fields make code readable and easy to maintain
    ''' 
    currentAge = calculateCurrentAge(account[6], account[7])
    print "current age = " + str(currentAge)
    query = selectMilestoneQuery(currentAge, account[8])
    print query
    cursor = database.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    
    if row == None:
        # TODO: select activiy or tip to tweet
        print "select activity or tip to tweet"
        cursor.close()
        return None
    else:
        # post milestone to twitter
        print row
        api = twitter.Api(consumer_key=account[2], consumer_secret=account[3], access_token_key=account[4], access_token_secret=account[5])
        status = row[1]
        print "original: " + status
        milestone_id = row[0]
        # replace %n% --> your baby; %pa%-->their
        status = status.replace('%n%', 'your baby').replace('%pa%', 'their').replace('%s%', 'he/she').replace('%o%', 'him/her')
        print "after replacement: " + status
        api.PostUpdate(status)
        cursor.close()
        return milestone_id  # return milestone id

def updateMilestoneOnTwitterAccountTable(database, most_recent_milestone, account_id):
    query = 'UPDATE twitteraccount SET most_recent_milestone = ' + str(most_recent_milestone) + '  WHERE id = ' + str(account_id) + ";"
    print query
    cursor = database.cursor()
    cursor.execute(query)
    cursor.close()
    database.commit()        

def startPostTweets():
    '''
    go through the twitteraccount table and post one milestone for each account
    '''
    db = MySQLdb.connect(host="db.babystepsuw.org", user="babystepsdbadmin",
                  passwd="vNRLtLf2Rhyy", db="babystepsdb")
    cur = db.cursor()
    cur.execute("SELECT * FROM twitteraccount;")
    
    while True:
        row = cur.fetchone()
        if row == None:
            break
        most_recent_milestone = postTweet(db, row)
        if most_recent_milestone != None:
            updateMilestoneOnTwitterAccountTable(db, most_recent_milestone, row[0])
    
    cur.close()
    db.close()
    


def main():
    '''
    for i in range(10):
        startPostTweets()
        threading.Event().wait(30)
        '''
    startPostTweets()

if __name__ == '__main__':
    main()
