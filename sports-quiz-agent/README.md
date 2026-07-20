# 🏆 AI-Powered Sports Quiz Generation Agent

An AI agent that generates engaging, factually-grounded multiple-choice
sports quizzes for social media, using Retrieval-Augmented Generation
(RAG) with a ChromaDB vector database and live web search.

## Overview

Traditional sports content on social media is limited to news,
highlights, and opinions. This project introduces an interactive
format: automatically generated sports quizzes that drive audience
participation. The agent grounds every generated question in
retrieved knowledge — combining a curated vector knowledge base with
fresh web search results — to minimize hallucination and keep content
current.

## Architecture

```
User selects sport + difficulty
            │
            ▼
   ┌─────────────────┐      ┌────────────────────┐
   │  ChromaDB (RAG)  │      │  Web Search (DDG)   │
   │  curated facts   │      │  fresh/live results │
   └────────┬─────────┘      └──────────┬──────────┘
            │                           │
            └───────────┬───────────────┘
                         ▼
              Combined grounding context
                         ▼
              Claude (Anthropic API)
        generates structured JSON quiz
                         ▼
              Streamlit dashboard renders quiz
```

- **`knowledge_base.py`** — seed factual sports knowledge (history,
  records, tournaments) used to bootstrap the vector store.
- **`vector_store.py`** — ChromaDB persistent collection setup,
  retrieval, and write-back of newly discovered web facts.
- **`web_search.py`** — live web search (DuckDuckGo, no API key
  required) for fresh sports information.
- **`quiz_generator.py`** — the core agent: builds combined context,
  prompts Claude with a strict grounding + JSON-only instruction, and
  parses the structured quiz output.
- **`app.py`** — Streamlit dashboard: sport/difficulty selection,
  generate/regenerate, and quiz display with answers + explanations.

## Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd sports-quiz-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Anthropic API key**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"       # macOS/Linux
   setx ANTHROPIC_API_KEY "your-api-key-here"          # Windows
   ```
   Get a key at https://console.anthropic.com/

4. **Run the app**
   ```bash
   streamlit run app.py
   ```
   The dashboard opens at `http://localhost:8501`.

## How It Works

1. User picks a **sport** and **difficulty**.
2. The agent retrieves the most relevant facts for that sport from
   **ChromaDB** (vector similarity search).
3. In parallel, it runs a **live web search** for recent news/records
   related to that sport, so quizzes stay current, not just
   historical.
4. Both sources are merged into a single grounding context and passed
   to **Claude**, with an explicit instruction to only use supported
   facts and avoid inventing information.
5. Claude returns a structured JSON quiz (4–5 questions, 4 options
   each, correct answer, and explanation), which the **Streamlit UI**
   renders.
6. Newly found web facts are written back into ChromaDB, so the
   knowledge base grows over time.
7. **Regenerate** re-runs the pipeline with a fresh randomization
   token to encourage variety across requests.

## Design Decisions & Tradeoffs

- **DuckDuckGo search** was used instead of a paid search API so the
  project runs out-of-the-box with just an Anthropic API key.
- **ChromaDB's default ONNX embedding function** is used (rather than
  a separately downloaded sentence-transformers model) to keep setup
  lightweight and dependency-light.
- The seed knowledge base is intentionally small and illustrative; in
  production this would be backed by a much larger, continuously
  updated sports data source.
- Web search failures are handled gracefully — the app falls back to
  vector-DB-only grounding rather than crashing.

## Example Output

```
Sport: Badminton
Difficulty: Medium
Question: Which country won the Thomas Cup in 2022?
A. Indonesia
B. India
C. China
D. Denmark
Correct Answer: B. India
Explanation: India won its first-ever Thomas Cup title in 2022 after
defeating Indonesia in the Thomas Cup final.
```

## Future Improvements

- Add caching/rate-limiting around web search calls.
- Support additional sports and multi-language quizzes.
- Add a feedback loop so flagged (incorrect) questions are removed
  from the vector store.
- Add automated tests for JSON schema validation of LLM output.
