from __future__ import annotations
from pathlib import Path
import typer
from rich import print

from .pipeline import run_pipeline

app = typer.Typer(help="Analyze CI logs and produce a JSON report")

@app.command()
def run(
    log_dir: Path = typer.Option(..., exists=True, file_okay=False, dir_okay=True),
    out: Path = typer.Option(Path("outputs/report.json")),
    cluster_method: str = typer.Option("dbscan", help="dbscan or kmeans"),
):
    """
    Process all .log files under log_dir, cluster similar failures,
    and write a report as JSON to out.
    """
    result = run_pipeline(log_dir, cluster_method=cluster_method)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result.model_dump_json(indent=2))
    print(f"[green]Report written:[/green] {out}")
    print(f"[cyan]Events:[/cyan] {len(result.events)}  [cyan]Clusters:[/cyan] {len(result.clusters)}")

if __name__ == "__main__":
    app()
