import tweepy
import sys
import requests
import regex as re
from urllib3.exceptions import ProtocolError, ReadTimeoutError
import urllib.request as urlreq
import json
from rauth import OAuth1Service
import pandas as pd

TWEET_FILE="q1_tweets.json"
DATA_FILE="twitterdata.txt"
COUNTS_FILE="q2_counts_appeared.json"
TERM_FILE="q2_term_per_account.json"

def main():
    apcount={}
    wordcounts={}
    feedlist=[]
    with open(TWEET_FILE, "r") as file:
        try:
            # read json file and gather words
            accounts = json.load(file)
            wordcounts=dict()
            for screen_name, tweet_list in accounts.items():
                feedlist.append(screen_name)
                wc=dict()
                for tweet in tweet_list:
                    words = tweet.split()
                    for word in words:
                        if word.isalpha() and (len(word) > 3 and len(word) < 15):
                            aword=word.lower()
                            wc.setdefault(aword,0)
                            wc[aword]+=1

                wordcounts[screen_name]=wc
                for word, count in wc.items():
                    apcount.setdefault(word,0)
                    if count>1:
                        apcount[word]+=1

            wordlist=[]
            for w,bc in apcount.items():
                frac=float(bc)/len(feedlist)
                if frac>0.1 and frac<0.5: 
                    wordlist.append(w)

        except:
            print(f"Something went wrong with loading json [{file}]")

    # save matrix
    with open(DATA_FILE, "w") as fp:
        fp.write("Account")
        for word in wordlist: 
            fp.write('\t%s' % word)
        fp.write('\n')
        for blog,wc in wordcounts.items():
            fp.write(blog)
            for word in wordlist:
                if word in wc: 
                    fp.write('\t%d' % wc[word])
                else: 
                    fp.write('\t0')
            fp.write('\n')


    # how many times the term appeared over all accounts.
    data_info = pd.read_csv(DATA_FILE, delimiter="\t", engine="python")
    header = list(data_info.columns)[1:]
    popular_word = dict()
    for col in header:
        popular_word[col]=int(data_info[col].sum())

    with open(COUNTS_FILE, "w") as file:
        json.dump(popular_word,file, indent=2)

    # ordered terms per account
    data_info = pd.read_csv(DATA_FILE, delimiter="\t", engine="python")
    header = list(data_info.columns)
    term_per_account = dict()
    
    for idx,row in data_info.iterrows():
        term_count=dict()
        for col in header[1:]:
            term_count[col]=row[col]
        
        sorted_term = dict(sorted(term_count.items(), key=lambda item: item[1], reverse=True))
            
    term_per_account[row[header[0]]]=sorted_term

    with open(TERM_FILE, "w") as file:
        json.dump(term_per_account,file, indent=2)

if __name__ == "__main__":
    main()
