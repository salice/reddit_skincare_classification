import numpy as np
import pandas as pd

import requests, json, time,datetime, sys, os, datetime
import praw

#function to connect and create the submission lists from 2 subreddits
def connect_and_subreddits(sub1, sub2):
    #start time counter to see how long it runs
    start_time = time.time()
    #connect to api
    
    creds_file = open("../creds.json", "r")
    reddit_creds = json.loads(creds_file.read())
    reddit = praw.Reddit(
    client_id=reddit_creds["id"],
    client_secret=reddit_creds["secret"],
    username=reddit_creds["user"],
    password=reddit_creds["pass"],
    user_agent="dsi")
    
    #check connection just in case
    
    if reddit.read_only == False:
        subreddit1 = reddit.subreddit(str(sub1))
        sub1_list = [i for i in subreddit1.new(limit=1000)]
        subreddit2 = reddit.subreddit(str(sub2))
        sub2_list = [j for j in subreddit2.new(limit=1000)]
        
        #build list of dictionaries
        
        sub1_outer = []
        for post in sub1_list:
            sub1_inner = {}
            sub1_inner["title"] = post.title
            sub1_inner["post"] = post.selftext
            sub1_inner["time_utc"] = post.created_utc
            sub1_inner["upvote"] = post.upvote_ratio
            sub1_inner["num_comments"] = post.num_comments
            
            sub1_outer.append(sub1_inner)
            
        sub1_df = pd.DataFrame(sub1_outer)
        
        sub2_outer = []
        for post in sub2_list:
            sub2_inner = {}
            sub2_inner["title"] = post.title
            sub2_inner["post"] = post.selftext
            sub2_inner["time_utc"] = post.created_utc
            sub2_inner["upvote"] = post.upvote_ratio
            sub2_inner["num_comments"] = post.num_comments
            
            sub2_outer.append(sub2_inner)
            
        sub2_df = pd.DataFrame(sub2_outer)
        
        #create folder using os and toss csvs in them
        time_for_file = str(time.localtime().tm_hour)+"-"+str(time.localtime().tm_mon)+"-"+str(time.localtime().tm_mday)
        
        sub1_df.to_csv("../data/scrape-"+time_for_file+"_asianbeauty.csv", index=False)
        sub2_df.to_csv("../data/scrape-"+time_for_file+"_skincareaddiction.csv", index=False)
        end_time = time.time()
        elapsed_time = (end_time - start_time) / 60
        print(f"Done! it took {elapsed_time} minutes")
    else:
        return "Connection Issue"

connect_and_subreddits(sub1="AsianBeauty", sub2="SkincareAddiction")