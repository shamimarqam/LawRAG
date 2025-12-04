import ollama
# rag_pipeline.py

import faiss
import json
from sentence_transformers import SentenceTransformer
from openai import OpenAI



INDEX_FILE = "legal_faiss.index"
METADATA_FILE = "legal_metadata.json"
EMBEDDING_MODEL = "BAAI/bge-large-en"  # Retrieval embeddings
# OPENAI_MODEL = "gpt-4o-mini"  # Or "gpt-4.1" if you have access

# Load FAISS + Metadata

print("Loading FAISS index & metadata...")
index = faiss.read_index(INDEX_FILE)
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load embedding model
embed_model = SentenceTransformer(EMBEDDING_MODEL)

# (e.g., in terminal: ollama serve, and ollama pull deepseek-r1:7b)

# --- Step 1: Set up the Ollama client ---
# client = ollama.Client()
# model_name = "deepseek-r1-distill-qwen:14b"

model_name = "llama3.1:8b"

def retrieve(query, top_k=5):
    query_embedding = embed_model.encode([query], normalize_embeddings=True)
    D, I = index.search(query_embedding, top_k)
    results = []
    for idx, score in zip(I[0], D[0]):
        results.append({
            "text": metadata[idx]["text"],
            "source": metadata[idx]["filename"],
            "score": float(score)
        })
    return results

# --- Step 2: Define your query and context ---
def rag_answer(query, top_k=5):
    # Step 1: Retrieve relevant chunks
    retrieved_docs = retrieve(query, top_k=top_k)
    context = "\n\n".join([doc["text"] for doc in retrieved_docs])

    # Step 2: Construct prompt
    prompt = f"""
You are a legal assistant. Answer the query. You can take help of the following case laws and bare act excerpts to answer the query.

Context:
{context}

Question: {query}

Answer as clearly and faithfully as possible, citing the source documents and Indian laws and Acts when useful.
    """

    # Step 3: Query LLM
    # try:
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful AI trained in Indian legal texts."},
            {"role": "user", "content": prompt}
        ],
        # temperature=0.2,  # lower = more factual
    )
    # except ollama.ResponseError as e:
    #     print(f"Error communicating with Ollama: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")

    return response['message']['content'], retrieved_docs


# --- Step 3: Get the response from the LLM ---
# response = client.chat(model=model_name, messages=messages)
# bot_response = response['message']['content']



if __name__ == "__main__":
    query = input("Enter query:\n")
    answer, docs = rag_answer(query, top_k=5)

    print("\n=== RAG Answer ===\n")
    print(answer)
    print("\n=== Sources ===\n")
    for d in docs:
        print(f"- {d['source']} (score {d['score']:.4f})")


