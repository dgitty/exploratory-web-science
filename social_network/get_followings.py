import tweepy
import sys
import requests
import regex as re
from urllib3.exceptions import ProtocolError, ReadTimeoutError
import urllib.request as urlreq
import json
from rauth import OAuth1Service

FILE= "followings.csv"

# authorization tokens
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""


def main():

    # Instantiate a client
    twitter_client = OAuth1Service(
        name="twitter",
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        base_url="https://api.twitter.com/1.1/",
    )

    twitter_session = twitter_client.get_session((ACCESS_TOKEN, ACCESS_TOKEN_SECRET))

    URL = "https://api.twitter.com/1.1/friends/list.json"
    r = twitter_session.get(
        URL, params={"screen_name": "weiglemc", "skip_status": 1, "count": 100}
    )

    # print(json.dumps(r.json(), indent=2))
    friends_list = r.json()

    count = 0
    friends = list()
    user = dict()
    # add all users
    for f in friends_list["users"]:

        count += 1
        user = dict()
        user["screen_name"] = f["screen_name"]
        user["friends_count"] = f["friends_count"]
        user["labels"] = "f" + str(count)
        friends.append(user)

    # write all users
    with open(FILE, "w") as fp:
        fp.write("USER,FRIENDCOUNT,labels\n")
        for u in friends:
            fp.write(
                "%s,%d,%s\n" % (u["screen_name"], u["friends_count"], u["labels"])
            )

    # add single user
    URL = "https://api.twitter.com/1.1/users/show.json"
    r = twitter_session.get(URL, params={"screen_name": "weiglemc",})
    # print(json.dumps(r.json(), indent=2))
    single_user = r.json()
    with open(FILE, "a") as fp:
        fp.write(
            "%s,%d,%s\n"
            % (single_user["screen_name"], single_user["friends_count"], "U")
        )


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
