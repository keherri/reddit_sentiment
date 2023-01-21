# Reddit Cryptocurrency Sentiment Classifier

**Objective**

Build a crypto Reddit comment sentiment classifier available via a basic REST API.

**Goals**
- 10m comments a day
- Streaming / real time predictions
- Budget of less than $100/month

## Set up
- Install Serverless Application Management (SAM) CLI [(install instructions)](!https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Use the instructions in `serverless/crypto-sentiment/README.md` to build your CloudFormation
- The CloudFormation has been successfully build, use the `activate_reddit_stream.ipynb` notebook to start the stream and make requests to the API.

To set up the pipeline, navigate to `serverless/crypto-sentiment`. In the `README.md` you'll see instructions in using


## Infrastructure

**Amazon EC2** - server to use the `asyncpraw` python package to stream Reddit cryptocurrency comments.

**Amazon Kinesis** - collect and process data streams in real-time.

**Amazon Lambda** - host our sentiment classifier model.

**Amazon DynamoDB** - store classified comments.

**API Gateway** - host our REST API that returns the last 10 minutes of Reddit cryptocurrency comments to the customer.

**Amazon Cloudwatch** - will be used to monitor the pipeline

## Model
**Fine-tuned distilbert-base-cased**
Distilbert was chosen as the model to finetune do to its relatively small size, but equal performance, compared to bert-base-cased.
* Model resulted in a 92% accuracy with a 80/20 training/test split.

You can run the model in the `distilbert_model_training.ipynb` notebook

## Rest API
The resulting API will return Reddit cryptocurrency comments from the past 10 minutes with the predicted sentiment.

## Reddit Stream
The server for the Reddit stream can be `activate_reddit_stream.ipynb` notebook. Make sure to go through the full `sam build` and `sam deploy` process in the `serverless/crypto-sentiment/` folder first though