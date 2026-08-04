"""Types for page/components/modals."""

from typing import TypeAlias

# Selenium expects tuple[str, str] e.g. (By.XPATH, "//div")
Locator: TypeAlias = tuple[str, str]
