import os
from mistralai import Mistral

client = Mistral(api_key=os.getenv("MIS_API"))
MODEL_NAME = "mistral-small-latest"


def mistral_answer(question: str, context: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful syllabus assistant. "
                "Answer ONLY from the provided context. "
                "If the answer is not present, say you couldn't find it."
            )
        },
        {
            "role": "user",
            "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
        }
    ]

    resp = client.chat.complete(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
    )

    return resp.choices[0].message.content
