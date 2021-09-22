import time
import json
import praw
import requests

from pathlib import Path
from tqdm import tqdm
import datetime as dt
import pandas as pd

# setup praw
with open('config.json', 'r') as f:
    config = json.load(f)
    
reddit = praw.Reddit(
    client_id= config['client_id'],
    client_secret = config['client_secret'],
    user_agent = config['user_agent']
)

# setup lists for data
bots = []

# unique values
comment_id_set = set()
post_id_set = set()

def bot_details(bot):
    return {
        "bot_id": bot.id,
        "bot_name": bot.name,
        "comment_karma": bot.comment_karma,
        "awardee_karma": bot.awardee_karma,
        "total_karma": bot.total_karma,
        "bot_created": dt.datetime.fromtimestamp(bot.created_utc)
    }

def collect_comment(comment):
    return {
        "submission_id": comment.submission.id,
        "comment_id": comment.id,
        "bot_id": comment.author,
        "comment_datetime": dt.datetime.fromtimestamp(comment.created_utc),
        "body_html": comment.body_html,
        "body_string": comment.body,
        "comment_ups": comment.ups,
        "comment_downs": comment.downs,
        "comment_awards": comment.total_awards_received
    }

def post_details(post):
    # if already collected return empty dict otherwise add to set
    if (post.id in post_id_set) or (post == None) :
        return {}
    else: 
        post_id_set.add(post.id)

    # if a post was deleted author is blank
    if post.author == None:
        author_id = None
    else:
        try: author_id = post.author.id
        except: author_id = None
    
    return {
        "post_id": post.id,
        "author_id": author_id,
        "author_name": post.author,
        "subreddit": post.subreddit,
        "subreddit_type": post.subreddit_type,
        "nsfw_post": post.over_18,
        "oc_post": post.is_original_content,
        "post_title": post.title,
        "post_awards": post.total_awards_received,
        "post_comments": post.num_comments,
        "post_upvote_ratio": post.upvote_ratio,
        "post_ups": post.ups,
        "post_downs": post.downs,
        "post_datetime": dt.datetime.fromtimestamp(post.created_utc) 
    }

def get_comment_ids(bot):
    """ collects all comments of a user from pushshift api
    input:
        bot (reddit account name)

    output:
        list of comment ids
    """
    api_url = 'https://api.pushshift.io/reddit/comment/search?html_decode=true'
    url = f'{api_url}&author={bot.name}&size=10000'
    
    comment_ids = []
    comments = requests.get(url).json()['data']
    while (len(comments) > 1):
        for comment in comments:
            if comment['id'] in comment_id_set:
                continue
            else:
                comment_id_set.add(comment['id'])

            comment_ids.append(comment['id'])
            print(f"comment_ids: {len(comment_ids)}", end='\r')
        
        time.sleep(1) # wait then continue to next search
        next_page = f'{url}&before={comments[-1]["created_utc"] + 1}'
        comments = requests.get(next_page).json()['data'] 

    return comment_ids

def save_file(data_list, file_path):
    df = pd.DataFrame(data_list)
    if not Path(file_path).exists():
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

def load_ids(bot, query):
    if query == 'reddit':
        top_comments = bot.comments.top(limit=None)
        new_comments = bot.comments.new(limit=None)

        comment_ids = []
        [comment_ids.append(x.id) for x in top_comments]
        [comment_ids.append(x.id) for x in new_comments]

        with open('./data/raw/praw_ids.txt', 'w') as f:
            f.writelines('\n'.join(comment_ids))

        print('num_comments', len(comment_ids))
        return comment_ids

    if query == 'pushshift':
        comment_ids = get_comment_ids(bot)
        with open('./data/raw/comment_ids.txt', 'w') as f:
            f.writelines('\n'.join(comment_ids))

        return comment_ids

    if query == 'load':
        with open('./data/raw/comment_ids.txt', 'r') as f:
            comment_ids = f.read().splitlines()

        return comment_ids

if __name__ == '__main__':

    # get sodogetip bot
    bot = reddit.redditor("sodogetip")
    bots.append(bot_details(bot))

    comment_ids = load_ids(bot, 'reddit')
    collected = pd.read_csv('./data/raw/comments.csv')['comment_id'].tolist()
    comment_ids = [x for x in comment_ids if x not in collected]

    for idx in tqdm(comment_ids):
        comments, posts = [], []
        comment = reddit.comment(idx)

        try: comment.submission
        except: continue

        comments.append(collect_comment(comment))
        posts.append(post_details(comment.submission))

        save_file(posts, './data/raw/posts.csv')
        save_file(comments, './data/raw/comments.csv')


    # combine dataframes & save
    pd.DataFrame(bots).to_csv('./data/raw/bots.csv', index=False)