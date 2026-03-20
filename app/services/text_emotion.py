from __future__ import annotations

import re
from typing import Dict, List

from app.services.emotion_labels import EMOTIONS


_POSITIVE_WORDS = {
    "love",
    "like",
    "great",
    "awesome",
    "amazing",
    "good",
    "nice",
    "wonderful",
    "excellent",
    "happy",
    "yay",
    "cool",
}

_SAD_WORDS = {
    "sad",
    "down",
    "cry",
    "depressed",
    "unhappy",
    "tired",
    "pain",
    "hurt",
}

_ANGRY_WORDS = {
    "angry",
    "mad",
    "furious",
    "hate",
    "annoyed",
    "upset",
    "worst",
    "terrible",
}

_FEAR_WORDS = {
    "fear",
    "scared",
    "afraid",
    "worried",
    "nervous",
    "panic",
    "terrified",
}

_DISGUST_WORDS = {
    "disgust",
    "gross",
    "nasty",
    "disgusting",
}

_SURPRISE_WORDS = {
    "omg",
    "wow",
    "what",
    "surprised",
    "unexpected",
}


def _count_words(text: str, vocab: set[str]) -> int:
    # Basic word extraction; keeps the demo lightweight and dependency-free.
    words = re.findall(r"[a-z']+", text.lower())
    return sum(1 for w in words if w in vocab)


def _normalize(scores: Dict[str, float]) -> List[Dict[str, float]]:
    total = sum(max(0.0, v) for v in scores.values())
    if total <= 0:
        # If we have no signal, show neutral confidently.
        emotions = [{"label": e, "score": (1.0 if e == "Neutral" else 0.0)} for e in EMOTIONS]
        return emotions

    emotions = []
    for label in EMOTIONS:
        emotions.append({"label": label, "score": max(0.0, scores.get(label, 0.0)) / total})
    return emotions


def predict_text_emotion(text: str) -> Dict[str, object]:
    """
    Lightweight heuristic predictor (placeholder).
    Replace this function with a real model when you plug in Transformers.
    """
    text = (text or "").strip()

    pos = _count_words(text, _POSITIVE_WORDS)
    sad = _count_words(text, _SAD_WORDS)
    angry = _count_words(text, _ANGRY_WORDS)
    fear = _count_words(text, _FEAR_WORDS)
    disgust = _count_words(text, _DISGUST_WORDS)
    surprise_words = _count_words(text, _SURPRISE_WORDS)

    exclamations = text.count("!")
    question_marks = text.count("?")
    uppercase_ratio = sum(1 for c in text if c.isupper()) / max(1, sum(1 for c in text if c.isalpha()))  # 0..1

    # Seed baseline so “Neutral” still gets a chance.
    scores: Dict[str, float] = {e: 0.0 for e in EMOTIONS}
    scores["Happy"] += float(pos)
    scores["Sad"] += float(sad) + float(1.0) * (1 if "..." in text else 0)
    scores["Angry"] += float(angry) + (2.0 * exclamations * uppercase_ratio)
    scores["Fear"] += float(fear) + float(question_marks) * 0.8
    scores["Disgust"] += float(disgust)
    scores["Surprise"] += float(surprise_words) + float(exclamations) * 0.9

    if scores["Happy"] + scores["Sad"] + scores["Angry"] + scores["Fear"] + scores["Disgust"] + scores["Surprise"] <= 0.2:
        scores["Neutral"] = 1.0
    else:
        # If there is some signal, keep a small neutral floor.
        scores["Neutral"] = 0.15

    emotions = _normalize(scores)
    top = max(emotions, key=lambda x: x["score"])
    return {
        "top_emotion": top["label"],
        "emotions": [{"label": e["label"], "score": round(float(e["score"]), 4)} for e in emotions],
    }

