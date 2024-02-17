import tomllib
from pathlib import Path

from xtml.torch import TrainConfig, DataLoaderConfig, TorchTrainer


def get_xtml_version():
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as pyproject:
        pyproject_data = tomllib.load(pyproject)
    return pyproject_data["project"]["version"]

__version__ = get_xtml_version()
