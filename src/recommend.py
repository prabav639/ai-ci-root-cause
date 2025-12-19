from __future__ import annotations

from typing import Dict, List

# Mapping from root cause to remediation suggestions.
REMEDIATIONS: Dict[str, List[str]] = {
    "k8s_image_pull": [
        "Verify image name/tag exists and registry credentials are correct.",
        "Check imagePullSecrets / workload identity permissions.",
        "Confirm the image is pushed to the expected registry and region.",
    ],
    "k8s_crash_loop": [
        "Inspect container logs for startup exceptions; verify environment variables and secrets.",
        "Check resource limits/requests; look for OOMKilled events.",
        "Add readiness/liveness probes and ensure dependencies are reachable.",
    ],
    "network_timeout": [
        "Check DNS resolution and egress rules (VPC/firewall/NAT).",
        "Add retry with exponential backoff for network calls.",
        "Validate service endpoints, TLS certificates, and proxy settings.",
    ],
    "dependency_resolution": [
        "Pin dependency versions and validate lockfiles are updated.",
        "Check package registry availability and authentication.",
        "Clear caches and rebuild environment to avoid corrupted artifacts.",
    ],
    "test_failure": [
        "Identify flaky tests; quarantine or add retries with reporting.",
        "Run failed tests in isolation; verify test data and timing assumptions.",
        "Check recent changes affecting the failing module; add deterministic waits/mocks.",
    ],
    "build_compile_error": [
        "Confirm compiler/toolchain versions match the build environment.",
        "Check missing headers/libs and update build scripts or container image.",
        "Re-run with verbose flags; ensure build cache is not stale/corrupted.",
    ],
    "unknown": [
        "Collect additional logs (full stack traces, env details) and re-run with debug flags.",
        "Check recent merges and bisect to isolate the regression.",
    ],
}


def recommendations_for(root_cause: str) -> List[str]:
    """Return a list of recommended actions for the given root cause label."""
    return REMEDIATIONS.get(root_cause, REMEDIATIONS["unknown"])
