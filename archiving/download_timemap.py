import sys
import os
import subprocess
import urllib.request
import requests
import json
import csv

FILE = "unique_links"
BIN_FILE = "uri_vs_mem.csv"
URIMEM_FILE = "uri_vs_mem_simple.csv"


def main():

    uri_vs_mem = dict(list())
    # Using readline()
    filename = open(FILE, "r")
    count = 0

    while True:
        count += 1

        # Get next line from file
        line = filename.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break

        link = line.strip()
        print(f"link: {link}")

        memlink = "http://localhost:1208/timemap/json/" + link

        print(f"memlink: {memlink}")

        r = requests.get(memlink)
        # write text to json file
        logfile = "timemap/timemap_" + str(count) + ".json"
        with open(logfile, "w") as file:
            if "mementos" not in r.text:
                notfound = dict()
                notfound["original_uri"] = link
                notfound["self"] = memlink
                notfound["text"] = r.text.strip()

                json.dump(notfound, file)
            else:
                file.write(r.text)

        # read from json file and add to dictionary bin
        with open(logfile, "r") as logfile:
            print(f"filename: {logfile}")
            num_memento = 0
            try:
                # read json file
                data = json.load(logfile)

                # check if memento exist for file
                if "mementos" in data:
                    num_memento = len(data["mementos"]["list"])
                else:
                    num_memento = 0

                # increment uri for number of memento
                if num_memento not in uri_vs_mem:
                    uri_vs_mem[num_memento] = 0

                uri_vs_mem[num_memento] += 1

            except:
                print(f"Something went wrong with [{logfile}]")

        # log uri vs mem to file
        with open(BIN_FILE, "w") as binfile:
            binfile.write("memento,num_of_uri\n")
            for key in uri_vs_mem.keys():
                binfile.write("%s,%s\n" % (key, uri_vs_mem[key]))

    # log all uri and mem
    with open(URIMEM_FILE, "w") as urifile:
        urifile.write("memento,num_of_uri\n")
        for key in uri_vs_mem.keys():
            for _ in range(uri_vs_mem[key]):
                urifile.write("%s,%d\n" % (key, 1))

    filename.close()


if __name__ == "__main__":
    main()
