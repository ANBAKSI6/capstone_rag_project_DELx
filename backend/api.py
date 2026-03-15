from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag_pipeline import classify_query, generate_answer

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/classify")
def classify(request: QueryRequest):
    result = classify_query(request.query)
    return {"classification": result}


@app.post("/answer")
def answer(request: QueryRequest):
    result = generate_answer(request.query)
    return {"answer": result}
