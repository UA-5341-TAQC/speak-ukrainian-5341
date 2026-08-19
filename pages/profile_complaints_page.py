"""Page object for the personal cabinet 'Скарги' (complaints) page of the Speak Ukrainian site.

Located at ``/user/{user_id}/complaints`` inside the personal cabinet
("Особистий кабінет"). The page shows the list of complaints submitted by the
authenticated user.
"""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.types import Locator


class ProfileComplaintsPage(BasePage):
    """Page object for the user's complaints (Скарги) page."""

    # Right-hand content column that holds the complaint list.
    CONTENT: Locator = (By.CSS_SELECTOR, "main .ant-layout-content.messagesContent")
    # Empty-state message shown when no complaints exist yet.
    EMPTY_MESSAGE: Locator = (By.CSS_SELECTOR, ".messagesContent .noMessages")
    # Individual complaint rows once the list is populated.
    COMPLAINT_ITEMS: Locator = (
        By.CSS_SELECTOR,
        ".messagesContent .ant-list .ant-list-item, .messagesContent .ant-list-item",
    )

    def wait_loaded(self) -> "ProfileComplaintsPage":
        """Wait until the complaints content column is visible."""
        self._wait_visible(self.CONTENT)
        return self

    @allure.step("Check if the submitted complaint '{text}' is displayed")
    def is_complaint_displayed(self, text: str) -> bool:
        """Return whether the given complaint text is visible on the page.

        Args:
            text: A distinctive fragment of the submitted complaint (e.g. a
                substring of the 'Опис' value).

        Returns:
            True if the text appears within the complaints list, otherwise False.
        """
        container = self._wait_present(self.CONTENT)
        return text in container.text
