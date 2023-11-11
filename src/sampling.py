import numpy as np
from scipy.stats import multivariate_normal
from tqdm.notebook import tqdm
from sklearn.decomposition import PCA


def sample_from_claster(embeddings, comments, n_samples=1, components_PCA=10):
    """
    PCA to reduce dimensionality of embeddings.
    Consider projections as gaussian distribution.
    Sample from given claster n_samples points with according distribution.
    :param embeddings: np.array of shape (n_samples, n_features)
    :param comments: list of comments
    :param n_samples: number of samples to take
    :return: list of comments
    """

    proj = PCA(n_components=components_PCA).fit_transform(embeddings)
    # fit gaussian distribution
    mean = np.mean(proj, axis=0)
    covarieance = np.cov(proj, rowvar=False)

    # give probability to each embedding
    probabilities = multivariate_normal.pdf(proj, mean=mean, cov=covarieance)

    # normalize probabilities
    probabilities /= np.sum(probabilities)

    # sample from distribution
    indices = np.random.choice(
        range(len(embeddings)),
        size=n_samples,
        p=probabilities
    )

    return [comments[i] for i in indices]