from __future__ import annotations
from pathlib import Path
from typing import Dict, List
import re
import collections

from .models import PipelineResult, FailureEvent
from .parse_logs import parse_logs_dir
from .embed import Embedder
from .cluster import cluster_vectors
from .index_faiss import FaissIndex
from .config import FAISS_TOP_K

def summarize_cluster_signatures(signatures: List[str], top_k: int = 3) -> str:
    words = []
    for sig in signatures:
        words.extend(re.findall(r"\b\w+\b", sig.lower()))
    common = collections.Counter(words).most_common(top_k)
    return ", ".join([w for w, _ in common]) or "generic-failure"

def run_pipeline(log_dir: Path, cluster_method: str = "dbscan") -> PipelineResult:
    events = parse_logs_dir(log_dir)
    if not events:
        return PipelineResult(events=[], clusters={})

    embedder = Embedder()
    vectors = embedder.embed_events(events)
    dim = vectors.shape[1]

    faiss_index = FaissIndex(dim)
    faiss_index.add(vectors)

    labels = cluster_vectors(vectors, method=cluster_method)

    # Assign basic root cause labels based on cluster
    for event, lbl in zip(events, labels):
        event.cluster_id = int(lbl)
        event.root_cause = f"cluster_{lbl}"
        event.confidence = 1.0
        event.recommendations = [
            "Review the error/exception message and stack trace.",
            "Inspect the environment and configuration.",
            "Re-run the CI job with verbose logging."
        ]

    clusters: Dict[int, Dict[str, object]] = {}
    unique = sorted(set(int(x) for x in labels))
    for cid in unique:
        indices = [i for i, lbl in enumerate(labels) if int(lbl) == cid]
        if not indices:
            continue

        rep_idx = indices[0]
        rep_vec = vectors[rep_idx : rep_idx + 1]
        scores, neighbors = faiss_index.search(rep_vec, k=min(FAISS_TOP_K, len(events)))

        similar_failures = []
        for score, idx in zip(scores[0].tolist(), neighbors[0].tolist()):
            if idx < 0:
                continue
            similar_failures.append({
                "score": float(score),
                "signature": events[idx].signature,
                "file": events[idx].file_path,
            })

        summary = summarize_cluster_signatures([events[i].signature for i in indices])

        clusters[cid] = {
            "count": len(indices),
            "summary": summary,
            "similar_failures": similar_failures,
            "recommendations": events[rep_idx].recommendations,
        }

    return PipelineResult(events=events, clusters=clusters)
