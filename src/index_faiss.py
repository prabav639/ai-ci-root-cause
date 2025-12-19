from __future__ import annotations
import numpy as np
import faiss
from typing import Tuple

class FaissIndex:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)

    def add(self, vectors: np.ndarray):
        if vectors.dtype != np.float32:
            vectors = vectors.astype("float32")
        self.index.add(vectors)

    def search(self, queries: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        if queries.dtype != np.float32:
            queries = queries.astype("float32")
        return self.index.search(queries, k)
