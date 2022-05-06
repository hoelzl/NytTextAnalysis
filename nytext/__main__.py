from pathlib import Path
from xmlrpc.client import Server
import typer
from .loader import (
    download_and_save_raw_archive_data,
    download_archive_data,
    generate_date_range,
    ServerKind,
    write_archive_data,
)

app = typer.Typer()


@app.command()
def download_archives(
    start_year: int = 2022,
    start_month: int = 1,
    end_year: int = 2022,
    end_month: int = 1,
):
    """
    Download article archives into the server's data dictionary.

    The article data for each month is saved to an individual file in the
    file-system layout expected by the server.
    """
    download_and_save_raw_archive_data(
        generate_date_range(start_year, start_month, end_year, end_month)
    )


@app.command()
def download_data(
    file: Path = Path("data.json"),
    start_year: int = 2022,
    start_month: int = 1,
    end_year: int = 2022,
    end_month: int = 1,
    server_kind: ServerKind = ServerKind.LOCAL,
):
    """
    Download article data into a file (removing metadata).

    The data from all months is concatenated into the output file.
    """
    data = download_archive_data(
        generate_date_range(start_year, start_month, end_year, end_month),
        server_kind=server_kind,
    )
    write_archive_data(data, file)


if __name__ == "__main__":
    app()
