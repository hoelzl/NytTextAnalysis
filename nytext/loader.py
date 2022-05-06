# %%
import json
from pathlib import Path

import requests
from nbex.interactive import session, pprint_interactive
from nytext.config import load_configuration


# %%
config = load_configuration()
project_data = config["nytext"]
app_id = project_data["app-id"]
api_key = project_data["api-key"]
data_dir_path = Path(project_data["data-dir"])

# %%
def load_raw_archive_data_for_month(year, month):
    assert year > 1800
    assert 1 <= month <= 12
    return requests.get(
        f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json",
        params={"api-key": api_key},
    )


# %%
def load_archive_data_for_month(year, month):
    r = load_raw_archive_data_for_month(year, month)
    if 200 <= r.status_code < 300:
        return r.json()["response"].get("docs", [])
    else:
        raise requests.RequestException(
            f"Invalid request (code {r.status_code}): {r!r}."
        )


# %%
if session.is_interactive and "data_2022_01" not in globals():
    data_2022_01 = load_archive_data_for_month(2022, 1)
else:
    data_2022_01 = globals()["data_2022_01"]

# %%
def load_archive_data(months):
    result = []
    for year, month in months:
        print(f"Trying to load archive data for {year}/{month}...", end="", flush=True)
        try:
            data = load_archive_data_for_month(year, month)
            result.extend(data)
            print(f"got {len(data)} items.")
        except requests.RequestException as ex:
            print(f"\nError during download:\n{ex}")
    return result


# %%
if session.is_interactive and "data_2022_01_02" not in globals():
    data_2022_01_02 = load_archive_data([(2022, 1), (2022, 2)])
else:
    data_2022_01_02 = globals()["data_2022_01_02"]

# %%
len(data_2022_01_02)

# %%
def generate_date_range(start_year, start_month, end_year, end_month):
    return [
        (year, month)
        for year in range(start_year, end_year + 1)
        for month in range(1, 13)
        if (
            (start_year < year < end_year)
            or (year == start_year and month >= start_month)
            or (year == end_year and month <= end_month)
        )
    ]


# %%
pprint_interactive(generate_date_range(2021, 4, 2022, 4))

# %%
if session.is_interactive and "large_archive_data" not in globals():
    large_archive_data = load_archive_data(generate_date_range(2021, 1, 2022, 4))
else:
    large_archive_data = globals()["large_archive_data"]

# %%
def write_archive_data(
    data, output_path: Path = data_dir_path / "archive_data.json", indent=2
):
    output_path.parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=indent)


# %%
if session.is_interactive:
    write_archive_data(data_2022_01_02, data_dir_path / "archive_2022_01_02.json")

# %%
if session.is_interactive:
    write_archive_data(large_archive_data)

# %%
