"""
ingest.py — Step 1: PDF → chunks → embeddings → ChromaDB

Usage:
    python -m rag_pipeline.ingest
    python -m rag_pipeline.ingest path/to/specific.pdf
"""
import sys
from pathlib import Path
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer
from .config import DATA_DIR, DB_DIR, CHUNK_SIZE, CHUNK_OVERLAP, EMBED_MODEL, COLLECTION_NAME


# ── helpers ────────────────────────────────────────────────────────────────

def extract_text(pdf_path: Path) -> str:
    """Return all text from a PDF file."""
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def chunk_text(text: str) -> list[str]:
    """Split text into overlapping fixed-size chunks."""
    chunks, start = [], 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end].strip())
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return [c for c in chunks if c]   # discard empty strings


# ── main ───────────────────────────────────────────────────────────────────

def ingest(source: Path | None = None) -> None:
    """
    Ingest PDFs into the vector store.

    Args:
        source: A single PDF file or a directory.  Defaults to DATA_DIR.
    """
    source = Path(source) if source else DATA_DIR
    DB_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # collect PDF files
    if source.is_file() and source.suffix.lower() == ".pdf":
        pdf_files = [source]
    elif source.is_dir():
        pdf_files = sorted(source.glob("*.pdf"))
    else:
        print(f"[ingest] No PDFs found at: {source}")
        return

    if not pdf_files:
        print(f"[ingest] No PDF files found in {source}")
        print(f"         Drop your PDFs into  {DATA_DIR}  and re-run.")
        return

    print(f"[ingest] Loading embedding model '{EMBED_MODEL}'...")
    model = SentenceTransformer(EMBED_MODEL)

    client     = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    total_chunks = 0
    for pdf in pdf_files:
        print(f"\n[ingest] Processing: {pdf.name}")
        text   = extract_text(pdf)
        chunks = chunk_text(text)
        if not chunks:
            print(f"         No text extracted — is the PDF scanned?  Skipping.")
            continue

        embeddings = model.encode(chunks, show_progress_bar=True).tolist()
        ids        = [f"{pdf.stem}__{i}" for i in range(len(chunks))]
        metadatas  = [{"source": pdf.name, "chunk_index": i} for i in range(len(chunks))]

        # upsert so re-ingesting the same file is safe
        collection.upsert(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)
        print(f"         → {len(chunks)} chunks stored")
        total_chunks += len(chunks)

    print(f"\n[ingest] Done. {total_chunks} total chunks in '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    path_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    ingest(path_arg)
