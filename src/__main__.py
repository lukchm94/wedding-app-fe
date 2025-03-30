from __future__ import annotations

import click
import uvicorn


@click.command(help="Starts Uvicorn server based on provided arguments.")
@click.option(
    "--host", default="127.0.0.1", help="Bind socket to this host. [default:127.0.0.1]"
)
@click.option("--port", default=8000, help="Bind socket to this port. [default: 8000]")
@click.option("--reload", default=False, is_flag=True, help="Enable auto-reload.")
def run(host: str, port: int, reload: bool) -> None:

    uvicorn.run(
        "src.shared.server.app:app",
        host=host,
        port=port,
        reload=reload,
    )


run()
