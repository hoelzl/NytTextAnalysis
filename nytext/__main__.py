from pathlib import Path
import typer
from .loader import (
    download_and_save_raw_archive_data,
    download_archive_data,
    generate_date_range,
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
    download_and_save_raw_archive_data(
        generate_date_range(start_year, start_month, end_year, end_month)
    )


@app.command()
def download_data(
    file=Path("data.json"),
    start_year: int = 2022,
    start_month: int = 1,
    end_year: int = 2022,
    end_month: int = 1,
):
    data = download_archive_data(
        generate_date_range(start_year, start_month, end_year, end_month)
    )
    write_archive_data(data, file)


if __name__ == "__main__":
    app()
