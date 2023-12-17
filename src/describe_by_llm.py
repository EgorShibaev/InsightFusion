import numpy as np
from scipy.stats import multivariate_normal
from tqdm.notebook import tqdm
from sklearn.decomposition import PCA
from openai import OpenAI


OPENAI_KEY = "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"

def describe_claster(embeddings, comments):
    """
    Takes top 100 comments by distance to mean and describes them.
    Description is done via openai's API.
    """

    mean = np.mean(embeddings, axis=0)

    top_100 = np.argsort(np.linalg.norm(embeddings - mean, axis=1))[:100]

    top_100_comments = [comments[i] for i in top_100]

    openai = OpenAI(api_key=OPENAI_KEY)

    system_prompt = "You will get a list of comments, find what is common - try to describe them in one sentence."
    user_prompt = "\n====================================\n".join(top_100_comments)

    completion = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    return completion.choices[0].message.content


