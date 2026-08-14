"""
retrieve.py — Step 2: query → embed → semantic search → relevant chunks
"""
import chromadb
from sentence_transformers import SentenceTransformer
from .config import DB_DIR, EMBED_MODEL, COLLECTION_NAME, TOP_K


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """
    Return the top-k most relevant chunks for a query.

    Each returned dict has:
        text   : str   — the chunk content
        source : str   — original PDF filename
        score  : float — similarity score (higher = more relevant)
    """
    client     = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    if collection.count() == 0:
        return []

    model           = SentenceTransformer(EMBED_MODEL)
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({"text": doc, "source": meta["source"], "score": round(1 - dist, 4)})

    # sort by score descending
    return sorted(chunks, key=lambda c: c["score"], reverse=True)
