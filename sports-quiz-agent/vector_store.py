"""
ChromaDB-based vector store for sports knowledge retrieval.

Uses ChromaDB's built-in default embedding function (ONNX MiniLM), so
no separate heavy embedding model download is required. Persists to
disk in ./chroma_db so the index survives across runs.
"""

import hashlib
import re

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from knowledge_base import SPORTS_KNOWLEDGE

DB_PATH = "./chroma_db"
COLLECTION_NAME = "sports_knowledge"
EMBED_DIM = 256


class HashingEmbeddingFunction(EmbeddingFunction):
    """
    A lightweight, dependency-free embedding function based on hashed
    bag-of-words term frequencies (a hashing vectorizer).

    This avoids requiring a network download of a pretrained embedding
    model (e.g. sentence-transformers/MiniLM) at first run, which makes
    the project easier to run in restricted/offline environments while
    still providing meaningful similarity search over sports facts —
    documents that share vocabulary (team names, tournament names,
    sport terms) map to similar vectors.

    For higher-quality semantic retrieval in production, swap this for
    chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction
    or an API-based embedding model.
    """

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            vec = [0.0] * EMBED_DIM
            tokens = re.findall(r"[a-z0-9]+", text.lower())
            for tok in tokens:
                h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
                idx = h % EMBED_DIM
                vec[idx] += 1.0
            norm = sum(v * v for v in vec) ** 0.5
            if norm > 0:
                vec = [v / norm for v in vec]
            embeddings.append(vec)
        return embeddings


def get_client():
    return chromadb.PersistentClient(path=DB_PATH)


def build_or_get_collection():
    """
    Creates the ChromaDB collection and populates it with seed sports
    knowledge if it doesn't already exist / is empty. Idempotent.
    """
    client = get_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, embedding_function=HashingEmbeddingFunction()
    )

    if collection.count() == 0:
        documents = []
        metadatas = []
        ids = []
        idx = 0
        for sport, facts in SPORTS_KNOWLEDGE.items():
            for fact in facts:
                documents.append(fact)
                metadatas.append({"sport": sport})
                ids.append(f"fact_{idx}")
                idx += 1

        collection.add(documents=documents, metadatas=metadatas, ids=ids)

    return collection


def retrieve_context(sport: str, n_results: int = 5):
    """
    Retrieve the most relevant stored facts for a given sport using
    vector similarity search against the sport name + general query.
    """
    collection = build_or_get_collection()

    results = collection.query(
        query_texts=[f"{sport} facts, records, tournaments, and history"],
        n_results=n_results,
        where={"sport": sport},
    )

    docs = results.get("documents", [[]])[0]
    return docs


def add_facts(sport: str, facts: list[str]):
    """
    Allows freshly retrieved web-search facts to be added into the
    vector store, so the knowledge base grows and stays current over
    time (keeps retrieval grounded in real content, not just the
    static seed set).
    """
    if not facts:
        return

    collection = build_or_get_collection()
    existing_count = collection.count()

    documents = facts
    metadatas = [{"sport": sport, "source": "web_search"} for _ in facts]
    ids = [f"web_{sport}_{existing_count + i}" for i in range(len(facts))]

    collection.add(documents=documents, metadatas=metadatas, ids=ids)
