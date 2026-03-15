import cohere
from backend.config import COHERE_API_KEY

co = cohere.Client(COHERE_API_KEY)

def rerank(query, documents):

    texts = [doc.page_content for doc in documents]

    response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=texts,
        top_n=3
    )

    ranked_docs = [documents[r.index] for r in response.results]
    return ranked_docs