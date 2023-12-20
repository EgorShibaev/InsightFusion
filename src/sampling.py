import numpy as np
from scipy.stats import multivariate_normal
from tqdm.notebook import tqdm
from sklearn.decomposition import PCA


def sample_from_claster(embeddings, comments, n_samples=1, k=10):
    """
    Samples comments from a claster.
    :param embeddings: np.array of shape (n_samples, n_features)
    :param comments: list of comments
    :param n_samples: number of samples to take
    :param k: number of top samples to consider
    :return: list of comments
    """

    if n_samples > k:
        k = n_samples

    # find mean

    mean = np.mean(embeddings, axis=0)

    # top k by distance to mean

    top_k = np.argsort(np.linalg.norm(embeddings - mean, axis=1))[:k]

    # take random n_samples from top k

    samples = np.random.choice(top_k, size=n_samples)

    # return comments

    return [comments[i] for i in samples]