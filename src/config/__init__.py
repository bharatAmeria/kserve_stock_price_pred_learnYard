from box import Box
import yaml
from pathlib import Path

def load_config(path: Path = Path("config.yaml")):
    with open(path, "r") as f:
        return Box(yaml.safe_load(f))  # Allows dot-access

CONFIG = load_config()
