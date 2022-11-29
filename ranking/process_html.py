import sys
import os
import subprocess
import urllib.request
import requests
import json
import os
import datetime
from pathlib import Path

from boilerpy3 import extractors


DIRECTORY = "q1_download_content"
PROCESS_DIR= "q1_process_html"


def main():

    # read each file
    count = 0
    filelist = sorted(Path(DIRECTORY).iterdir(), key=os.path.getmtime)

    for filename in filelist:
        count += 1
        filepath = DIRECTORY + "/" + filename.name

        extractor = extractors.ArticleExtractor()

        try:
            # From a file
            content = extractor.get_content_from_file(filepath)
        except:
            content = ""

        content_filepath = PROCESS_DIR+"/"+"content_"+filename.name
        with open(content_filepath, "w") as file:
            file.write(content)

if __name__ == "__main__":
    main()