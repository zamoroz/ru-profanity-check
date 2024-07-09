import pkg_resources

import faiss
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np


class ProfanityChecker:
    def __init__(self, embeddings = None):
        if not embeddings:
            embeddings = pkg_resources.resource_filename('profanity_check', 'data/embeddings.txt')
        self.index = self.load_faiss_index(embeddings)

        model_path = pkg_resources.resource_filename('profanity_check','data/model')
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)


    def load_faiss_index(self, embeddings):
        embs = np.loadtxt(embeddings)
        index = faiss.IndexFlatIP(embs.shape[1])
        index.add(embs)
        return index


    def predict(self, text) -> float:
        t = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=300)
        with torch.no_grad():
            model_output = self.model(**{k: v.to(self.model.device) for k, v in t.items()})
        embeddings = torch.nn.functional.normalize(model_output.last_hidden_state[:, 0, :])
        query_emb = embeddings[0].cpu().numpy()
        D, I = self.index.search(query_emb.reshape(1, -1), 10)
        return max(D[0])
