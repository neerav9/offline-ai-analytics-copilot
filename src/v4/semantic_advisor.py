# src/v4/semantic_advisor.py

from typing import Dict, Optional
import logging

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None
    util = None


# -----------------------------
# Configuration
# -----------------------------

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_logger = logging.getLogger(__name__)
_model = None


# -----------------------------
# Model Loader (lazy + safe)
# -----------------------------

def _load_model() -> Optional[SentenceTransformer]:
    """
    Lazy-load the HF sentence transformer model.
    Returns None if unavailable.
    """
    global _model

    if _model is not None:
        return _model

    if SentenceTransformer is None:
        _logger.warning("sentence-transformers not installed. HF advisor disabled.")
        return None

    try:
        _model = SentenceTransformer(MODEL_NAME)
        return _model
    except Exception as e:
        _logger.warning(f"Failed to load HF model: {e}")
        return None


# -----------------------------
# Public API
# -----------------------------

def semantic_hint(
    column_name: str,
    context: str = ""
) -> Dict[str, Optional[float]]:
    """
    Provide a semantic suggestion for a column using HF embeddings.

    Returns:
        {
          "suggestion": str | None,
          "confidence": float | None
        }
    """

    model = _load_model()
    if model is None:
        return {"suggestion": None, "confidence": None}

    # Candidate semantic labels (controlled vocabulary)
    semantic_labels = [
        "revenue",
        "sales amount",
        "academic score",
        "quantity",
        "count",
        "date",
        "timestamp",
        "person name",
        "product name",
        "category",
        "geographic region",
        "department",
    ]

    try:
        column_text = f"{column_name}. {context}".strip()

        col_emb = model.encode(column_text, convert_to_tensor=True)
        label_embs = model.encode(semantic_labels, convert_to_tensor=True)

        scores = util.cos_sim(col_emb, label_embs)[0]

        best_idx = int(scores.argmax())
        best_score = float(scores[best_idx])

        return {
            "suggestion": semantic_labels[best_idx],
            "confidence": round(best_score, 2)
        }

    except Exception as e:
        _logger.warning(f"HF semantic hint failed: {e}")
        return {"suggestion": None, "confidence": None}
