import praw #type: ignore
import json
import time
import extract_text as et

# Setup Reddit API connection
reddit = praw.Reddit('DEFAULT')

save_path = 'C:/Users/6gane/OneDrive/Desktop/New folder/archive all subjects/Summer 2024/Machine Learning 5369L/DL Projects/scam detection/scam-detection-in-real-time/images/image.jpg'

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
            "comments": get_top_comments_with_replies(post, limit=5),  # Get top 5 comments with replies
            "url": post.url,
            "image_text": []
        }

         # Check if the post contains images (single or gallery)
        if hasattr(post, "is_gallery"):
            # Loop through gallery images
            for item in post.gallery_data['items']:
                media_id = item['media_id']
                image_url = f"https://i.redd.it/{media_id}.jpg"
                
                # Download and extract text from each image
                et.download_image(image_url, save_path)
                extracted_text = et.extract_text_from_image(save_path)
                post_data['image_text'].append(extracted_text)

        # If the post is a single image
        elif post.url.endswith(('.jpg','.jpeg', '.png', '.gif')):
            et.download_image(post.url, save_path)
            extracted_text = et.extract_text_from_image(save_path)
            post_data['image_text'].append(extracted_text)

        # Print to track progress
        print(f"Processed post {post.id} with title: {post.title}")
        print("gallery: ", hasattr(post, 'is_gallery'))
        print("url", post.url)
        print('image_text', post_data['image_text'])
        posts_data.append(post_data)

        # Sleep to respect rate limits
        time.sleep(2)

    return posts_data

subreddit_list = ['scams', 'phishing']

for subreddit in subreddit_list:
    # Scrape data from r/scams, r/scambait subreddit
    data = scrape_subreddit(subreddit, limit=None)

    # Store data in a JSON file
    subreddit_json = subreddit + '.json'
    with open(subreddit_json, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data scraping completed and saved to {subreddit_json}")



