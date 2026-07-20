from __future__ import annotations

import random
import time

import numpy as np


CLASS_NAMES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
]


class MockCVModel:
    def __init__(self, min_latency: float = 0.01, max_latency: float = 0.05, seed: int = 42):
        self.min_latency = min_latency
        self.max_latency = max_latency
        self._rng = random.Random(seed)

    def predict(self, image: np.ndarray) -> tuple[int, str, float]:
        latency = self._rng.uniform(self.min_latency, self.max_latency)
        time.sleep(latency)
        class_id = self._rng.randint(0, len(CLASS_NAMES) - 1)
        confidence = round(self._rng.uniform(0.5, 0.99), 4)
        return class_id, CLASS_NAMES[class_id], confidence
