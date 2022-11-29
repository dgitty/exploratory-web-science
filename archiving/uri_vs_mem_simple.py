
URIMEM_FILE = "uri_vs_mem_simple.csv"
uri_vs_mem = dict()
uri_vs_mem = {0:962,
1:12,
8:1,
4:3,
226:1,
686:1,
100:3,
2:4,
7:1,
3:2,
6:2,
5:1,
474:1,
454:1,
24:1,
48:1,
23:1,
298:1,
20:1
}


# for i in range(4):
#     print("hi")

# log all uri and mem
with open(URIMEM_FILE, 'w') as urifile:
    urifile.write("memento,num_of_uri\n")
    for key in uri_vs_mem.keys():
        for _ in range(uri_vs_mem[key]):
            urifile.write("%s,%d\n"%(key,1))