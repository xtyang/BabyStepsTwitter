'''
Created on Feb 28, 2013

@author: Chun-Ku
'''

import twitter
import threading
import sqlite3
import datetime

def postTweet(database, account):
    print 'postTweet'
    api = twitter.Api(consumer_key=account[2], consumer_secret=account[3], access_token_key=account[4], access_token_secret=account[5])
    cur = database.cursor()
    query_for_most_recent_updates = 'SELECT milestone_id, month FROM twitter_updates WHERE twitter_id = '+ str(account[0])
    cur.execute(query_for_most_recent_updates) 
    row = cur.fetchone()
    print query_for_most_recent_updates
    print row
    updateText = None
    milestone_id = None
    now = datetime.datetime.now()
    print now
    month = (now.year - account[6])*12 + now.month - account[7] 
    
    if row == None:#the first milestone to post
        print 'first milestone to post'
        query_for_corresponding_updates = 'SELECT milestone_id FROM month_milestones WHERE month = ' + str(month)
        print query_for_corresponding_updates
        cur.execute(query_for_corresponding_updates)
        row = cur.fetchone() #fetch the first milestone to update
        if row != None:
            print 'fisrt milestone text to update'
            milestone_id = row[0]
            query_milestone_text = 'SELECT text FROM milestones WHERE id = ' + str(milestone_id)
            cur.execute(query_milestone_text)
            row = cur.fetchone()
            updateText = row[0]
    else:
        if row[1] == month:
            query_for_corresponding_updates = 'SELECT milestone_id FROM month_milestones WHERE month = ' + str(month)+' AND milestone_id > '+str(row[0])
            print query_for_corresponding_updates
            cur.execute(query_for_corresponding_updates)
            #row[0] is the most recent milestone_id
            row = cur.fetchone()
            print row
            if row != None:
                milestone_id = row[0]
                query_milestone_text = 'SELECT text FROM milestones WHERE id = ' + str(milestone_id)
                cur.execute(query_milestone_text)
                row = cur.fetchone()
                updateText = row[0]
        else:
            query_for_corresponding_updates = 'SELECT milestone_id FROM month_milestones WHERE month = ' + str(month)
            print query_for_corresponding_updates
            cur.execute(query_for_corresponding_updates)
            row = cur.fetchone() #fetch the first milestone to update
            if row != None:
                print 'fisrt milestone text to update'
                milestone_id = row[0]
                query_milestone_text = 'SELECT text FROM milestones WHERE id = ' + str(milestone_id)
                cur.execute(query_milestone_text)
                row = cur.fetchone()
                updateText = row[0]
            
         
    if updateText != None:
        print str(updateText)
        api.PostUpdate(str(updateText)) #TODO: need to catch whether post fail
        #write update to twitter_updates
        cur.execute(query_for_most_recent_updates)
        row = cur.fetchone()
        if row == None:
            insert = 'INSERT INTO twitter_updates VALUES ('+str(month)+', ' +str(account[0]) +', '+ str(milestone_id)+')'
            cur.execute(insert)
            print insert
            database.commit()
        else:
            updates = 'UPDATE twitter_updates SET milestone_id = '+str(milestone_id)+ ', month = '+str(month)+'  WHERE twitter_id = '+str(account[0])
            cur.execute(updates)
            print updates
            database.commit()
    else:
        print 'no updates being made'
            
def startPostTweets():
    db = sqlite3.connect('test.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM BabyStepsTwitterAccount")
    while True:
        row = cur.fetchone()
        if row == None:
            break
        postTweet(db, row)
    db.close()


def main():
    for i in range(10):
        startPostTweets()
        threading.Event().wait(30)
    

if __name__ == "__main__":
    main()
