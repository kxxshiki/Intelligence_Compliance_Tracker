from __future__ import annotations

import hashlib

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None

from app.core.config import settings


class EmbeddingService:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model
        self.model = None

    def _ensure_model(self):
        if self.model is None and SentenceTransformer is not None:
            self.model = SentenceTransformer(self.model_name)

    def _fallback_embedding(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        values: list[float] = []
        for index in range(384):
            chunk = digest[(index * 2) % len(digest):(index * 2 + 2) % len(digest)]
            if len(chunk) < 2:
                chunk = digest
            value = int(chunk, 16) / 255.0
            values.append((value * 2.0) - 1.0)
        return values

    def embed_text(self, text: str) -> list[float]:
        if not text:
            return self._fallback_embedding("")
        try:
            self._ensure_model()
            if self.model is not None:
                vector = self.model.encode(text, normalize_embeddings=True)
                return np.asarray(vector, dtype=float).tolist()
        except Exception:
            pass
        return self._fallback_embedding(text)

    def cosine_similarity(self, left: list[float], right: list[float]) -> float:
        if not left or not right or len(left) != len(right):
            return 0.0
        left_array = np.asarray(left, dtype=float)
        right_array = np.asarray(right, dtype=float)
        dot = float(np.dot(left_array, right_array))
        left_norm = float(np.linalg.norm(left_array))
        right_norm = float(np.linalg.norm(right_array))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot / (left_norm * right_norm)
