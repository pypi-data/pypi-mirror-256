import tomllib
from pathlib import Path


def get_xtml_version():
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as pyproject:
        pyproject_data = tomllib.load(pyproject)
    return pyproject_data["project"]["version"]
