# %%
import json
from pathlib import Path

import requests
from nbex.interactive import session, print_interactive, pprint_interactive
from nytext.config import load_configuration, get_archive_file_path

# %%
config = load_configuration()
project_data = config["nytext"]
app_id = project_data["app-id"]
api_key = project_data["api-key"]
data_dir_path = Path(project_data["data-dir"])
url_str = project_data["url"]


# %%
def download_raw_archive_data_for_month(year, month):
    # assert year >= 1851
    # assert 1 <= month <= 12
    return requests.get(
        url_str.format(year=year, month=month),
        params={"api-key": api_key},
    )


# %%
def download_archive_data_for_month(year, month):
    r = download_raw_archive_data_for_month(year, month)
    if 200 <= r.status_code < 300:
        return r.json()["response"].get("docs", [])
    else:
        raise requests.RequestException(
            f"Invalid request (code {r.status_code}): {r!r}."
        )


# %%
if session.is_interactive and "data_2022_01" not in globals():
    data_2022_01 = download_archive_data_for_month(2022, 1)


# %%
def download_archive_data(months):
    result = []
    for year, month in months:
        print(f"Trying to download archive data for {year}/{month}...", end="", flush=True)
        try:
            data = download_archive_data_for_month(year, month)
            result.extend(data)
            print(f"got {len(data)} items.")
        except requests.RequestException as ex:
            print(f"\nError during download:\n{ex}")
    return result


# %%
if session.is_interactive and "data_2022_01_02" not in globals():
    data_2022_01_02 = download_archive_data([(2022, 1), (2022, 2)])


# %%
def generate_date_range(start_year, start_month, end_year, end_month):
    return tuple(
        (year, month)
        for year in range(start_year, end_year + 1)
        for month in range(1, 13)
        if (
            (start_year == end_year and start_month <= month <= end_month)
            or (
                start_year < end_year
                and (
                    (start_year < year < end_year)
                    or (year == start_year and month >= start_month)
                    or (year == end_year and month <= end_month)
                )
            )
        )
    )


# %%
print_interactive(generate_date_range(2021, 4, 2022, 4))
print_interactive(generate_date_range(2021, 1, 2021, 4))

# %%
default_date_range = generate_date_range(2021, 1, 2022, 4)

# %%
# This will issue a rather large number of requests.
#
# if session.is_interactive and "large_archive_data" not in globals():
#     large_archive_data = download_archive_data(default_date_range)
# else:
#     large_archive_data = globals()["large_archive_data"]

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
# if session.is_interactive:
#     write_archive_data(large_archive_data)


# %%
def load_or_download_archive_data(
    local_path: Path = data_dir_path / "archive_data.json", months=default_date_range
):
    if local_path.exists():
        with open(local_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        data = download_archive_data(months)
        write_archive_data(data, local_path)
        return data


# %%
if session.is_interactive:
    large_archive_data = load_or_download_archive_data()
    print(f"Archive data has {len(large_archive_data)} entries.")

# %%
session.forced_interactive_value = None


# %%
def download_and_save_raw_archive_data(months):
    for year, month in months:
        print(f"Downloading raw archive data for {year}/{month}.")
        response = download_raw_archive_data_for_month(year, month)
        if 200 <= response.status_code < 300:
            path = get_archive_file_path(year, month, check_path_exists=False)
            path.parent.mkdir(exist_ok=True, parents=True)
            print(f"  Writing to {path}.")
            write_archive_data(response.json(), path)
        else:
            print(f"  Not writing file: status code {response.status_code}")


# %%
if session.is_interactive:
	download_and_save_raw_archive_data(generate_date_range(2022, 1, 2022, 4))

# %%
