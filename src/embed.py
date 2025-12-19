from __future__ import annotations
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from .models import FailureEvent
from .config import EMBED_MODEL_NAME

class Embedder:
    def __init__(self, model_name: str = EMBED_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed_events(self, events: List[FailureEvent]) -> np.ndarray:
        texts = [f"{event.signature}\n{event.excerpt[:1200]}" for event in events]
        embeddings = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return embeddings.astype(np.float32)
