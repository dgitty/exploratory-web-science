import sys
import requests
import json
from bs4 import BeautifulSoup

FILE = "expanded-URLs.csv"
JSON_FILE = "q1_redirect.json"

QUESTION_FILE="q1a.json"

def main():

    # Using readline()
    filename = open(FILE, "r")
    uri_list=list()
    filename.readline()
    
    count=0
    diff_uri= 0
    ok_count=0
    not_ok = 0
    while True:
        count+=1
        
        # Get next line from file
        line = filename.readline()

        # if line is empty then end of file is reached
        if not line:
            break

        line_info = line.strip().rsplit(',',1)
        
        qa_info=dict()
        final_uri = ""
        current_http_status = 0
        try:
            link = line_info[0]
            print(f"line: {count}, {link}")
            response = requests.get(link, timeout=5)

            final_uri=response.url
            current_http_status=response.status_code

            uri_info=dict()
            uri_info["original_uri"]=link
            uri_info["tweet_freq"]=int(line_info[1]) if line_info[1] != "" else 0

            uri_info["final_uri"]=final_uri
            uri_info["current_http_status"]=current_http_status
            uri_list.append(uri_info)

            if link != final_uri:
                diff_uri+=1

            if current_http_status == 200:
                ok_count+=1

            if current_http_status == 404 or current_http_status == "" or str(current_http_status)[0] != "2":
                not_ok+=1

            qa_info["diff_uri"]=diff_uri
            qa_info["ok_count"]=ok_count
            qa_info["not_ok"]=not_ok

        except:
            print(f"Something went wrong with the response link [{link}]")

    with open(JSON_FILE, "w") as file:
        json.dump(uri_list,file, indent=2)

    with open(QUESTION_FILE, "w") as file:
        json.dump(qa_info,file, indent=2)

if __name__ == "__main__":
    main()
