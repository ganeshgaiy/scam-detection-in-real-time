import praw #type: ignore
import json
import time

# Setup Reddit API connection
reddit = praw.Reddit('DEFAULT')

# Function to get top 5 replies for a comment
def get_top_replies(comment, limit=5):
    replies_data = []
    comment.replies.replace_more(limit=0)  # Remove MoreComments placeholders

    # Fetch replies and sort by upvotes
    replies = [reply for reply in comment.replies if isinstance(reply, praw.models.Comment)]
    sorted_replies = sorted(replies, key=lambda x: x.score, reverse=True)

    for reply in sorted_replies[:limit]:
        reply_data = {
            "comment_id": reply.id,
            "parent_id": reply.parent_id,
            "comment_text": reply.body,
            "upvotes": reply.score,
            "created_utc": reply.created_utc,
            # You can add more fields if necessary
        }
        replies_data.append(reply_data)
    return replies_data

# Function to get top 5 comments and their top 5 replies
def get_top_comments_with_replies(post, limit=5):
    comments_data = []

    post.comments.replace_more(limit=0)  # Remove MoreComments placeholders

    # Fetch comments and sort by upvotes
    comments = [comment for comment in post.comments if isinstance(comment, praw.models.Comment)]
    sorted_comments = sorted(comments, key=lambda x: x.score, reverse=True)

    for comment in sorted_comments[:limit]:
        comment_data = {
            "comment_id": comment.id,
            "parent_id": comment.parent_id,
            "comment_text": comment.body,
            "upvotes": comment.score,
            "created_utc": comment.created_utc,
            "replies": get_top_replies(comment, limit=5)  # Get top 5 replies
        }
        comments_data.append(comment_data)
    return comments_data

# Function to scrape posts
def scrape_subreddit(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    for post in subreddit.top(limit=limit):
        post_data = {
            "post_id": post.id,
            "title": post.title,
            "selftext": post.selftext,
            "flair": post.link_flair_text,
            "upvotes": post.score,
            "created_utc": post.created_utc,
            "comments": get_top_comments_with_replies(post, limit=5)  # Get top 5 comments with replies
        }

        posts_data.append(post_data)

        # Sleep to respect rate limits
        time.sleep(2)

    return posts_data

# Scrape data from r/scams subreddit
data = scrape_subreddit('scams', limit=None)

# Store data in a JSON file
with open('scams_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data scraping completed and saved to scams_data.json.")
