import pkg_resources

import faiss
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np


class ProfanityChecker:
    def __init__(self):
        model_path = pkg_resources.resource_filename('profanity_check','data/model')
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)


    def embed_bert_cls(self, text):
        t = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**{k: v.to(self.model.device) for k, v in t.items()})
        embeddings = torch.nn.functional.normalize(model_output.last_hidden_state[:, 0, :])
        return embeddings[0].cpu().numpy()


    def load_faiss_index(self, embeddings):
        embs = np.array(embeddings)
        index = faiss.IndexFlatIP(embs.shape[1])
        index.add(embs)
        return index


    def predict(self, text) -> float:
        index = self.load_faiss_index(self.embed_bert_cls([text]))
        result = []
        for word in open(pkg_resources.resource_filename("profanity_check", "data/words.txt")).read().split():
            query_emb = self.embed_bert_cls(word)
            D, I = index.search(query_emb.reshape(1, -1), 10)
            result.append(max(D[0]))
        return max(result)
