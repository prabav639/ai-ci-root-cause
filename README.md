# AI-Driven CI Failure Root Cause Analysis

This repository contains a proof-of-concept tool for analyzing continuous integration (CI) logs using AI techniques. It parses log files, generates embeddings for failure snippets, clusters similar failures, classifies root causes using simple heuristics, and suggests remediation steps. The project demonstrates how AI-assisted analysis can reduce mean time to resolution (MTTR) in CI pipelines.

## Features

- Parse CI log files to extract failure events and contexts
- Generate semantic embeddings (using sentence-transformers) for failure snippets
- Cluster failures using DBSCAN or KMeans to identify related issues
- Classify root causes with heuristic patterns (build errors, test failures, network issues, etc.)
- Retrieve similar past failures via a FAISS index for context and diagnosis
- Provide human-readable remediation recommendations for each root cause
- CLI tool for batch processing directories of logs
- Optional FastAPI service for uploading log files and obtaining structured analysis results

## Getting Started

See `requirements.txt` for dependencies. You can run the CLI with:

```
python -m src.cli run --log-dir data/sample_ci_logs --out outputs/report.json
```

For API usage, run:

```
uvicorn app.api:api --reload --port 8000
```

and POST a `.log` file to `/analyze`.

## License

This project is provided for educational purposes.
