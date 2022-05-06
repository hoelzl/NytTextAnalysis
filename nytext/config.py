# %%
import json
from pathlib import Path


# %%
def load_configuration():
    config_file_path = Path.home() / ".nyt.json"
    if config_file_path.exists():
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            return json.load(config_file)
    else:
        raise FileNotFoundError("Could not find configuration file '~/.nyt.json'.")

# %%
