import scipy.stats as stats
import csv

RANK_FILE="rank.csv"
RANK_FILE2="q4_rank.csv"
TAU_FILE="kendall_taub.csv"

def main():

    x1=list()
    x2=list()

    # read in rank.csv from q2
    with open(RANK_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row['TF-IDF'], row['TF'])
            x1.append(row['TF-IDF'])

    # read in q4_rank.csv from q4
    with open(RANK_FILE2, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row['TF-IDF'], row['TF'])
            x2.append(row['TF-IDF'])

    print(x1)
    print(x2)



    # x1 = [12, 2, 1, 12, 2]
    # x2 = [1, 4, 7, 1, 0]
    tau, p_value = stats.kendalltau(x1, x2)

    # write file
    with open(TAU_FILE, 'w') as f:
        f.write("tau-b, p\n%f,%f\n"%(tau, p_value))


if __name__ == "__main__":
    main()