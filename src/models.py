from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class FailureEvent(BaseModel):
    file_path: str
    signature: str
    excerpt: str
    cluster_id: Optional[int] = None
    root_cause: Optional[str] = None
    confidence: Optional[float] = None
    recommendations: List[str] = Field(default_factory=list)

class PipelineResult(BaseModel):
    events: List[FailureEvent]
    clusters: Dict[int, Dict[str, object]]
