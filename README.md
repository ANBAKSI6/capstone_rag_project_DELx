# Dell RAG Assistant (Capstone Project)

This project implements a Retrieval Augmented Generation (RAG) pipeline using:

- LangChain
- FAISS Vector Database
- Cohere Reranking
- AWS Credentials
- Streamlit Frontend

## Project Structure

capstone_rag_project/
│
├── data/                  # Add Dell PDFs here
├── vectorstore/           # FAISS index
├── backend/
│   ├── ingestion.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── rag_pipeline.py
│   └── config.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── .env

## Setup

Install dependencies

pip install -r requirements.txt

Add Dell PDFs inside data/

Create FAISS index

python backend/ingestion.py

Run UI

streamlit run frontend/app.py