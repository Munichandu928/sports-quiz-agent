"""
Web search module — fetches fresh, recent sports information to
ground quiz generation beyond the static seed knowledge base.

Uses the duckduckgo-search library, which requires no API key,
making the project runnable out-of-the-box for evaluation.
"""

from ddgs import DDGS


def search_recent_sports_info(sport: str, max_results: int = 5) -> list[str]:
    """
    Searches the web for recent news / facts about the given sport and
    returns a list of short text snippets suitable for grounding quiz
    question generation.
    """
    query = f"{sport} latest news results records 2026"
    snippets = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for r in results:
                title = r.get("title", "")
                body = r.get("body", "")
                if body:
                    snippets.append(f"{title}: {body}")
    except Exception as e:
        # Web search can fail due to network/rate limits — the app
        # should still work using the vector DB knowledge alone.
        print(f"[web_search] Search failed, falling back to vector DB only: {e}")

    return snippets
