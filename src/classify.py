from __future__ import annotations

import re
from typing import Tuple

# Each entry maps a human-readable label to a compiled regex that matches lines.
ROOT_CAUSE_PATTERNS = [
    ("k8s_image_pull", re.compile(r"(ImagePullBackOff|ErrImagePull|manifest unknown|pull access denied)", re.I)),
    ("k8s_crash_loop", re.compile(r"(CrashLoopBackOff|Back-off restarting failed container|OOMKilled)", re.I)),
    ("network_timeout", re.compile(r"(timed out|timeout|TLS handshake|name resolution|connection reset|connection refused)", re.I)),
    ("dependency_resolution", re.compile(r"(Could not resolve dependency|No matching distribution found|pip.*ERROR|ModuleNotFoundError|cannot find package)", re.I)),
    ("test_failure", re.compile(r"(AssertionError|FAILED\s+\w+|FAIL\s+.+|test .* failed)", re.I)),
    ("build_compile_error", re.compile(r"(fatal error:|undefined reference to|ld: .*|collect2: error|error: .*)", re.I)),
]

DEFAULT_LABEL = "unknown"


def classify_root_cause(text: str) -> Tuple[str, float]:
    """
    Determine the root cause category for a given text snippet.
    Returns the label and a basic confidence estimate.
    """
    for label, pattern in ROOT_CAUSE_PATTERNS:
        if pattern.search(text):
            return label, 0.78
    return DEFAULT_LABEL, 0.40
