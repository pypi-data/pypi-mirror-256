from typing import List

import os

from dataclasses import dataclass


ENV_FILE = "workflows/.env"


class ConfigNotAvailable(Exception):
    pass


@dataclass
class Config:
    name: str
    description: str


def require_config(config: Config) -> str:
    env_name = config.name
    if env_name not in os.environ:
        raise ConfigNotAvailable(
            f"""Config '{env_name}' is not defined as an environment variable. 
Please set it or add it to your 'workflows/.env' file."""
        )
    return os.environ[env_name]
