import tweepy
import sys
import requests
import regex as re
from urllib3.exceptions import ProtocolError, ReadTimeoutError
import urllib.request as urlreq
import json
from rauth import OAuth1Service

FILE="top100.csv"
TWEET_FILE="q1_tweets.json"

# authorization tokens
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""


accounts=dict()
def main():

    # Instantiate a client
    twitter_client = OAuth1Service(
        name="twitter",
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        base_url="https://api.twitter.com/1.1/",
    )

    twitter_session = twitter_client.get_session((ACCESS_TOKEN, ACCESS_TOKEN_SECRET))



    print("twitter session established")
     # Using readline()
    filename = open(FILE, "r")

    while True:
        
        # Get next line from file
        line = filename.readline()

        # if line is empty then end of file is reached
        if not line:
            break

        screen_name = line.strip()
        print(f"screen name: {screen_name}")

        
        URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        r = twitter_session.get(
            URL, params={"screen_name": screen_name, "exclude_replies": True, "count": 200, "tweet_mode":"extended"}
        )

        tweet_list = r.json()

        # add all tweets
        tweets = []
        count=0
        for t in tweet_list:
            count+=1
            full_text =t["full_text"]
            tweets.append(full_text)
        
        accounts[screen_name]=tweets
        
    with open(TWEET_FILE, "w") as file:
        json.dump(accounts,file, indent=2)

if __name__ == "__main__":

    # set_credentials()
    with open("../twittercred.json", "r") as credfile:
        try:
            # read josn file
            data = json.load(credfile)
        except:
            print("Unable to read Cred..")

    CONSUMER_KEY = data["API Key"]
    CONSUMER_SECRET = data["API Secret Key"]
    ACCESS_TOKEN = data["Access Token"]
    ACCESS_TOKEN_SECRET = data["Access Token Secret"]

    main()
