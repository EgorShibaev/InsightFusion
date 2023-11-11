from sentence_transformers import SentenceTransformer

model_names = [
    'SentenceTransformer/bert-base-nli-mean-tokens',
    # TODO: add more models
]


def get_model(model_name):
    if model_name not in model_names:
        raise ValueError(f'Invalid model name: {model_name}')
    
    if model_name == 'SentenceTransformer/bert-base-nli-mean-tokens':
        return SentenceTransformer('bert-base-nli-mean-tokens')
    else:
        pass


def embed(model_name, sentences):
    model = get_model(model_name)
    return model.encode(sentences)