from decimal import Decimal


class Comment:
    """
    A class representing a Reddit Comment
    """
    def __init__(self, comment_id: str, body: str, author: str, created_utc: float, subreddit: str):
        """
        Initialize a Comment object
        
        :param comment_id: the id of the comment
        :type comment_id: str
        :param body: the text of the comment
        :type body: str
        :param author: the author of the comment
        :type author: str
        :param created_utc: the timestamp of the comment in UTC
        :type created_utc: float
        :param subreddit: the subreddit the comment was posted in
        :type subreddit: str
        """
        self.comment_id = comment_id
        self.body = body
        self.author = author
        self.created_utc = created_utc
        self.subreddit = subreddit
        self.sentiment = None
        self.sentiment_score = None

    def to_dict(self):
        return {
            "CommentId": self.comment_id,
            "CommentText": self.body,
            "Author": self.author,
            "CreatedUtc": Decimal(self.created_utc),
            'Subreddit': self.subreddit,
            'Sentiment': self.sentiment,
            'SentimentScore': int(round(self.sentiment_score * 100))
        }

    @classmethod
    def from_dict(cls, comment_dict: dict):
        return cls(comment_dict['comment_id'], comment_dict['body'], comment_dict['author'], comment_dict['created_utc'], comment_dict['subreddit'])