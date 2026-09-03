"""Configuration module to load environment variables from a .env file.

This module uses the `python-dotenv` package to load environment variables from
a .env file located in the parent directory of this script.
The `Config` class provides easy access to these variables as class attributes.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Override existing environment variables so that .env always wins over any
# ambient shell variables (e.g. a USER_EMAIL that may be inherited from the OS).
load_dotenv(override=True)

ENV_PATH = Path(__file__).parent.parent / ".env"


class Config:
    """Configuration class to load environment variables."""

    BASE_UI_URL: str = os.getenv("BASE_UI_URL", "")
    BASE_API_URL: str = os.getenv("BASE_API_URL", "")
    IMPLICITY_WAIT: int = int(os.getenv("IMPLICITY_WAIT", "10"))
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10"))
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() in ("true", "1", "t")
    WINDOW_SIZE: str = os.getenv("WINDOW_SIZE", "1600,1000")
    MAXIMIZE: bool = os.getenv("MAXIMIZE", "False").lower() in ("true", "1", "t")
    USER_NAME: str = os.getenv("USER_NAME", "")
    USER_PASSWORD: str = os.getenv("USER_PASSWORD", "")
    USER_EMAIL: str = os.getenv("USER_EMAIL", "")
    MANAGER_EMAIL: str = os.getenv("MANAGER_EMAIL", "")
    MANAGER_PASSWORD: str = os.getenv("MANAGER_PASSWORD", "")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "")

    API_USER_EMAIL: str = os.getenv("API_USER_EMAIL", "")
    API_USER_PASSWORD: str = os.getenv("API_USER_PASSWORD", "")
