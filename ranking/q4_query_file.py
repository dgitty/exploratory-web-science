import sys
import os
import subprocess
import urllib.request
import json
import os
import datetime
from pathlib import Path
import regex as re
import math
from collections import OrderedDict
from urllib.parse import urlparse
from boilerpy3 import extractors


DIRECTORY = "q1_process_html"
LIST_FILE= "q2_query_list"
RANK_FILE = "q4_rank.csv"
# RANK_FILE = "q4_rank_more.csv"
WORD="sars"
HASH_URI_FILE ="hash_to_uri.json"

def main():

    # grep for word
    # not recognized in windows command, used in git bash instead.
    # os.system(f"grep -rnliw {WORD} {DIRECTORY} > {LIST_FILE}")

    # read json file of hash to uri
    with open(HASH_URI_FILE, "r") as hashfile:
        try:
            # read json file
            uri_to_hash = json.load(hashfile)
        except:
            print(f"Something went wrong with loading json [{hashfile}]")

    # write headers to csv file
    with open(RANK_FILE, 'w') as urifile:
        urifile.write("TF-IDF,TF,IDF,URI\n")


    # compute IDF of afile
    # Google: 55 B total size in corpus, 55 000 000 000 
    # idf= math.log((55000000000/10),2)
    idf= math.log((1000/10),2)
    # used for more
    # idf= math.log((1000/33),2)

    # Using readline()
    filename = open(LIST_FILE, "r")
    count = 0

    tflist =dict()
    od_tfidf = dict()
    domainlist=dict()

    while True:

        # Get next line from file
        line = filename.readline()

        # if line is empty then end of file is reached
        if not line:
            break

        hashpath = line.strip()
       
        # get the hash from the filename
        hash_text = re.sub(r'^.*?content_', '', hashpath)
        uri = uri_to_hash[hash_text]

        domain = urlparse(uri).netloc
        # print(domain) # --> www.example.test

        # get unique domains only
        if domain not in domainlist:
            count += 1
            domainlist[domain]=True
            # print(domain)

            # read content of each file
            hashpathfile = open(hashpath, "r")
            uri_text = hashpathfile.read()
            words = uri_text.split()
            num_words = len(words)
            
            # compute TF of afile
            tf= uri_text.lower().count(WORD)
            tfnorm = tf/num_words
            tflist[uri]= tfnorm
            
            # compute TF-IDF of afile
            tfidf = tfnorm *idf
            od_tfidf[uri]=tfidf

            # print(f"{uri}: {tfidf},{tfnorm}")

        # break once 10 files has been reached
        if count == 10:
            break

    filename.close()


    rank =dict()
    for k, v in sorted(od_tfidf.items(), key=lambda item: item[1], reverse=True):
        rank[k]=v


    # output to csv file by rank of tfidf
    with open(RANK_FILE, "a") as file:
        for key, value in rank.items(): 
            # print(key, value)
            file.write("%f,%f,%f,%s\n"%(value,tflist[key],idf,key))


if __name__ == "__main__":
    main()