import tweepy
import sys
import requests
import regex as re
from urllib3.exceptions import ProtocolError, ReadTimeoutError
import urllib.request as urlreq
import json

# authorization tokens
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

global link_list
global total

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):

        print(status.id_str)

        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        remove_characters = [",", "\n"]
        for c in remove_characters:
            text.replace(c, " ")
            quoted_text.replace(c, " ")

        if quoted_text != "":
            link = re.search("(?P<url>https?://[^\s]+)", quoted_text)

            try:
                uri = link.group("url")
                total["Total links"] += 1

                # check shortened uri
                # resp = urlreq.urlopen(uri)
                # if resp.getcode() ==200:
                #     total_short = total_short+1

                # get final url
                # response = urllib2.urlopen(uri)
                # final_uri = response.geturl()

                response = requests.get(uri)
                final_uri = response.url
                if response.status_code == 200:

                    if "twitter.com" not in final_uri and final_uri not in link_list:
                        if final_uri != uri:
                            total["Total shortened"] += 1
                            total["Total redirects"] += 1

                        # final_uri = StreamListener.resolve_uri(self,uri)
                        # if final_uri not in link_list:
                        print(f"Got link: {status.id_str}")
                        link_list.append(final_uri)
                        with open("unique_links", "a", encoding="utf-8") as f:
                            f.write("%s\n" % (final_uri))
            except:
                pass

        with open("q1_total.json", "w") as fp:
            json.dump(total, fp)

        if len(link_list) == 1050:
            sys.exit()

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()


if __name__ == "__main__":
    # get total counts
    with open("q1_total.json", "r") as countfile:
        print(f"filename: {countfile}")
        total = json.load(countfile)

    # acquire list
    with open("unique_links") as listfile:
        link_list = listfile.read().splitlines()

    # set_credentials()
    with open("../twittercred.json", "r") as credfile:
        print(f"filename: {credfile}")
        try:
            # read josn file
            data = json.load(credfile)
        except:
            print("Unable to read Cred..")

    consumer_key = data["API Key"]
    consumer_secret = data["API Secret Key"]
    access_key = data["Access Token"]
    access_secret = data["Access Token Secret"]
    print(f"consumer_key: {consumer_key}")
    print(f"consumer_secret: {consumer_secret}")
    print(f"access_key: {access_key}")
    print(f"access_secret: {access_secret}")

    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)
    # api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(
        auth=api.auth, listener=streamListener, tweet_mode="extended"
    )
    # tags = ["EndSars"]
    # tags = ["VPDebate","MapOfTheSoulOne","NBAFinals","EndPolicebrutality"]
    tags = ["NBAFinals"]
    while True:
        try:
            # stream.filter(track=tags)
            stream.sample(languages=["en"])

        except ProtocolError:
            continue
        except ReadTimeoutError:
            continue
        except:
            continue
