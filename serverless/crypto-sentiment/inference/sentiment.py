from typing import List

import torch
from torch.utils.data import TensorDataset, DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from reddit import Comment


def get_sentiment(comments: List[Comment]):
    # Load model and tokenizer
    model = AutoModelForSequenceClassification.from_pretrained('distilbert_reddit_model')
    tokenizer = AutoTokenizer.from_pretrained('distilbert_reddit_tokenizer')

    # Tokenize the comment
    texts = [comm.body for comm in comments]
    encoded_inputs = tokenizer.batch_encode_plus(texts, return_tensors='pt', truncation=True, padding=True)

    # Create a TensorDataset with the encoded inputs
    input_data = encoded_inputs['input_ids']
    dataset = TensorDataset(input_data)

    # Create a DataLoader with a batch size
    batch_size = 20 # Your desired batch size
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    # Get the sentiment score    
    outputs = []
    with torch.no_grad():
        for batch in dataloader:
            output = model(*batch)
            outputs.append(output)
    
    logits = [l for o in outputs for l in o.logits]

    # Get the predicted class
    labels = {0: 'NEGATIVE', 1: 'POSITIVE'}
    for comm, lgs in zip(comments, logits):
        scores = torch.softmax(lgs, dim=-1)
        _, predicted_class = torch.max(scores, dim=-1)

        # Get the sentiment
        try:
            comm.sentiment = labels[predicted_class.item()]
            comm.sentiment_score = scores[predicted_class.item()].item()
        except:
            print(f'predicted_class: {predicted_class}')
            print(f'predicted_class.item(): {predicted_class.item()}')
            comm.sentiment = 'ERROR'
            comm.sentiment_score = 0.0