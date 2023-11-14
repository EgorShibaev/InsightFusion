from sentence_transformers import SentenceTransformer
import cohere
import numpy as np

model_names = [
    'SentenceTransformer/bert-base-nli-mean-tokens',
    'cohere'
    # TODO: add more models
]

cohere_key = 'oFd6NCO7dkVeFVPSXsANEzlT4OShQKGovZNhcszU' # this is trial key

def embed(model_name, sentences):
    if model_name not in model_names:
        raise ValueError(f'Invalid model name: {model_name}')
    
    match model_name:
        case 'SentenceTransformer/bert-base-nli-mean-tokens':
            model = SentenceTransformer('bert-base-nli-mean-tokens')
            return model.encode(sentences)
        case 'cohere':
            co = cohere.Client(cohere_key)
            embs = co.embed(sentences, input_type='clustering', model='embed-english-v3.0').embeddings
            return np.array(embs)
