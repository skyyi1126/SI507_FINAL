import requests
import requests.auth
import json
import praw
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import sys
import sqlite3
import csv
from secret import reddit
from datetime import datetime

subreddit = reddit.subreddit('nba')

def get_player():
    nba_player_list = []
    with open("nbaplayers1718.csv", "r") as csv_file:
        spamreader = csv.reader(csv_file, delimiter=',')
        ignore_first_row = 1
        for row in spamreader:
            if ignore_first_row:
                ignore_first_row = 0
            else:
                nba_player_list.append(row[2])
    return nba_player_list

def create_database():
    DBNAME = 'nba.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Players';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Submissions';
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Players' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'NAME' TEXT NOT NULL,
            'Submission1Id' INTEGER NOT NULL,
            'Submission2Id' INTEGER NOT NULL,
            'Submission3Id' INTEGER NOT NULL,
            'Submission4Id' INTEGER NOT NULL,
            'Submission5Id' INTEGER NOT NULL,
            FOREIGN KEY ('Submission1Id') REFERENCES Countries('Id'),
            FOREIGN KEY ('Submission2Id') REFERENCES Countries('Id'),
            FOREIGN KEY ('Submission3Id') REFERENCES Countries('Id'),
            FOREIGN KEY ('Submission4Id') REFERENCES Countries('Id'),
            FOREIGN KEY ('Submission5Id') REFERENCES Countries('Id')
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Submissions' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'RedditId' TEXT NOT NULL,
            'Title' TEXT NOT NULL,
            'CommentNumber' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit()
    
    for i in range(1, 51):
        statement = """
        ALTER TABLE 'Submissions' add 'Comment""" + str(i) + "' TEXT"
        cur.execute(statement)
    
    conn.commit()
    conn.close()

def populate_database(nba_player_list):
    DBNAME = 'nba.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    reddit_ids = []
    def insert(player):
        submission_list = []
        for submission in subreddit.search(player, limit=5):
            if submission.id in reddit_ids:
                submission_list.append(reddit_ids.index(submission.id) + 1)
            else:
                insertion = [None, submission.id, submission.title, submission.num_comments]
                if len(submission.comments) > 50:
                    for comment in submission.comments[0:50]:
                        insertion.append(comment.body)
                else:
                    for comment in submission.comments:
                        try:
                            insertion.append(comment.body)
                        except:
                            insertion.append(None)
                    for comment in range(0, 50-len(submission.comments)):
                        insertion.append(None)
                insertion = tuple(insertion)
                statement = "INSERT INTO 'Submissions' VALUES ("
                for i in range(0, 53):
                    statement += "?,"
                statement += "?)"
                cur.execute(statement, insertion)
                reddit_ids.append(submission.id)
                submission_list.append(len(reddit_ids))

        insertion = (None,player,submission_list[0],submission_list[1],submission_list[2],submission_list[3],submission_list[4])
        statement = "INSERT INTO 'Players' VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(statement, insertion)
    for i in nba_player_list:
        insert(i)
    conn.commit()
    conn.close()
"""
create_database()

populate_database(get_player())
"""

class Cache:
    def __init__(self):
        self.reddit_ids = []
        try:
            with open ("cache_data","r") as cache_f:
                cache = cache_f.read()
                self.time_diction = json.loads(cache)
        except:
            self.time_diction = {}

    def get_id(self):
        DBNAME = 'nba.db'
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        statement = '''
            SELECT RedditId FROM Submissions
        '''
        results = cur.execute(statement)
        for i in results:
            self.reddit_ids.append(i[0])
        return self.reddit_ids
    
    def get_time(self):
        print(self.reddit_ids)
        for i in self.reddit_ids:
            time = reddit.submission(id=i).created_utc
            self.time_diction[i] = time
            print(time)
        return self.time_diction

    def dump(self):
        cache_dump=json.dumps(self.time_diction, indent = 4)
        with open("cache_data","w") as file:
            file.write(cache_dump)

cache = Cache()
"""
with open("date.txt", "w") as file:
	for i in cache.time_diction:
		time = datetime.fromtimestamp(int(cache.time_diction[i]))
		file.write(str(time.year) + "/" + str(time.month) + "/" + str(time.day) + "\n")
"""
"""
cache.get_id()
cache.get_time()

cache.dump()
"""
