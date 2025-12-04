# # chunking_with_tokens.py
# import json
# import tiktoken
# from nltk.tokenize import sent_tokenize

# # Load data
# with open("../data/legal_data.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# # Use OpenAI's cl100k_base tokenizer (works for most embedding models)
# tokenizer = tiktoken.get_encoding("cl100k_base")

# def count_tokens(text):
#     return len(tokenizer.encode(text, disallowed_special=()))

# def chunk_text_token_based(text, chunk_size=800, chunk_overlap=100):
#     sentences = sent_tokenize(text)
#     chunks, current_chunk = [], []
#     current_tokens = 0

#     for sent in sentences:
#         sent_tokens = count_tokens(sent)

#         # If single sentence itself is bigger than chunk_size
#         if sent_tokens > chunk_size:
#             # break it into smaller pieces by token length
#             words = sent.split()
#             partial = []
#             partial_tokens = 0
#             for w in words:
#                 w_tokens = count_tokens(w + " ")
#                 if partial_tokens + w_tokens > chunk_size:
#                     chunks.append(" ".join(partial))
#                     partial = [w]
#                     partial_tokens = w_tokens
#                 else:
#                     partial.append(w)
#                     partial_tokens += w_tokens
#             if partial:
#                 chunks.append(" ".join(partial))
#             continue

#         # If adding this sentence exceeds chunk_size → save current chunk
#         if current_tokens + sent_tokens > chunk_size:
#             chunks.append(" ".join(current_chunk))

#             # Handle overlap by keeping last few tokens
#             overlap_tokens = 0
#             overlap_sentences = []
#             for s in reversed(current_chunk):
#                 overlap_tokens += count_tokens(s)
#                 overlap_sentences.insert(0, s)
#                 if overlap_tokens >= chunk_overlap:
#                     break
#             current_chunk = overlap_sentences
#             current_tokens = sum(count_tokens(s) for s in current_chunk)

#         # Add sentence to current chunk
#         current_chunk.append(sent)
#         current_tokens += sent_tokens

#     if current_chunk:
#         chunks.append(" ".join(current_chunk))

#     return chunks

# # Process each doc
# chunked_data = []
# for doc in data:
#     chunks = chunk_text_token_based(doc["content"], chunk_size=500, chunk_overlap=50)
#     for i, chunk in enumerate(chunks):
#         chunked_data.append({
#             "doc_id": doc["file_name"],
#             "chunk_id": i,
#             "text": chunk
#         })

# # Save chunked data
# with open("legal_chunks.json", "w", encoding="utf-8") as f:
#     json.dump(chunked_data, f, indent=2, ensure_ascii=False)

# print("Token-based chunking complete! Saved as legal_chunks.json")

import json
import re
import nltk

nltk.download("punkt")

# --------------------------
# 1. Clean noisy characters
# --------------------------
def clean_text(text: str) -> str:
    # Remove non-printable and random junk
    text = re.sub(r"[^a-zA-Z0-9.,;:'\"()\-–\n\s]", " ", text)

    # Replace multiple spaces/newlines with single space
    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------
# 2. Word-level chunking
# --------------------------
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += chunk_size - overlap  # shift window forward

    return chunks


# --------------------------
# 3. Load JSON, clean & chunk
# --------------------------
with open("../data/legal_data.json", "r") as f:
    data = json.load(f)

chunked_data = []

for doc in data:
    cleaned_text = clean_text(doc["content"])
    chunks = chunk_text(cleaned_text)

    for i, chunk in enumerate(chunks):
        chunked_data.append({
            "filename": doc["file_name"],
            "chunk_id": i,
            "text": chunk
        })

# --------------------------
# 4. Save chunks for FAISS
# --------------------------
with open("legal_chunks.json", "w") as f:
    json.dump(chunked_data, f, indent=2)

print(f"Processed {len(data)} documents into {len(chunked_data)} chunks.")