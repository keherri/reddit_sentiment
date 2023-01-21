import base64
import json
import os
import sys
from typing import List

import boto3

from reddit import Comment
from sentiment import get_sentiment

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

 
# Execute Lambda function 
def lambda_handler(event, context):
    # Comments from Kinesis
    comments = []
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        data_str = base64.b64decode(record['kinesis']['data'])
        data = json.loads(data_str)
        comments.append(
            Comment.from_dict(data)
        )

    # Get Sentiment Score and add comments to Reddit Crypto Table
    logger.info('Getting sentiment score')
    get_sentiment(comments)

    # Add comment to Reddit Crypto Table
    logger.info('Adding comments to Reddit Crypto Table')
    batch_write_to_table(comments)

    # Print 1st comment
    comm1 = comments[0]
    print(comm1.body[:50])
    print(comm1.sentiment, comm1.sentiment_score)
    print("-----------------------------------")
        

    # Finished   
    return {
        'statusCode': 200,
        'body': 'Success'
    }

    
def batch_write_to_table(comments: List[Comment]):
    # Connect to DyanmoDB
    db = boto3.resource('dynamodb')
    # Write items to the table in batches of 25
    comment_dicts = [comment.to_dict() for comment in comments]
    batch_size = 25 # Max batch size for DynamoDB batch_write_item
    for i in range(0, len(comment_dicts), batch_size):
        # Batch write items to DynamoDB table
        response = db.batch_write_item(
            RequestItems={
                'reddit-crypto-table': [
                    {'PutRequest': {'Item': item}} for item in comment_dicts[i : i+batch_size]
                ]
            }
        )