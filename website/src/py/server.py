# server should be started from the root directory of project using following line:
# python3 -m website.src.py.server

from flask import Flask, jsonify
from flask_cors import CORS
from collections import Counter
import json

from src.clasterization import clasterize
from src.fetch_from_youtube import fetch_comments, fetch_stats
from src.embed import embed
from src.embed import model_names as embed_model_names
from src.sampling import sample_from_claster as sample
from src.describe_by_llm import describe_claster


app = Flask(__name__)
CORS(app)


@app.route('/analyze_comments/<videoId>', methods=['POST'])
def analyze_comments(videoId):
    # Stub
    # return jsonify(json.loads(open("website/src/py/stub_json.txt", "r").read()))

    result = {}

    choosed_n_clusters = 5
    choosed_n_comments = 6
    comments_to_analyze = 500
    
    result['n_of_clusters'] = choosed_n_clusters
    result['n_of_samples'] = choosed_n_comments

    comments = fetch_comments(id=videoId, max_result=comments_to_analyze, max_len=250)
    ind_model = 2
    embeddings = embed(model_name=embed_model_names[ind_model], sentences=comments)

    clusters, kmeans = clasterize(
        method_name='kmeans', 
        embeddings=embeddings,
        n_clusters=choosed_n_clusters)
    
    counts = Counter(clusters)
    for cluster, count in counts.items():
        result[f'number_of_comments_{cluster}'] = str((count * 100) // len(comments)) + "%"

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


@app.route('/get_stats/<videoId>', methods=['POST'])
def get_stats(videoId):
    result = fetch_stats(videoId)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
