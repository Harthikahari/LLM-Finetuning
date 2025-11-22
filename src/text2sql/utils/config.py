"""Configuration management for Text2SQL."""

import logging
import yaml
import json
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from file."""
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    if config_path.suffix == ".yaml" or config_path.suffix == ".yml":
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    elif config_path.suffix == ".json":
        with open(config_path, "r") as f:
            config = json.load(f)
    else:
        raise ValueError(f"Unsupported config format: {config_path.suffix}")

    logger.info(f"Loaded config from {config_path}")
    return config


def save_config(config: Dict[str, Any], save_path: str):
    """Save configuration to file."""
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    if save_path.suffix == ".yaml" or save_path.suffix == ".yml":
        with open(save_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
    elif save_path.suffix == ".json":
        with open(save_path, "w") as f:
            json.dump(config, f, indent=2)
    else:
        raise ValueError(f"Unsupported config format: {save_path.suffix}")

    logger.info(f"Saved config to {save_path}")
