from __future__ import annotations

import hashlib
import random
from typing import Dict, List

from app.services.emotion_labels import EMOTIONS


def predict_speech_emotion(audio_bytes: bytes) -> Dict[str, object]:
    """
    Lightweight placeholder predictor (dependency-free).
    Replace with a real speech emotion model later.
    """
    audio_bytes = audio_bytes or b""
    digest = hashlib.sha256(audio_bytes).hexdigest()
    seed = int(digest[:8], 16)
    rng = random.Random(seed)

    # Give a small deterministic structure: larger "signals" slightly increase
    # non-neutral emotions.
    strength = min(1.0, len(audio_bytes) / 200000.0)  # ~0..1

    # Start with neutral baseline.
    raw_scores = {e: 0.05 for e in EMOTIONS}
    raw_scores["Neutral"] = 0.8 - 0.3 * strength

    # Distribute remaining probability mass across the other emotions.
    for e in EMOTIONS:
        if e == "Neutral":
            continue
        # Skew towards mid-range values.
        raw_scores[e] += (0.2 + 0.8 * strength) * (rng.random() ** 0.6)

    total = sum(raw_scores.values())
    emotions: List[Dict[str, float]] = []
    for label in EMOTIONS:
        emotions.append({"label": label, "score": raw_scores[label] / total})

    top = max(emotions, key=lambda x: x["score"])
    return {
        "top_emotion": top["label"],
        "emotions": [{"label": e["label"], "score": round(float(e["score"]), 4)} for e in emotions],
    }

