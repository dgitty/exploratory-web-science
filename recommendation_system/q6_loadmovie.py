import pandas as pd
from itertools import islice
import json
import csv
import re

def main():
    #  load u_item_movie
    import pandas as pd

    # header=['movie_id', 'movie_title', 'release_date', 'video_release_date','IMDb_URL' ,'unknown', 'Action' , 'Adventure' , 'Animation' , 'Childrens', 'Comedy' , 'Crime' , 'Documentary' , 'Drama' , 'Fantasy' , 'Film_Noir' , 'Horror' , 'Musical' , 'Mystery' , 'Romance' , 'Sci_Fi' , 'Thriller' , 'War' , 'Western']
    df = pd.read_csv("ml-100k/ml-100k/u.item", sep='|',engine='python', header=None)

    movie_list=""
    u_item_movie=dict()
    row=0
    while row< len(df):
        movie_list=movie_list+" "+df[1][row]
        u_item_movie[df[1][row]]={'movie_id':df[0][row], 
                                'movie_title':df[1][row], 
                                'release_date':df[2][row], 
                                'video_release_date':df[3][row],
                                'IMDb_URL':str(df[4][row]),
                                'unknown':df[5][row],
                                'Action':df[6][row],
                                'Adventure':df[7][row],
                                'Animation':df[8][row],
                                'Childrens':df[9][row],
                                'Comedy':df[10][row],
                                'Crime':df[11][row],
                                'Documentary':df[12][row],
                                'Drama':df[13][row],
                                'Fantasy':df[14][row],
                                'Film_Noir':df[15][row],
                                'Horror':df[16][row],
                                'Musical':df[17][row],
                                'Mystery':df[18][row],
                                'Romance':df[19][row],
                                'Sci_Fi':df[20][row],
                                'Thriller':df[21][row],
                                'War':df[22][row],
                                'Western':df[23][row]
                                }
        row+=1


    title_basic=dict()
    filename = open("../todaydataset/title_basics.tsv", "r", encoding='utf-8')
    line = filename.readline()
    while True:
        # Get next line from file
        line = filename.readline()
        # if line is empty then end of file is reached
        if not line:
            break

        line_info = line.rsplit('\t')
        print(line_info[0])

        title = line_info[2]

        movie_title_first=None
        if ',' in title:
            split_string = title.split(",", 1) #Split into "ab" and "cd"
            movie_title_first = split_string[0].strip()
        
        movie_title_second=None
        if '(' in title:
            split_string = title.split("(", 1) #Split into "ab" and "cd"
            movie_title_second = split_string[0].strip()

        movie_title_third=None
        movie_title_fourth=None
        if ':' in title:
            split_string = title.split(":", 1) #Split into "ab" and "cd"
            movie_title_third = split_string[0].strip()
            movie_title_fourth = split_string[1].strip()

        for k,v in u_item_movie.items():
            u_movie_year = str(['release_date']).rsplit('-', 1)[-1]
            # u_movie_year = re.search('\((.*)\)', k).group(1)
            # u_movie_first = k.split('(',1)
            if line_info[5] == u_movie_year and (line_info[2] in u_item_movie or line_info[3] in u_item_movie or (movie_title_first is not None and movie_title_first in movie_list) or (movie_title_second is not None and movie_title_second in movie_list) or (movie_title_third is not None and movie_title_third in movie_list) or  (movie_title_fourth is not None and movie_title_fourth in movie_list)):            
            # if line_info[2] in u_item_movie or line_info[3] in u_item_movie or (movie_title_first is not None and movie_title_first in movie_list) or (movie_title_second is not None and movie_title_second in movie_list) or (movie_title_third is not None and movie_title_third in movie_list) or  (movie_title_fourth is not None and movie_title_fourth in movie_list):            
                title_basic[line_info[0]]={'tconst':line_info[0], 
                                        'titleType':line_info[1], 
                                        'primaryTitle':line_info[2], 
                                        'originalTitle':line_info[3],
                                        'isAdult':line_info[4],
                                        'startYear':line_info[5],
                                        'endYear':line_info[6],
                                        'runtimeMinutes':line_info[7],
                                        'genres':line_info[8],
                                        }
                break

    # for k,v in u_item_movie.items():
    #     title = v['movie_title']

    #     movie_title_first=None
    #     if ',' in title:
    #         split_string = title.split(",", 1) #Split into "ab" and "cd"
    #         movie_title_first = split_string[0].strip()
        
    #     movie_title_second=None
    #     if '(' in title:
    #         split_string = title.split("(", 1) #Split into "ab" and "cd"
    #         movie_title_second = split_string[0].strip()

    #     movie_title_third=None
    #     movie_title_fourth=None
    #     if ':' in title:
    #         split_string = title.split(":", 1) #Split into "ab" and "cd"
    #         movie_title_third = split_string[0].strip()
    #         movie_title_fourth = split_string[1].strip()

    #     title_basic[line_info[0]]={'tconst':line_info[0], 
    #                                     'titleType':line_info[1], 
    #                                     'primaryTitle':line_info[2], 
    #                                     'originalTitle':line_info[3],
    #                                     'isAdult':line_info[4],
    #                                     'startYear':line_info[5],
    #                                     'endYear':line_info[6],
    #                                     'runtimeMinutes':line_info[7],
    #                                     'genres':line_info[8],
    #                                     }
    # # load title_basics
    # # tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres
    # # escapechar = ['\\','"']
    # df = pd.read_csv("todaydataset/title_basics.tsv", sep='\t', quoting=csv.QUOTE_NONE , engine='python', header=None,error_bad_lines=False)
    # # print(df)
    # title_basic=dict()
    # row=1
    # while row< len(df):
    #     print(f"tconst: {df[0][row]}")
    #     if df[2][row] in u_item_movie:
    #         title_basic[int(df[0][row])]={'tconst':df[0][row], 
    #                             'titleType':df[1][row], 
    #                             'primaryTitle':df[2][row], 
    #                             'originalTitle':df[3][row],
    #                             'isAdult':df[4][row],
    #                             'startYear':df[5][row],
    #                             'endYear':df[6][row],
    #                             'runtimeMinutes':df[7][row],
    #                             'genres':df[8][row],
    #                             }
    #     row+=1


    # load title_ratings
    df = pd.read_csv("../todaydataset/title_ratings.tsv", sep='\t',engine='python', header=None)
    # tconst	averageRating	numVotes
    title_ratings=dict()
    row=1
    while row< len(df):
        if df[0][row] in title_basic:
            title_ratings[df[0][row]]={'tconst':df[0][row], 
                                    'averageRating':float(df[1][row]), 
                                    'numVotes':int(df[2][row]),
                                    }
        row+=1

    rank_n_title = dict()
    movie_rank_title = dict()
    for k, v in title_ratings.items():
        rate_value = v['averageRating']
        num_vote = v['numVotes']
        rank_n_title[k] = {rate_value:num_vote}

        if rate_value not in movie_rank_title:
            movie_rank_title[rate_value] = dict()
            if k not in movie_rank_title[rate_value]:
                movie_rank_title[rate_value].update({k:num_vote})
        # rate:{movie:number of raters, movieb:number of raters}
        movie_rank_title[rate_value].update({k:num_vote})



    sorted_ordered_movies_title = dict()
    for k,v in movie_rank_title.items():
        ordered_movies =sorted(v.items(), key = lambda kv:(kv[1], kv[0]))
        sorted_ordered_movies_title[k]= ordered_movies

    # # count: movie:, num_rater:, rate:
    ranked_movies_title = dict()
    count=len(rank_n_title)
    for k in sorted(sorted_ordered_movies_title.keys()):
        for x in sorted_ordered_movies_title[k]:
            # ranked_movies_title[count] = {'tconst':x[0], 'numVotes':x[1],'averageRating':k }
            # if title_basic[x[0]]['primaryTitle'] in u_item_movie:
            ranked_movies_title[count] = {'tconst':x[0],'movie_title':title_basic[x[0]]['primaryTitle'], 'numVotes':x[1],'averageRating':k }
            count-=1
            print(title_basic[x[0]]['primaryTitle'])

    
    FILE="q6_ranked_movies_title.json"
    with open(FILE, "w") as file:
        json.dump(ranked_movies_title,file, indent=2)

    top_title = take(len(ranked_movies_title)-10,len(ranked_movies_title), ranked_movies_title.items())
    
    FILE="q6_ranked_movies_title_top.json"
    with open(FILE, "w") as file:
        json.dump(top_title,file, indent=2)

    bottom_title = take(0,10, ranked_movies_title.items())

    FILE="q6_ranked_movies_title_bottom.json"
    with open(FILE, "w") as file:
        json.dump(bottom_title,file, indent=2)

def take(n,m, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n, m))


if __name__ == "__main__":
    main()
