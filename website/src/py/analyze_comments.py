# server should be started from the root directory of project using following line:
# python3 -m website.src.py.analyze_comments

from flask import Flask, jsonify
from flask_cors import CORS

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

    comments = fetch_comments(id=videoId, max_result=3000, max_len=1000)
    ind_model = 2
    embeddings = embed(model_name=embed_model_names[ind_model], sentences=comments)

    interias = []
    for n_clusters in range(1, 10):
        _, kmeans = clasterize('kmeans', embeddings, n_clusters=n_clusters)
        interias.append(kmeans.inertia_)

    choosed_n_clusters = 6
    clasters, kmeans = clasterize(
        method_name='kmeans', 
        embeddings=embeddings,
        n_clusters=choosed_n_clusters)

    claster_inds = {claster for claster in clasters}
    for ind in claster_inds:
        inds = clasters == ind
        comments_claster = [comment for comment, ind in zip(comments, inds) if ind]
        embeddings_claster = embeddings[inds]

        samples = sample(embeddings_claster, comments_claster, n_samples=5)

        result[f'claster_{ind}'] = {}
        for i in range(5):
            result[f'claster_{ind}'][f'comment_{i}'] = samples[i]

    result['result'] = ""
    for ind in claster_inds:
        inds = clasters == ind
        comments_claster = [comment for comment, ind in zip(comments, inds) if ind]
        embeddings_claster = embeddings[inds]

        result[f'description_{ind}'] = describe_claster(embeddings_claster, comments_claster)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
