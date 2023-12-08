from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, MeanShift
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA

methods = [
    'kmeans',
    'dbscan',
    'gaussian_mixture',
    'agglomerative',
    'mean_shift'
    # TODO: add more methods
]

def clasterize(method_name, embeddings, **kwargs):
    if method_name not in methods:
        raise ValueError(f'Invalid method name: {method_name}')
    
    if method_name == 'kmeans':
        if 'n_clusters' not in kwargs:
            kwargs['n_clusters'] = 5
        if 'n_init' not in kwargs:
            kwargs['n_init'] = 'auto'
        kmeans = KMeans(
            **kwargs
        ).fit(embeddings)
        return kmeans.predict(embeddings), kmeans
    elif method_name == 'dbscan':
        return DBSCAN(
            **kwargs
        ).fit_predict(embeddings)
    elif method_name == 'gaussian_mixture':
        if 'n_components' not in kwargs:
            kwargs['n_components'] = 5
        return GaussianMixture(
            **kwargs
        ).fit_predict(embeddings)
    elif method_name == 'agglomerative':
        if 'n_clusters' not in kwargs:
            kwargs['n_clusters'] = 5
        return AgglomerativeClustering(
            **kwargs
        ).fit_predict(embeddings)
    elif method_name == 'mean_shift':
        # PCA to reduce dimensionality
        pca = PCA(n_components=10)
        embeddings = pca.fit_transform(embeddings)
        return MeanShift(
            **kwargs
        ).fit_predict(embeddings)