import praw
import json
import os
from datetime import datetime

# Reddit API credentials
reddit = praw.Reddit(
    client_id="4Mqq1qhf9ugFLxACcpcK3w",
    client_secret="zueS3m_6nvrZJfaI04W31_IKXcVEiA",
    user_agent="fractal_geometry",
)

# Get a specific post by ID
submission = reddit.submission(id="1f3flud")  # Replace with an actual post ID. Normally found in the post URL

# Remove "Load More Comments"
submission.comments.replace_more(limit=None)  # Fetch all comments

# Get post creation time
post_timestamp = datetime.fromtimestamp(submission.created_utc)

# Function to recursively extract comments with timestamps
def extract_comments(comment, depth=0):
    comment_timestamp = datetime.fromtimestamp(comment.created_utc)

    return {
        "id": comment.id,
        "fullname": comment.fullname,
        "author": comment.author.name if comment.author else "Deleted",
        "author_fullname": getattr(comment, "author_fullname", None),

        "body": comment.body,
        "body_html": comment.body_html,

        "created_utc": comment.created_utc,
        "timestamp_utc": comment_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "edited": comment.edited,

        "score": comment.score,
        "likes": comment.likes,
        "controversiality": comment.controversiality,
        "gilded": comment.gilded,
        "total_awards_received": comment.total_awards_received,

        "stickied": comment.stickied,
        "locked": comment.locked,
        "collapsed": comment.collapsed,
        "is_submitter": comment.is_submitter,
        "distinguished": comment.distinguished,

        "saved": comment.saved,
        "permalink": comment.permalink,
        "parent_id": comment.parent_id,
        "link_id": comment.link_id,
        "subreddit": str(comment.subreddit),
        "subreddit_id": comment.subreddit_id,

        "depth": depth,

        "actions": {
            "upvote": {"action": "upvote", "target_id": comment.fullname},
            "downvote": {"action": "downvote", "target_id": comment.fullname},
            "save": {"action": "save", "target_id": comment.fullname},
            "report": {
                "action": "report",
                "target_id": comment.fullname,
                "reason": None
            },
            "award": {
                "action": "award",
                "target_id": comment.fullname,
                "award_type": None
            }
        },

        "replies": [
            extract_comments(reply, depth + 1)
            for reply in comment.replies
        ]
    }


# Extract structured comments
comment_data = [extract_comments(comment) for comment in submission.comments]

# Find the last comment timestamp
all_timestamps = []
def collect_timestamps(comment):
    all_timestamps.append(datetime.strptime(comment["timestamp"], "%Y-%m-%d %H:%M:%S"))
    for reply in comment["replies"]:
        collect_timestamps(reply)

for comment in comment_data:
    collect_timestamps(comment)

if all_timestamps:
    last_comment_time = max(all_timestamps)
    time_difference = last_comment_time - post_timestamp
else:
    last_comment_time = None
    time_difference = None

# Print results to the console
output_data = {
    "post": {
        "id": submission.id,
        "fullname": submission.fullname,
        "title": submission.title,
        "author": submission.author.name if submission.author else "Deleted",
        "subreddit": str(submission.subreddit),
        "subreddit_id": submission.subreddit_id,

        "selftext": submission.selftext,
        "url": submission.url,
        "permalink": submission.permalink,

        "score": submission.score,
        "upvote_ratio": submission.upvote_ratio,
        "num_comments": submission.num_comments,
        "locked": submission.locked,
        "stickied": submission.stickied,
        "over_18": submission.over_18,
        "spoiler": submission.spoiler,
        "distinguished": submission.distinguished,

        "created_utc": submission.created_utc,
        "post_timestamp_utc": post_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    },

    "comment_summary": {
        "last_comment_timestamp_utc": (
            last_comment_time.strftime("%Y-%m-%d %H:%M:%S")
            if last_comment_time else None
        ),
        "time_difference_seconds": (
            time_difference.total_seconds()
            if time_difference else None
        )
    },

    "comments": comment_data
}


# Create jason_data folder if it doesn't exist
os.makedirs("json_data", exist_ok=True)

# Save to file
# Always select which folder to insert data to
with open("json_data/post58lb_reddit_comments_with_time.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Reddit post and comments saved to json_data/post55lb_reddit_comments_with_time.json")