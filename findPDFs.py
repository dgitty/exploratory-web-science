import sys
import requests
from bs4 import BeautifulSoup

def main(argv):
    # get arg
    uri=sys.argv[1]
    response = requests.get(uri)

    # use beautifulsoup to gather content
    soup = BeautifulSoup(response.text,features="lxml")
    for links in soup.find_all('a'):
        link = links.get('href')
        try:
            response = requests.get(link)

            if response.headers['Content-Type'] == "application/pdf":
                # print info
                print(f"URI: {link}")
                print(f"Final URI: {response.url}")

                content_length = "{:,}".format(int(response.headers['Content-Length']))
                print(f"Content Length: {content_length} bytes")
                print()
        except:
            pass

if __name__ == "__main__":
    main(sys.argv[1:])
