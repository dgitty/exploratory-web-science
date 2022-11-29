import os
import hashlib
import json

FILE = "unique_links"

def main():
    
    # Using readline()
    filename = open(FILE, "r")
    count = 0

    uri_to_hash =dict()

    while True:
        count += 1

        # Get next line from file
        line = filename.readline()

        # if line is empty then end of file is reached
        if not line:
            break

        link = line.strip()

        # create hex hash encoding then sending to md5() 
        result = hashlib.md5(link.encode()) 

        # acquire hexidecimal
        md5file = result.hexdigest()

        os.system(f"curl {link} > q1_download_content/{md5file}")

        uri_to_hash[md5file]= link

    filename.close()


    with open("hash_to_uri.json", "w") as file:
        json.dump(uri_to_hash, file)

if __name__ == "__main__":
    main()