# Land Dispute Legal Query RAG System

A Retrieval-Augmented Generation (RAG) pipeline designed to answer **Indian land-dispute–related legal queries** using structured legal documents (case laws, statutes, judgments).  
This repository includes preprocessing scripts, embedding & indexing utilities, and an inference pipeline for generating context-aware answers.

---

## Features

### 1. Legal Corpus Preparation
- Ingest raw documents: PDFs, text files, case summaries.
- Clean, normalize, and segment documents into retrieval-friendly chunks.
- Generate metadata: titles, case IDs, jurisdiction, year, sections involved.

### 2. Embedding & Indexing Engine
- Uses **BGE Large** / **Legal Embedding Models** to generate dense sentence embeddings.
- FAISS index for high-speed semantic retrieval.
- Supports incremental indexing.

### 3. RAG Pipeline
- Takes user query → retrieves top-k relevant legal texts → generates output using an LLM.
- Supports:
  - Direct answers
  - Summaries
  - Case-law comparisons
  - Citation-backed responses

### 4. Sample Legal Inputs
The repository includes **sample land dispute prompts**, e.g.:
- Boundary disputes  
- Encroachment  
- Government acquisition  
- Inheritance & partition  
- Title conflicts  
- Easement rights  
*(See `/samples/land_disputes.json`)*

## System Architecture
<img width="593" height="616" alt="image" src="https://github.com/user-attachments/assets/137775bc-bd02-4a14-bd6b-556e4e4f1932" />
