import sys
import json

D2_FILE="q1_domain.json"
D1_FILE="Alternative Domains - Raw Data & Initial Coding - d1.csv"
D3_FILE="NewsGuardTech.com coronavirus domains - 20201028 - d3.csv"
AFILE="d1_d2.csv"
BFILE="d2_d3.csv"
CFILE="d3_d1.csv"
DFILE="d123.csv"

def main():


    a=list()
    b=list()
    c=list()
    d=list()
    d1_domains=list()
    d3_domains=list()
    d2_domains=list()

    # D2 
    with open(D2_FILE, "r") as file:
        try:
            # read json file
            d2 = json.load(file)
            for i in d2.keys():
                d2_domains.append(i)
        except:
            print(f"Something went wrong with loading json [{file}]")

    # print(d2_domains)

    # D1 
    filename = open(D1_FILE, "r")
    filename.readline()
    while True:
        # Get next line from file
        line = filename.readline()
        # if line is empty then end of file is reached
        if not line:
            break

        line_info = line.split(",")
        d1_domains.append(line_info[0].lower())


    # D3 
    filename = open(D3_FILE, "r")
    filename.readline()
    while True:
        # Get next line from file
        line = filename.readline()
        # if line is empty then end of file is reached
        if not line:
            break

        line_info = line.split(",")
        d3_domains.append(line_info[0].lower())

    # gather datasets
    # a. domains that are present in both D1 and D2
    d1_set = set(d1_domains)
    a_intersect = d1_set.intersection(d2_domains)
    a = list(a_intersect)

    # b. domains that are present in both D2 and D3
    d2_set = set(d2_domains)
    b_intersect = d2_set.intersection(d3_domains)
    b = list(b_intersect)

    # c. domains that are present in both D1 and D3
    d3_set = set(d3_domains)
    c_intersect = d3_set.intersection(d1_domains)
    c = list(c_intersect)

    # d. domains that are present in all three datasets
    s1 = set(d1_domains) 
    s2 = set(d2_domains) 
    s3 = set(d3_domains) 
    # Calculates intersection of  
    # sets on s1 and s2 
    set1 = s1.intersection(s2) 
    # Calculates intersection of sets 
    # on set1 and s3 
    result_set = set1.intersection(s3) 
    # Converts resulting set to list 
    d = list(result_set) 


    # print(d)

    # write to file
    with open(AFILE, "w") as file:
        for i in a:
            file.write(f"{i}\n")

    with open(BFILE, "w") as file:
        for i in b:
            file.write(f"{i}\n")

    with open(CFILE, "w") as file:
        for i in c:
            file.write(f"{i}\n")

    with open(DFILE, "w") as file:
        for i in d:
            file.write(f"{i}\n")

if __name__ == "__main__":
    main()