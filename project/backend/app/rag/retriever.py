import os
os.environ["HF_HOME"] = "/root/.cache/huggingface"
os.environ["HUGGINGFACE_HUB_CACHE"] = "/root/.cache/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/root/.cache/huggingface"

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

from huggingface_hub import login
import json
import numpy as np
from sentence_transformers import SentenceTransformer

def ensure_hf_login():
    token = os.environ.get("HF_TOKEN")
    if token:
        try:
            login(token=token)
        except Exception as e:
            print("HF login failed:", e)

BASE_DIR = os.path.dirname(__file__)
CHUNKS_PATH = os.path.join(BASE_DIR, "data", "chunks.jsonl")
EMB_PATH = os.path.join(BASE_DIR, "data", "embeddings.npy")


MODEL_E5 = None
CHUNKS = None
EMBS = None

def load_retriever():

    global MODEL_E5, CHUNKS, EMBS

    if MODEL_E5 is not None:
        return

    print("[RAG] Loading E5-Large-V2 model...")
    MODEL_E5 = SentenceTransformer("intfloat/e5-large-v2")
    print("[RAG] Model loaded.")

    print("[RAG] Loading chunks...")
    CHUNKS, _ = load_chunks()
    print(f"[RAG] Loaded {len(CHUNKS)} chunks.")

    print("[RAG] Loading embeddings...")
    EMBS = np.load(EMB_PATH)
    print(f"[RAG] Embeddings loaded: {EMBS.shape}")


def load_chunks(path=CHUNKS_PATH):
    chunks = []
    texts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            chunks.append(entry)
            texts.append(entry.get("text", ""))
    return chunks, texts



def dense_search(query: str, top_k: int = 5):

    load_retriever()

    query_emb = MODEL_E5.encode(
        "query: " + query,
        normalize_embeddings=True
    )

    scores = np.dot(EMBS, query_emb)

    top_idx = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_idx:
        results.append({
            "chunk_id": CHUNKS[idx].get("chunk_id"),
            "text": CHUNKS[idx].get("text"),
            "score": float(scores[idx])
        })

    return results


def retrieve(query: str, top_k: int = 5):
    return dense_search(query, top_k=top_k)
