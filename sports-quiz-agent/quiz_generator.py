"""
Core AI agent logic: combines retrieved vector-DB context and fresh
web search snippets, then prompts an LLM (Claude, via the Anthropic
API) to generate a grounded, factually-accurate sports quiz as
structured JSON.
"""

import os
import json
import random
import anthropic

from vector_store import retrieve_context, add_facts
from web_search import search_recent_sports_info

MODEL = "claude-sonnet-4-6"


def _get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Set it before running the app (see README.md)."
        )
    return anthropic.Anthropic(api_key=api_key)


def build_context(sport: str) -> str:
    """
    Gathers grounding context from two sources:
      1. ChromaDB vector retrieval (curated/seed knowledge)
      2. Live web search (fresh, recent information)

    Freshly retrieved web facts are also written back into the vector
    store, so the knowledge base grows over time.
    """
    vector_facts = retrieve_context(sport, n_results=6)
    web_facts = search_recent_sports_info(sport, max_results=5)

    if web_facts:
        add_facts(sport, web_facts)

    context_lines = []
    if vector_facts:
        context_lines.append("Known facts:")
        context_lines.extend(f"- {f}" for f in vector_facts)
    if web_facts:
        context_lines.append("\nRecent web search results:")
        context_lines.extend(f"- {f}" for f in web_facts)

    return "\n".join(context_lines) if context_lines else "No grounding context retrieved."


def generate_quiz(sport: str, difficulty: str, num_questions: int = 5, seed_variation: str = "") -> dict:
    """
    Generates a structured multiple-choice sports quiz grounded in
    retrieved context. Returns a dict matching the assignment's
    expected output schema.
    """
    context = build_context(sport)
    client = _get_client()

    variation_hint = seed_variation or f"variation-token-{random.randint(1000, 9999)}"

    system_prompt = (
        "You are a sports quiz generation agent. You MUST ground every "
        "question strictly in the provided context. Do not invent facts, "
        "scores, dates, or winners that are not supported by the context. "
        "If the context is insufficient for a fact, choose a different, "
        "well-supported question instead of guessing. "
        "Always respond with ONLY valid JSON, no markdown fences, no prose."
    )

    user_prompt = f"""
Generate a {difficulty} difficulty sports quiz about {sport}.

Context (use this to ensure factual accuracy — do not contradict it):
{context}

Requirements:
- Produce exactly {num_questions} multiple-choice questions.
- Each question must have exactly 4 answer options (A, B, C, D).
- Exactly one option must be correct.
- Include a short (1-2 sentence) explanation for the correct answer.
- Vary question topics (history, records, tournaments, rules) rather than
  repeating the same fact.
- Freshness token (ignore in content, just ensures variety across calls): {variation_hint}

Respond with ONLY this JSON structure, no other text:
{{
  "sport": "{sport}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "question": "string",
      "options": {{"A": "string", "B": "string", "C": "string", "D": "string"}},
      "correct_answer": "A" | "B" | "C" | "D",
      "explanation": "string"
    }}
  ]
}}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        temperature=0.9,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw_text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    ).strip()

    # Defensive cleanup in case the model wraps output in a code fence.
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    try:
        quiz = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Model did not return valid JSON: {e}\nRaw output:\n{raw_text}")

    return quiz
