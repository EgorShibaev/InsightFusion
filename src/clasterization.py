from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture

methods = [
    'kmeans',
    'dbscan',
    'gaussian_mixture'
    # TODO: add more methods
]

def clasterize(method_name, embeddings, **kwargs):
    if method_name not in methods:
        raise ValueError(f'Invalid method name: {method_name}')
    
    if method_name == 'kmeans':
        return KMeans(
            **kwargs
        ).fit_predict(embeddings)
    elif method_name == 'dbscan':
        return DBSCAN(
            **kwargs
        ).fit_predict(embeddings)
    elif method_name == 'gaussian_mixture':
        return GaussianMixture(
            **kwargs
        ).fit_predict(embeddings)