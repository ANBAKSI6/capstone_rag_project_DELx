# from backend.retriever import get_retriever
# from backend.reranker import rerank

# def generate_answer(query):

#     retriever = get_retriever()
#     docs = retriever.invoke(query)

#     reranked_docs = rerank(query, docs)

#     context = " ".join([
#         doc.page_content.strip().replace("\n", " ")[:300]
#         for doc in reranked_docs
#     ])

#     answer = f"""
# Based on the Dell documentation:

# {context}
# """

#     return answer

# from backend.retriever import get_retriever
# from backend.reranker import rerank


# def generate_answer(query):

#     retriever = get_retriever()

#     # retrieve documents
#     docs = retriever.invoke(query)

#     # rerank documents
#     reranked_docs = rerank(query, docs)

#     # take only the best document
#     best_doc = reranked_docs[0].page_content

#     # clean formatting
#     clean_text = best_doc.replace("\n", " ").strip()

#     return f"Answer:\n{clean_text}"

# from backend.retriever import get_retriever
# from backend.reranker import rerank
# import re


# def generate_answer(query):

#     retriever = get_retriever()
#     docs = retriever.invoke(query)

#     reranked_docs = rerank(query, docs)

#     # Take best document
#     best_doc = reranked_docs[0].page_content

#     # Clean formatting
#     text = best_doc.replace("\n", " ")
#     text = re.sub(r'\s+', ' ', text)

#     # Remove table-like junk
#     text = text.split("Table")[0]

#     # Keep answer short
#     answer = text[:300]

#     return f"Answer:\n{answer}"

# from backend.retriever import get_retriever
# from backend.reranker import rerank
# import cohere
# import os
# from dotenv import load_dotenv

# # load .env file
# load_dotenv()

# # read API key
# cohere_api_key = os.getenv("COHERE_API_KEY")

# # initialize client
# co = cohere.Client(cohere_api_key)


# def generate_answer(query):

#     retriever = get_retriever()
#     docs = retriever.invoke(query)

#     reranked_docs = rerank(query, docs)

#     context = "\n".join([doc.page_content for doc in reranked_docs])

#     prompt = f"""
# You are a Dell documentation assistant.

# Answer the question using the provided context.

# Context:
# {context}

# Question:
# {query}

# Answer in 2-3 sentences.
# """

#     response = co.generate(
#         model="command",
#         prompt=prompt,
#         max_tokens=150
#     )

#     return response.generations[0].text.strip()

# from typer import prompt

# from backend.retriever import get_retriever
# from backend.reranker import rerank
# import cohere
# import os
# from dotenv import load_dotenv

# # load .env file
# load_dotenv()

# # read API key
# cohere_api_key = os.getenv("COHERE_API_KEY")

# # initialize client
# co = cohere.Client(cohere_api_key)


# def generate_answer(query):

#     retriever = get_retriever()
#     docs = retriever.invoke(query)

#     reranked_docs = rerank(query, docs)

#     context = "\n".join([doc.page_content for doc in reranked_docs])

#     prompt = f"""
# You are a Dell documentation assistant.

# Answer the question using the provided context.

# Context:
# {context}

# Question:
# {query}

# Answer in 2-3 sentences.
# """

#     # NEW API
# response = co.chat(
#     model="command",
#     message=prompt,
#     max_tokens=150
# )

# return response.text.strip()

# from backend.retriever import get_retriever
# from backend.reranker import rerank
# import cohere
# import os
# from dotenv import load_dotenv

# load_dotenv()

# co = cohere.Client(os.getenv("COHERE_API_KEY"))


# def generate_answer(query):

#     retriever = get_retriever()
#     docs = retriever.invoke(query)

#     reranked_docs = rerank(query, docs)

#     context = "\n".join([doc.page_content for doc in reranked_docs])

#     prompt = f"""
# You are a Dell documentation assistant.

# Answer the question using the provided context.

# Context:
# {context}

# Question:
# {query}

# Answer in 2-3 sentences.
# """

#     response = co.chat(
#         model="command",
#         message=prompt,
#         max_tokens=150
#     )

#     return response.text.strip()

from backend.retriever import get_retriever
from backend.reranker import rerank
import cohere
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))


# -------------------------------
# QUERY CLASSIFICATION
# -------------------------------
def classify_query(query):

    classification_prompt = f"""
Classify the user query into one of these categories:

1. information → asking about specifications, features, ports, RAM, storage, camera, processor etc.
2. recommendation → asking for suggestions, best laptops, cheap laptops, comparison etc.
3. out_of_scope → not related to Dell laptops.

Return ONLY one word:
information
recommendation
out_of_scope

Query: {query}
"""

    response = co.chat(
        model="command-r-plus-08-2024",
        message=classification_prompt
    )

    return response.text.strip().lower()


# -------------------------------
# MAIN RAG FUNCTION
# -------------------------------
def generate_answer(query):

    # Step 1 — classify the query
    query_type = classify_query(query)

    # Step 2 — handle out of scope
    if query_type == "out_of_scope":
        return "This assistant can only answer questions related to Dell laptop documentation."

    # Step 3 — retrieve documents
    retriever = get_retriever()
    docs = retriever.invoke(query)

    # Step 4 — rerank documents
    reranked_docs = rerank(query, docs)

    # Step 5 — build context
    context = "\n".join([doc.page_content for doc in reranked_docs])

    # -------------------------------
    # INFORMATION QUERY
    # -------------------------------
    if query_type == "information":

        prompt = f"""
You are a Dell laptop documentation assistant.

Use the provided context to answer the user's question.

Rules:
- Provide a clear and short answer
- Maximum 3-5 sentences
- Do not repeat the context text

Context:
{context}

Question:
{query}

Answer:
"""

    # -------------------------------
    # RECOMMENDATION QUERY
    # -------------------------------
    elif query_type == "recommendation":

        prompt = f"""
You are a Dell laptop advisor.

From the context identify relevant Dell laptop models.

Rules:
- Return laptop names only
- Use bullet points
- Do not include explanations

Context:
{context}

Question:
{query}

Answer:
"""

    # Step 6 — generate answer
    response = co.chat(
        model="command-r-plus-08-2024",
        message=prompt
    )

    return response.text.strip()