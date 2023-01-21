"""
Lambda triggered by API to return Reddit Sentiment data
"""

import datetime
from decimal import Decimal
import json
import os

import boto3
from boto3.dynamodb.conditions import Attr


DB = boto3.resource('dynamodb')

REDDIT_CRYPTO_TABLE = DB.Table('reddit-crypto-table')

def lambda_handler(event, context):
    current_time = datetime.datetime.now()
    begin_time = current_time - datetime.timedelta(minutes=10)
    # Get seconds from utc epoch
    seconds_from_epoch = Decimal(begin_time.timestamp())
    reddit_data = get_reddit_data(seconds_from_epoch)

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { "content-type": "application/json"},
        "body":  json.dumps(
            {
                "statusCode": 200,
                "results": reddit_data
            }
        )
    }    


def get_reddit_data(begin_time):
    reddit_scan = REDDIT_CRYPTO_TABLE.scan(
        FilterExpression=Attr("CreatedUtc").gt(begin_time),
    )
    reddit_data = reddit_scan['Items']
    
    while 'LastEvaluatedKey' in reddit_scan:
        reddit_scan = REDDIT_CRYPTO_TABLE.scan(
            FilterExpression=Attr("CreatedUtc").gt(begin_time),
            ExclusiveStartKey=reddit_scan['LastEvaluatedKey']
        )
        reddit_data.extend(reddit_scan['Items'])

    # Convert Decimal to float in prep for json.dumps
    for item in reddit_data:
        for key in ['CreatedUtc', 'SentimentScore']:
            item[key] = round(float(item[key]), 2)

    return reddit_data