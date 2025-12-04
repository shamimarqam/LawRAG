# embed_store.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------
# Config
# -----------------------
CHUNKS_FILE = "../data/legal_chunks.json"   # Input JSON file
INDEX_FILE = "legal_faiss.index"    # Output FAISS index file
EMBEDDING_MODEL = "BAAI/bge-large-en"  

# -----------------------
# Load Chunks
# -----------------------
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = [d["text"] for d in data]

print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE}")

# -----------------------
# Load Model
# -----------------------
print(f"Loading embedding model: {EMBEDDING_MODEL}")
model = SentenceTransformer(EMBEDDING_MODEL)

# -----------------------
# Generate Embeddings
# -----------------------
print("Generating embeddings...")
embeddings = model.encode(chunks, batch_size=32, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

print(f"Generated embeddings with shape: {embeddings.shape}")

# -----------------------
# Build FAISS Index
# -----------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine similarity if normalized)
index.add(embeddings)

print(f"FAISS index built with {index.ntotal} vectors")

# -----------------------
# Save Index + Metadata
# -----------------------
faiss.write_index(index, INDEX_FILE)

# Save metadata (so we can map search results back to text)
with open("legal_metadata.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Saved FAISS index to {INDEX_FILE} and metadata to legal_metadata.json")