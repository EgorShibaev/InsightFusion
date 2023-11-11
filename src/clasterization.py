

methods = [
    'kmeans',
    'dbscan',
    # TODO: add more methods
]

def clasterize(method_name, embeddings, **kwargs):
    if method_name not in methods:
        raise ValueError(f'Invalid method name: {method_name}')
    
    if method_name == 'kmeans':
        from sklearn.cluster import KMeans
        return KMeans(
            **kwargs
        ).fit_predict(embeddings)
    elif method_name == 'dbscan':
        from sklearn.cluster import DBSCAN
        return DBSCAN(
            **kwargs
        ).fit_predict(embeddings)
    else:
        pass