import json
import asyncio
import os

import asyncpraw
import boto3

# Load credentials
if "REDDIT_CLIENT_ID" in os.environ:
    REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT")
    kinesis = boto3.client("kinesis")
else:
    # Load reddit_creds from file
    reddit_creds = json.loads(open(".reddit_config").read())
    REDDIT_CLIENT_ID = reddit_creds["client_id"]
    REDDIT_CLIENT_SECRET = reddit_creds["client_secret"]
    REDDIT_USER_AGENT = reddit_creds["user_agent"]

    # create Kinesis client
    kinesis = boto3.client("kinesis", region_name="us-east-1")

async def main():
    reddit = asyncpraw.Reddit(client_id=REDDIT_CLIENT_ID, 
                              client_secret=REDDIT_CLIENT_SECRET, 
                              user_agent=REDDIT_USER_AGENT)

    # Select subreddits
    channels = ["bitcoin", "cryptocurrency"]
    subreddits = [await reddit.subreddit(channel) for channel in channels]
    
    # asynchronously handle comments for each subreddit
    await asyncio.gather(*[handle_comments(subreddit) for subreddit in subreddits])


async def handle_comments(subreddit: asyncpraw.models.Subreddit):
    # stream comments from the subreddit and handle each comment
    async for comment in subreddit.stream.comments():
        print(comment.id)
        send_to_kinesis(comment)

        
def send_to_kinesis(comment: asyncpraw.models.Comment):
    # send comment data to the Kinesis stream
    kinesis.put_record(
        PartitionKey=comment.id,
        StreamName="reddit_comments", 
        Data=json.dumps(comment_to_dict(comment))
    )


def comment_to_dict(comment: asyncpraw.models.Comment):
    # convert comment object to a dictionary
    return {
        "comment_id": comment.id,
        "body": comment.body,
        "author": comment.author.name,
        "created_utc": comment.created_utc,
        "subreddit": comment.subreddit.display_name
    }


if __name__ == "__main__":
    asyncio.run(main())