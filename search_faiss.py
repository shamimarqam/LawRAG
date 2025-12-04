# search_faiss.py

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_FILE = "legal_faiss.index"
METADATA_FILE = "legal_metadata.json"
EMBEDDING_MODEL = "BAAI/bge-large-en"

# Load index + metadata
index = faiss.read_index(INDEX_FILE)
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

model = SentenceTransformer(EMBEDDING_MODEL)

# Search function
def search(query, top_k=5):
    query_embedding = model.encode([query], normalize_embeddings=True)
    D, I = index.search(query_embedding, top_k)  # Distances, Indices
    results = []
    for idx, score in zip(I[0], D[0]):
        results.append({
            "text": metadata[idx]["text"],
            "source": metadata[idx]["filename"],
            "score": float(score)
        })
    return results

# Example
if __name__ == "__main__":
    query = input("Enter query: ")
    # "What are the rules of land acquisition?"
    results = search(query)
    for r in results:
        print(f"[{r['score']:.4f}] {r['text'][:200]}...)\nSource: {r['source']}")
        # print(r['text'])