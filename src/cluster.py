from __future__ import annotations
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from .config import DBSCAN_EPS, DBSCAN_MIN_SAMPLES

def cluster_vectors(vectors: np.ndarray, method: str = "dbscan") -> np.ndarray:
    if len(vectors) == 0:
        return np.array([], dtype=int)
    if method == "kmeans":
        n = len(vectors)
        k = max(2, min(8, int(n ** 0.5)))
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        return km.fit_predict(vectors)
    dbscan = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MIN_SAMPLES, metric="cosine")
    return dbscan.fit_predict(vectors)
