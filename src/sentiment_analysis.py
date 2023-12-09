import transformers
import numpy as np

model = transformers.AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
tokenizer = transformers.AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")


def one_comment_sentiment(comment: str) -> int:
    """
    Takes a comment and a model, returns a sentiment score: integer from 0 to 4
    """
    tokens = tokenizer.encode(comment, return_tensors="pt")
    result = model(tokens)
    return result.logits.argmax().item()\


def comments_sentiment(comments: list[str]) -> float:
    """
    Takes a list of comments and returns a sentiment score: float from 0 to 1
    """
    # take 50 random comments

    random_comments = np.random.choice(comments, size=50)

    # get sentiment for each comment

    sentiments = [one_comment_sentiment(comment) for comment in random_comments]

    # return mean sentiment

    return np.mean(sentiments) / 4
