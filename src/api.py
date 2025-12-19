from __future__ import annotations
from fastapi import FastAPI, File, UploadFile
from pathlib import Path
import tempfile
import shutil

from src.pipeline import run_pipeline

api = FastAPI(title="AI CI Root Cause Analyzer", version="1.0.0")

@api.post("/analyze")
async def analyze(file: UploadFile = File(...), cluster_method: str = "dbscan"):
    """
    Accept a .log file upload and return the analysis result as JSON.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / file.filename
        with tmp_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        result = run_pipeline(Path(tmpdir), cluster_method=cluster_method)
        return result.model_dump()
