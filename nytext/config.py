# %%
import json
from pathlib import Path
import nytext


# %%
def load_json_configuration():
    config_file_path = Path.home() / ".nyt.json"
    if config_file_path.exists():
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            return json.load(config_file)
    else:
        raise FileNotFoundError("Could not find configuration file '~/.nyt.json'.")


# %%
def load_configuration():
    config_dir = load_json_configuration()
    return config_dir


# %%
def get_archive_root_path(check_path_exists=True):
    config = load_configuration()
    dir_str = config["nytext"].get("news-dir", None)
    if dir_str is None:
        archive_path = Path(nytext.__file__).parent / "articles"
    else:
        archive_path = Path(dir_str)
    if check_path_exists:
        assert archive_path.exists(), f"Archive path {archive_path!r} does not exist!"
    return archive_path


# %%
def get_archive_file_path(year, month, check_path_exists=True):
    root_path = get_archive_root_path(check_path_exists)
    return root_path / f"{year}/{month}.json"