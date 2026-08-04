from selenium.webdriver.remote.webelement import WebElement

from pages.base import Base


class BaseModal(Base):
    """Base class for all modals, representing an encapsulated UI component (COM)."""

    def __init__(self, root: WebElement):
        """Initialize the base modal with its root WebElement."""
        super().__init__(root)
