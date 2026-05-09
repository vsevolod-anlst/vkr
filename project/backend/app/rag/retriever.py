import numpy as np
from sentence_transformers import SentenceTransformer
from time import time

MODEL_E5 = SentenceTransformer("intfloat/e5-large-v2")

def build_dense_index(texts, model=MODEL_E5, save_path=None):
    print("[INFO] Encoding chunk embeddings...")
    t0 = time()
    chunk_embs = model.encode(
        ["passage: " + t for t in texts],
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True
    )
    chunk_embs = np.array(chunk_embs)
    print(f"[INFO] Chunk embeddings ready (took {time()-t0:.1f}s)")
    if save_path:
        np.save(save_path, chunk_embs)
        print(f"[INFO] Saved embeddings to {save_path}")
    return chunk_embs
