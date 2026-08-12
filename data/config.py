"""Configuration module to load environment variables from a .env file.

This module uses the `python-dotenv` package to load environment variables from
a .env file located in the parent directory of this script.
The `Config` class provides easy access to these variables as class attributes.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ENV_PATH = Path(__file__).parent.parent / ".env"


class Config:
    """Configuration class to load environment variables."""

    BASE_UI_URL: str = os.getenv("BASE_UI_URL", "https://speak-ukrainian.org.ua")
    BASE_API_URL: str = os.getenv("BASE_API_URL", "")
    IMPLICITY_WAIT: int = int(os.getenv("IMPLICITY_WAIT", "10"))
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10"))
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() in ("true", "1", "t")
    USER_NAME: str = os.getenv("USER_NAME", "")
    USER_PASSWORD: str = os.getenv("USER_PASSWORD", "")
    USER_EMAIL: str = os.getenv("USER_EMAIL", "")
