import numpy as np
from scipy.stats import multivariate_normal
from tqdm.notebook import tqdm
from sklearn.decomposition import PCA


def sample_from_claster(embeddings, comments, n_samples=1):
    """
    Samples comments from a claster.
    :param embeddings: np.array of shape (n_samples, n_features)
    :param comments: list of comments
    :param n_samples: number of samples to take
    :return: list of comments
    """

    # find mean

    mean = np.mean(embeddings, axis=0)

    # top 100 by distance to mean

    top_100 = np.argsort(np.linalg.norm(embeddings - mean, axis=1))[:100]

    # take random n_samples from top 100

    samples = np.random.choice(top_100, size=n_samples)

    # return comments

    return [comments[i] for i in samples]