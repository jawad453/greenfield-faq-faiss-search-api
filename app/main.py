
import json
import os
from pathlib import Path

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

from search_faq import search_faq

app = FastAPI(title="GreenField Farmers FAQ API")

FALLBACK_ANSWER = "We\u2019ll get back to you shortly"

BASE_DIR = Path(__file__).resolve().parent.parent
FAQ_PATH = BASE_DIR / "faq.json"

with open(FAQ_PATH, "r", encoding="utf-8") as file:
    faq_data = json.load(file)

# Assign stable string IDs based on each FAQ's position.
faq_ids = {
    faq["question"]: str(index)
    for index, faq in enumerate(faq_data, start=1)
}

client = OpenAI() if os.getenv("OPENAI_API_KEY") else None


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "GreenField Farmers FAQ API is running"}


@app.post("/answer")
def answer_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        return {
            "answer": FALLBACK_ANSWER,
            "sources": [],
        }

    results = search_faq(question)

    if not results or results[0]["similarity_score"] < 0.45:
        return {
            "answer": FALLBACK_ANSWER,
            "sources": [],
        }

    # Return FAQ IDs, not complete FAQ objects.
    sources = [
        faq_ids[item["question"]]
        for item in results
        if item["question"] in faq_ids
    ]

    if client is None:
        return {
            "answer": results[0]["answer"],
            "sources": sources,
        }

    context = "\n\n".join(
        f"FAQ ID: {faq_ids.get(item['question'], '')}\n"
        f"Question: {item['question']}\n"
        f"Answer: {item['answer']}"
        for item in results
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the "
                    "provided FAQ context. Do not invent facts, "
                    "prices, or policies. If the context does not "
                    "answer the question, reply exactly: "
                    f"{FALLBACK_ANSWER}"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"FAQ context:\n{context}\n\n"
                    f"Question: {question}"
                ),
            },
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content or FALLBACK_ANSWER

    return {
        "answer": answer,
        "sources": sources,
    }
