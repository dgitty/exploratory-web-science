import sys
import urllib.request
import json
from urllib.parse import urlparse
import requests
import operator
from tldextract import extract

OUTFILE = "q1_domain.json"
JSON_FILE = "q1_redirect.json"
QUESTION_FILE="q1b.json"
CSV_FILE="q1_tweets_per_domain.csv"

def main():

    with open(CSV_FILE, "a") as fp:
        fp.write(f"domain,number_of_tweets\n")

    qa_info=dict()
    domain_freq=dict()
    with open(JSON_FILE, "r") as file:
        try:
            # read json file
            redirect_list = json.load(file)
            domain_list= dict()
            for r in redirect_list:
                tsd, td, tsu = extract(r["final_uri"]) # prints abc, hostname, com

                domain = td + '.' + tsu # will prints as hostname.com
                
                appeared=1
                tweet_freq = r["tweet_freq"]
                if domain in domain_list:
                    appeared = appeared + domain_list[domain]["appeared"]
                    tweet_freq = tweet_freq + domain_list[domain]["total_num_of_tweets_appeared"]

                domain_list[domain]={ "unique_domain":domain,"appeared":  appeared,"total_num_of_tweets_appeared": tweet_freq}
                domain_freq[domain]=tweet_freq

            qa_info["top5"] = dict(sorted(domain_freq.items(), key=operator.itemgetter(1), reverse=True)[:5])
            qa_info["num_unique_domain"]=len(domain_list)
                
        except:
            print(f"Something went wrong with loading json [{file}]")

    with open(OUTFILE, "w") as file:
        json.dump(domain_list,file, indent=2)

    with open(QUESTION_FILE, "w") as file:
        json.dump(qa_info,file, indent=2)

    for d,v in domain_freq.items():
        with open(CSV_FILE, "a") as f:
            f.write(f"{d},{v}\n")

if __name__ == "__main__":
    main()