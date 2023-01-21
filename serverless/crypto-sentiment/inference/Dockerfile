FROM public.ecr.aws/lambda/python:3.9

COPY app.py requirements.txt reddit.py sentiment.py ./
COPY distilbert_reddit_model ./distilbert_reddit_model
COPY distilbert_reddit_tokenizer ./distilbert_reddit_tokenizer
# COPY model /opt/ml/model

RUN python3.9 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
