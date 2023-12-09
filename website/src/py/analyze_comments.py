# server should be started from the root directory of project using following line:
# python3 -m website.src.py.analyze_comments

from flask import Flask, jsonify
from flask_cors import CORS
from collections import Counter

from src.clasterization import clasterize
from src.fetch_comments import fetch_comments
from src.embed import embed
from src.embed import model_names as embed_model_names
from src.sampling import sample_from_claster as sample
from src.describe_by_llm import describe_claster


app = Flask(__name__)
CORS(app)


@app.route('/analyze_comments/<videoId>', methods=['POST'])
def analyze_comments(videoId):
    result = {}

    choosed_n_clusters = 5
    choosed_n_comments = 6
    
    result['n_of_clusters'] = choosed_n_clusters
    result['n_of_samples'] = choosed_n_comments

    comments = fetch_comments(id=videoId, max_result=3000, max_len=1000)
    ind_model = 2
    embeddings = embed(model_name=embed_model_names[ind_model], sentences=comments)

    interias = []
    for n_clusters in range(1, 10):
        _, kmeans = clasterize('kmeans', embeddings, n_clusters=n_clusters)
        interias.append(kmeans.inertia_)

    clusters, kmeans = clasterize(
        method_name='kmeans', 
        embeddings=embeddings,
        n_clusters=choosed_n_clusters)
    
    counts = Counter(clusters)
    for cluster, count in counts.items():
        result[f'number_of_comments_{cluster}'] = count

    cluster_inds = {cluster for cluster in clusters}
    for ind in cluster_inds:
        inds = clusters == ind
        comments_cluster = [comment for comment, ind in zip(comments, inds) if ind]
        embeddings_cluster = embeddings[inds]

        samples = sample(embeddings_cluster, comments_cluster, n_samples=choosed_n_comments)

        result[f'cluster_{ind}'] = {}
        for i in range(choosed_n_comments):
            result[f'cluster_{ind}'][f'comment_{i}'] = samples[i]

    for ind in cluster_inds:
        inds = clusters == ind
        comments_cluster = [comment for comment, ind in zip(comments, inds) if ind]
        embeddings_cluster = embeddings[inds]

        result[f'description_{ind}'] = describe_claster(embeddings_cluster, comments_cluster)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
