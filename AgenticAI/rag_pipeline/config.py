from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"       # drop PDFs here
DB_DIR   = BASE_DIR / "db"         # ChromaDB persists here

# --- Chunking ---
CHUNK_SIZE    = 800    # characters per chunk
CHUNK_OVERLAP = 100    # characters shared between consecutive chunks

# --- Embedding model (local, no API key needed) ---
EMBED_MODEL = "all-MiniLM-L6-v2"

# --- Vector store ---
COLLECTION_NAME = "pdf_rag"

# --- Groq (free tier) ---
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_MAX_TOKENS = 1024

# --- Retrieval ---
TOP_K = 5   # number of chunks returned per query
