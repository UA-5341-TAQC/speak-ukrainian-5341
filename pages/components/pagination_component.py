"""Component representing Ant Design pagination controls."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class PaginationComponent(BaseComponent):
    """Component representing an Ant Design `ul.ant-pagination` control."""

    PAGE_ITEMS: Locator = (
        By.CSS_SELECTOR,
        "li.ant-pagination-item",
    )
    ACTIVE_PAGE: Locator = (
        By.CSS_SELECTOR,
        "li.ant-pagination-item-active",
    )
    PREVIOUS_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "li.ant-pagination-prev",
    )
    NEXT_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "li.ant-pagination-next",
    )

    @allure.step("Get current pagination page")
    def get_current_page(self) -> int:
        """Get the number of the currently active page."""
        return int(self._find_element(self.ACTIVE_PAGE).text)

    @allure.step("Get available pagination page numbers")
    def get_page_numbers(self) -> list[int]:
        """Get the page numbers currently rendered as clickable items."""
        return [int(el.text) for el in self._find_elements(self.PAGE_ITEMS)]

    @allure.step("Click pagination page {page_number}")
    def click_page(self, page_number: int) -> None:
        """Click a pagination item to jump to that page.

        Args:
            page_number: The page number to open.

        Raises:
            ValueError: If page_number is not currently a clickable page item.
        """
        locator: Locator = (
            By.CSS_SELECTOR,
            f'li.ant-pagination-item[title="{page_number}"]',
        )
        pages = self.get_page_numbers()
        if page_number not in pages:
            raise ValueError(f"Page {page_number} not available (options: {pages}).")
        self._wait_clickable(locator).click()

    @allure.step("Click pagination 'Next' button")
    def click_next(self) -> None:
        """Click the 'Next' pagination button."""
        self._wait_clickable(self.NEXT_BUTTON).click()

    @allure.step("Click pagination 'Previous' button")
    def click_previous(self) -> None:
        """Click the 'Previous' pagination button."""
        self._wait_clickable(self.PREVIOUS_BUTTON).click()

    @allure.step("Check if pagination 'Next' button is enabled")
    def is_next_enabled(self) -> bool:
        """Return whether the 'Next' pagination button is enabled."""
        return self._find_element(self.NEXT_BUTTON).get_attribute("aria-disabled") == "false"

    @allure.step("Check if pagination 'Previous' button is enabled")
    def is_previous_enabled(self) -> bool:
        """Return whether the 'Previous' pagination button is enabled."""
        return self._find_element(self.PREVIOUS_BUTTON).get_attribute("aria-disabled") == "false"
