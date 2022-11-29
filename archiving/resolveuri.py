import sys
import requests
from bs4 import BeautifulSoup
import regex as re


def main(argv):
    # get arg
    uri = sys.argv[1]
    try:
        response = requests.get(uri)

        print(f"URI: {uri}")
        print(f"Final URI: {response.url}")
        print(f"status code: {response.status_code}")
    except:
        pass

    # myString = "This is a link http://www.google.com"
    # myString = "@chukkietweets @Ore_akiinde https://t.co/Qh7qpqefmN #ENDSARS"
    # myString = " hello no links"
    # uri = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    # print(uri)

    # for tweet in tweets:
    #     urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.text)
    #     for url in urls:
    #         try:
    #             res = urllib2.urlopen(url)
    #             actual_url = res.geturl()
    #             print actual_url
    #         except:
    #             print url

    # use beautifulsoup to gather content
    # soup = BeautifulSoup(response.text,features="lxml")
    # for links in soup.find_all('a'):
    #     link = links.get('href')
    #     try:
    #         response = requests.get(link)

    #         if response.headers['Content-Type'] == "application/pdf":
    #             # print info
    #             print(f"URI: {link}")
    #             print(f"Final URI: {response.url}")

    #             content_length = "{:,}".format(int(response.headers['Content-Length']))
    #             print(f"Content Length: {content_length} bytes")
    #             print()
    #     except:
    #         pass


if __name__ == "__main__":
    main(sys.argv[1:])

# https://t.co/DpO767Md1v
