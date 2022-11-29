import sys
import os
import subprocess
import urllib.request
import requests
import json
import os
import datetime
from pathlib import Path

DIRECTORY = "timemap"


def main():

    total_uri = 0
    no_mem = 0

    # read each file
    memento = dict()
    count = 0
    filelist = sorted(Path(DIRECTORY).iterdir(), key=os.path.getmtime)
    print(filelist)

    for filename in filelist:
        count += 1
        filepath = DIRECTORY + "/" + filename.name
        with open(filepath, "r") as f:
            print(f"filename: {filename}")
            total_uri += 1
            try:
                # read jssn file
                data = json.load(f)

                if "mementos" in data:
                    # print(data["original_uri"])
                    # print(data["mementos"]["first"]["datetime"])
                    memento[data["original_uri"]] = data["mementos"]["first"][
                        "datetime"
                    ]

                    #  "datetime": "2020-10-11T15:08:49Z",
                    first_date = datetime.datetime.strptime(
                        memento[data["original_uri"]], "%Y-%m-%dT%H:%M:%SZ"
                    )

                    # calculate age between collection and earliest datetime
                    mem_age = dict()
                    mem_age["original_uri"] = data["original_uri"]

                    mem_cnt = 0
                    mem_day = dict()

                    mem_age_list = list()
                    num_mem_list = list()
                    for mem in data["mementos"]["list"]:
                        mem_cnt += 1
                        mem_date = datetime.datetime.strptime(
                            mem["datetime"], "%Y-%m-%dT%H:%M:%SZ"
                        )
                        age = mem_date - first_date
                        mem_day[mem_cnt] = age.days
                        num_mem_list.append(mem_cnt)
                        mem_age_list.append(age.days)

                    # mem_age["age_at_mem"]=mem_day
                    mem_age["age"] = mem_age_list
                    mem_age["num_of_mem"] = num_mem_list

                    # save age and nummber of mementos
                    # write text to json file
                    logfile = "memento_age/memento_age_" + str(count) + ".json"
                    with open(logfile, "w") as memfile:
                        json.dump(mem_age, memfile)

                else:
                    memento[data["original_uri"]] = "none"
                    no_mem += 1
            except:
                print("Problem loading json...")

    with open("earliest_memento.json", "w") as file:
        json.dump(memento, file)

    with open("q3_total", "w") as countfile:
        countfile.write("Total URIs: %d\nno mementos: %d" % (total_uri, no_mem))


if __name__ == "__main__":
    main()
