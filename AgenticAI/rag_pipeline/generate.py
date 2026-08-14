"""
generate.py — Step 3: context chunks + query → Groq (Llama) answer
"""
import os
from groq import Groq
from .config import GROQ_MODEL, GROQ_MAX_TOKENS


def generate_answer(query: str, context_chunks: list[dict]) -> str:
    """
    Send the retrieved chunks + user question to Groq and return the answer.

    Args:
        query          : the user's question
        context_chunks : list of dicts from retrieve.retrieve()

    Returns:
        The model's answer as a string
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

    # build context block
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        context_parts.append(f"[Excerpt {i} — {chunk['source']}]\n{chunk['text']}")
    context = "\n\n---\n\n".join(context_parts)

    system_prompt = (
        "You are a precise, helpful assistant. Answer the question using ONLY the "
        "excerpts provided. If the excerpts do not contain enough information "
        "to answer, say so clearly — do not make up facts."
    )
    user_prompt = (
        f"--- CONTEXT ---\n{context}\n\n"
        f"--- QUESTION ---\n{query}\n\n"
        "Answer:"
    )

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=GROQ_MAX_TOKENS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
