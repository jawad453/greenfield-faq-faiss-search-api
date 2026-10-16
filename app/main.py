
import os
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

from search_faq import search_faq

app = FastAPI(title="GreenField Farmers FAQ API")

BASE_DIR = Path(__file__).resolve().parent.parent
FALLBACK_ANSWER = "We’ll get back to you shortly"

client = OpenAI() if os.getenv("OPENAI_API_KEY") else None


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "GreenField Farmers FAQ API is running"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        return {"question": question, "answer": FALLBACK_ANSWER}

    results = search_faq(question)

    if not results or results[0]["similarity_score"] < 0.45:
        return {"question": question, "answer": FALLBACK_ANSWER}

    if client is None:
        return {
            "question": question,
            "answer": results[0]["answer"],
            "sources": results[:3],
        }

    context = "\n".join(
        f"Q: {item['question']}\nA: {item['answer']}"
        for item in results
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the supplied "
                    "FAQ context. Do not invent policies, prices, or facts. "
                    f"If the context is insufficient, reply exactly: "
                    f"{FALLBACK_ANSWER}"
                ),
            },
            {
                "role": "user",
                "content": f"FAQ context:\n{context}\n\nQuestion: {question}",
            },
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content or FALLBACK_ANSWER

    return {
        "question": question,
        "answer": answer,
        "sources": results[:3],
    }
