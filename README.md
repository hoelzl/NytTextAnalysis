# Package nytext

Some simple data analysis of New York Times articles.

## Configuration

The project looks for a config file named `~/.nyt.json` containing nested JSON directories with (at least) the following keys:

```json
{
	"nytext": {
		"app-id": "xxx",
		"api-key": "yyy",
		"data-dir": "path-to-directory-where-data-can-be-stored"
	}
}
```

## Installation

To build the project use

```shell script
python -m build
```
in the root directory (i.e., the directory where `pyproject.toml` and `setup.cfg` live).

After building the package you can install it with pip:
```shell script
pip install dist/nytext-0.0.1-py3-none-any.whl
```

To install the package so that it can be used for development purposes
install it with
```shell script
pip install -e .
```
in the root directory.
