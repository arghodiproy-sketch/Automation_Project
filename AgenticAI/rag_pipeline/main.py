#!/usr/bin/env python3
"""
main.py — RAG pipeline entry point

Usage:
    python -m rag_pipeline.main "Your question about the PDFs"
"""
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except Exception:
    pass

from .retrieve import retrieve
from .generate import generate_answer
from .config   import DATA_DIR, DB_DIR, TOP_K


def run() -> None:
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        print("Usage: python -m rag_pipeline.main \"Your question here\"")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  RAG Query: {query}")
    print(f"{'='*60}\n")

    # ── guard: vector store must exist ──────────────────────────────────
    if not DB_DIR.exists() or not any(DB_DIR.iterdir()):
        print("[!] Vector store is empty.")
        print(f"    Drop PDF files into  {DATA_DIR}")
        print(f"    then run:  python -m rag_pipeline.ingest\n")
        sys.exit(1)

    # ── retrieve ─────────────────────────────────────────────────────────
    print(f"Searching vector store (top {TOP_K} chunks)...")
    chunks = retrieve(query)

    if not chunks:
        print("[!] No relevant chunks found. Try ingesting more documents.")
        sys.exit(1)

    print(f"Found {len(chunks)} relevant chunks:")
    for c in chunks:
        print(f"  score={c['score']:.4f}  source={c['source']}")

    # ── generate ─────────────────────────────────────────────────────────
    print("\nGenerating answer with Claude...\n")
    answer = generate_answer(query, chunks)

    print(f"{'='*60}")
    print("  Answer")
    print(f"{'='*60}\n")
    print(answer)
    print()


if __name__ == "__main__":
    run()
