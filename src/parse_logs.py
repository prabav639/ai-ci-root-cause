from __future__ import annotations
from pathlib import Path
from typing import List
import re

from .models import FailureEvent

# A simple heuristic: consider lines containing these words as failure events
FAILURE_KEYWORDS = re.compile(r"\b(error|failed|exception|abort|panic|fatal)\b", re.I)

def parse_log_file(path: Path, context: int = 6) -> List[FailureEvent]:
    content = path.read_text(errors="ignore")
    lines = content.splitlines()
    events: List[FailureEvent] = []
    for idx, line in enumerate(lines):
        if FAILURE_KEYWORDS.search(line):
            start = max(0, idx - context)
            end = min(len(lines), idx + context + 1)
            excerpt = "\n".join(lines[start:end])
            signature = line.strip()[:240]
            events.append(FailureEvent(file_path=str(path), signature=signature, excerpt=excerpt))
    return events

def parse_logs_dir(log_dir: Path) -> List[FailureEvent]:
    events: List[FailureEvent] = []
    for log_file in sorted(log_dir.glob("**/*.log")):
        events.extend(parse_log_file(log_file))
    return events
