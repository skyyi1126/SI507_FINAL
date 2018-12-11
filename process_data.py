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
import nltk
from nltk.corpus import stopwords


def task1():
    DBNAME = 'nba.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = """
        SELECT p.NAME, s1.CommentNumber, s2.CommentNumber, s3.CommentNumber, s4.CommentNumber, s5.CommentNumber
        FROM Players p 
        JOIN Submissions s1
            On p.Submission1Id = s1.Id
        JOIN Submissions s2
            On p.Submission2Id = s2.Id
        JOIN Submissions s3
            On p.Submission3Id = s3.Id
        JOIN Submissions s4
            On p.Submission4Id = s4.Id
        JOIN Submissions s5
            On p.Submission5Id = s5.Id
    """
    results = cur.execute(statement)
    result_list = []
    with open("task1.txt", "w") as write_file:
        write_file.write("Name, CommentNumber\n")
        for i in results:
            result_list.append([i[0], i[1]+i[2]+i[3]+i[4]+i[5]])
            write_file.write(i[0] + ", " + str(i[1]+i[2]+i[3]+i[4]+i[5]) + "\n")
    return result_list


def task2(player):
    stop_words = list(stopwords.words("english"))
    stop_words_extra = ['a', 'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at', 'away', 'b', 'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes', 'been', 'before', 'began', 'behind', 'being', 'beings', 'best', 'better', 'between', 'big', 'both', 'but', 'by', 'c', 'came', 'can', 'cannot', 'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could', 'd', 'did', 'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'down', 'downed', 'downing', 'downs', 'during', 'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even', 'evenly', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'f', 'face', 'faces', 'fact', 'facts', 'far', 'felt', 'few', 'find', 'finds', 'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered', 'furthering', 'furthers', 'g', 'gave', 'general', 'generally', 'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good', 'goods', 'got', 'great', 'greater', 'greatest', 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'herself', 'high', 'high', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 'interesting', 'interests', 'into', 'is', 'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows', 'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely', 'long', 'longer', 'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed', 'needing', 'needs', 'never', 'new', 'new', 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered', 'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p', 'part', 'parted', 'parting', 'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 'possible', 'present', 'presented', 'presenting', 'presents', 'problem', 'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 'side', 'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone', 'something', 'somewhere', 'state', 'states', 'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things', 'think', 'thinks', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today', 'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two', 'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted', 'wanting', 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'when', 'where', 'whether', 'which', 'while', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years', 'yet', 'you', 'young', 'younger', 'youngest', 'your', 'yours', 'z']
    stop_words += stop_words_extra
    stop_words += ["n't", "game", "games", "He", "player", "players", "I", "This", "That", "shit", "season", "fine", "lol", "play", "guy", "gon"]
    DBNAME = 'nba.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT p.NAME, s1.*, s2.*, s3.*, s4.*, s5.*
        FROM Players p
        JOIN Submissions s1
            On p.Submission1Id = s1.Id
        JOIN Submissions s2
            On p.Submission2Id = s2.Id
        JOIN Submissions s3
            On p.Submission3Id = s3.Id
        JOIN Submissions s4
            On p.Submission4Id = s4.Id
        JOIN Submissions s5
            On p.Submission5Id = s5.Id
        WHERE p.NAME LIKE "%'''
    statement += player + '%"'
    results = cur.execute(statement)
    result_list = []
    with open("task2.txt", "w", encoding="utf-8") as write_file:
        write_file.write("Name, Comments\n")
        for result in results:
            #print(result[0])
            for i in range(0,5):
                for j in range(0,50):
                    comment = result[54*i+5+j]
                    if comment!=None:
                        result_list.append(result[54*i+5+j] + " ")
                        write_file.write(result[54*i+5+j])
    
    
    def start_with_alpha(word):
        asc = ord(word[0])
        if asc >= 65 and asc <=90:
            return True
        elif asc >= 97 and asc <=122:
            return True
        else:
            return False

    def not_stop(word):
        if word.lower() in stop_words:
            return False
        else:
            return True

    def not_http(word):
        if word == "http" or word == "https" or word == "RT":
            return False
        else:
            return True

    WORD_DICTION = {}
    for i in result_list:
        tokens=[nltk.word_tokenize(i)]
        for j in tokens[0]:
            if (start_with_alpha(j) and not_stop(j) and not_http(j)):	
                if j in WORD_DICTION:
                    WORD_DICTION[j] += 1
                else:
                    WORD_DICTION[j] = 1
    with open("./static/data/"+ player +".txt", "w", encoding="utf-8") as file:
        file.write("keyword,num\n")
        for i in sorted(WORD_DICTION.items(), key=lambda item: item[1], reverse=True)[0:100]:
            file.write(i[0] + ", " + str(i[1]) + "\n")
"""
for i in task1():
    print(i[0])
    task2(i[0])
"""

def task3(player):
    DBNAME = 'nba.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT s1.Title, s2.Title, s3.Title, s4.Title, s5.Title
        FROM Players p
        JOIN Submissions s1
            On p.Submission1Id = s1.Id
        JOIN Submissions s2
            On p.Submission2Id = s2.Id
        JOIN Submissions s3
            On p.Submission3Id = s3.Id
        JOIN Submissions s4
            On p.Submission4Id = s4.Id
        JOIN Submissions s5
            On p.Submission5Id = s5.Id
        WHERE p.NAME LIKE "%'''
    statement += player + '%"'
    results = cur.execute(statement)
    result_list = []
    for i in results.fetchone():
        result_list.append(i)
    return result_list