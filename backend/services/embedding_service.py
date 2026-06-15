"""
Sentence-Transformer embedding service.

Uses the all-MiniLM-L6-v2 model to generate embeddings for text, compute
similarity scores, and detect duplicate complaints / similar schemes.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Lazy-loaded model
_model = None


def _get_model():
    """Lazily load the SentenceTransformer model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            logger.info("Loaded embedding model: %s", settings.EMBEDDING_MODEL_NAME)
        except Exception as e:
            logger.error("Failed to load embedding model: %s", e)
            raise RuntimeError(f"Embedding model unavailable: {e}")
    return _model


def generate_embedding(text: str) -> List[float]:
    """
    Generate a dense vector embedding for the given text.

    Args:
        text: Input text (complaint description, scheme description, etc.)

    Returns:
        List of floats representing the 384-dimensional embedding vector.
    """
    if not text or not text.strip():
        return [0.0] * 384  # MiniLM-L6-v2 produces 384-dim vectors

    model = _get_model()
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding.tolist()


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Returns:
        Float between -1 and 1 (1 = identical, 0 = unrelated, -1 = opposite).
    """
    if not embedding1 or not embedding2:
        return 0.0

    a = np.array(embedding1, dtype=np.float32)
    b = np.array(embedding2, dtype=np.float32)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a, b) / (norm_a * norm_b))


def find_duplicates(
    new_complaint_text: str,
    existing_complaints: List[Dict[str, Any]],
    threshold: float = 0.85,
) -> List[Dict[str, Any]]:
    """
    Find complaints in `existing_complaints` that are potential duplicates of
    the new complaint based on semantic similarity.

    Args:
        new_complaint_text: Text of the new complaint.
        existing_complaints: List of dicts, each must have keys:
            - id, tracking_id, title, category, status, embedding (List[float])
        threshold: Minimum cosine similarity to consider a duplicate (0-1).

    Returns:
        List of dicts with keys: complaint_id, tracking_id, title, similarity_score,
        category, status – sorted by similarity descending.
    """
    if not new_complaint_text or not existing_complaints:
        return []

    new_embedding = generate_embedding(new_complaint_text)

    duplicates: List[Dict[str, Any]] = []

    for complaint in existing_complaints:
        existing_emb = complaint.get("embedding")
        if not existing_emb:
            continue

        similarity = compute_similarity(new_embedding, existing_emb)

        if similarity >= threshold:
            duplicates.append({
                "complaint_id": complaint.get("id", ""),
                "tracking_id": complaint.get("tracking_id", ""),
                "title": complaint.get("title", ""),
                "similarity_score": round(similarity, 4),
                "category": complaint.get("category", ""),
                "status": complaint.get("status", ""),
            })

    # Sort by similarity descending
    duplicates.sort(key=lambda x: x["similarity_score"], reverse=True)
    return duplicates[:10]  # Return top 10 at most


def find_similar_schemes(
    query: str,
    scheme_descriptions: List[Dict[str, Any]],
    top_k: int = 10,
) -> List[Dict[str, Any]]:
    """
    Find schemes most semantically similar to a user's query or profile text.

    Args:
        query: Search query or profile description.
        scheme_descriptions: List of dicts, each with keys:
            - id, name, embedding (List[float])
        top_k: Number of top results to return.

    Returns:
        List of dicts with keys: scheme_id, scheme_name, similarity_score
        – sorted by similarity descending.
    """
    if not query or not scheme_descriptions:
        return []

    query_embedding = generate_embedding(query)

    scored: List[Tuple[float, Dict[str, Any]]] = []

    for scheme in scheme_descriptions:
        scheme_emb = scheme.get("embedding")
        if not scheme_emb:
            continue

        similarity = compute_similarity(query_embedding, scheme_emb)
        scored.append((similarity, scheme))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    results: List[Dict[str, Any]] = []
    for score, scheme in scored[:top_k]:
        results.append({
            "scheme_id": scheme.get("id", ""),
            "scheme_name": scheme.get("name", ""),
            "similarity_score": round(score, 4),
        })

    return results


def batch_generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts efficiently.

    Args:
        texts: List of input texts.

    Returns:
        List of embedding vectors (each a list of floats).
    """
    if not texts:
        return []

    model = _get_model()
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, batch_size=32)
    return [emb.tolist() for emb in embeddings]
