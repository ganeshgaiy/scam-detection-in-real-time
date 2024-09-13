import praw #type: ignore
#  Praw is reddit's official api wrapper
import pandas as pd #type: ignore
import time
import json
# from dotenv import load_dotenv #type: ignore


#fetch subreddit posts count
def post_count(subreddit):
    #initialize post count
    pos = 0

    batch_size = 100
    rate_limit_per_min = 100
    delay_between_batches = 60/rate_limit_per_min

    for submission in subreddit.top(limit=None):
        pos+=1
        if pos%batch_size == 0:
            print(f"Processed {pos} posts so far...")
            time.sleep(delay_between_batches)
    return pos

# Function to get comments and replies recursively
def get_comment_data(comment):
    comment_data = {
        "comment_id": comment.id,
        "parent_id": comment.parent_id,
        "comment_text": comment.body,
        "upvotes": comment.score,
        "created_utc": comment.created_utc,
        "replies": []
    }

    # Recursively get replies (if any)
    if hasattr(comment, 'replies') and len(comment.replies) > 0:
        for reply in comment.replies:
            if isinstance(reply, praw.models.Comment):
                comment_data['replies'].append(get_comment_data(reply))

    return comment_data

def scrape_subreddit(subreddit_name, limit):
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    for post in subreddit.top(limit=limit):
        print("this is post", post)
        post_data = {
            "post_id": post.id,
            "title": post.title,
            "selftext": post.selftext,
            "flair": post.link_flair_text,
            "upvotes": post.score,
            "created_utc": post.created_utc,
            "comments": []
        }
        # print("post data is", post_data)
        # Get comments for the post
        post.comments.replace_more(limit=5)  # Load all comments
        for comment in post.comments.list():
            post_data['comments'].append(get_comment_data(comment))

        posts_data.append(post_data)
        print("post data is:\n", posts_data)
        # Sleep to respect rate limits
        time.sleep(2)

    return posts_data


# Initialize the Reddit instance using the credentials from praw.ini
reddit = praw.Reddit('DEFAULT')

# verifying the connection
print(reddit.read_only)

#subreddit r/Scams, r/fraud, r/Phishing

r_scams = reddit.subreddit("scams")
r_fraud = reddit.subreddit("fraud")
r_phishing = reddit.subreddit("phishing")

# for post in r_scams.top(limit=10):
#     print(post.title)

#scraping data 
'''
Posts:
    Title, post body, submission date, Flair
Comments:
    comment text, upvotes/downvotes, reply chains
Meta data:
    upvotes/downvotes for the post, timestamps, author karma(?)
'''
data = scrape_subreddit('scams', limit=1)

# Store data in a JSON file
with open('scams_data.json', 'w') as f:
    json.dump(data, f, indent=4)

# fetch top 1500 posts, titles and posts comments

