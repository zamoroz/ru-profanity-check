import pkg_resources

import faiss
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np


model_path = pkg_resources.resource_filename('profanity_check','data/model')
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)


def embed_bert_cls(text, model, tokenizer):
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=300)
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()


def load_faiss_index():
    embs = np.loadtxt(pkg_resources.resource_filename('profanity_check', 'data/embeddings.txt'))
    index = faiss.IndexFlatIP(embs.shape[1])
    index.add(embs)
    return index


def predict(text) -> float:
    query_emb = embed_bert_cls(text, model, tokenizer)
    index = load_faiss_index()
    D, I = index.search(query_emb.reshape(1, -1), 10)
    return max(D[0])
