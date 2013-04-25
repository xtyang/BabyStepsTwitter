'''
Created on Apr 22, 2013

@author: Chun-Ku
'''
import twitter
import threading
import datetime
import MySQLdb

def startPostTweets():
    '''
    go through the twitteraccount table and post one milestone for each account
    '''
    db = MySQLdb.connect(host="db.babystepsuw.org",user="babystepsdbadmin",
                  passwd="vNRLtLf2Rhyy",db="babystepsdb")
    print db
    print "what happend"
    cur = db.cursor()
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print row
    
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