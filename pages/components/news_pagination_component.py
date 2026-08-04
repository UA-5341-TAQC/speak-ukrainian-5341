"""Component Object for News page pagination."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.types import Locator


class NewsPaginationComponent(BaseComponent):
    """Represents Ant Design pagination on the News list page."""

    PAGE_ITEMS: Locator = (By.CSS_SELECTOR, "li.ant-pagination-item")
    ACTIVE_PAGE: Locator = (By.CSS_SELECTOR, "li.ant-pagination-item-active")
    NEXT_BUTTON: Locator = (By.CSS_SELECTOR, "li.ant-pagination-next button")
    PREVIOUS_BUTTON: Locator = (By.CSS_SELECTOR, "li.ant-pagination-prev button")
    NEXT_CONTAINER: Locator = (By.CSS_SELECTOR, "li.ant-pagination-next")
    PREVIOUS_CONTAINER: Locator = (By.CSS_SELECTOR, "li.ant-pagination-prev")

    def __init__(self, root: WebElement):
        """Initialize the news pagination component."""
        super().__init__(root)

    def get_current_page(self) -> int:
        """Return the active page number."""
        return int(self._wait_visible(self.ACTIVE_PAGE).text.strip())

    def get_page_numbers(self) -> list[int]:
        """Return visible page numbers."""
        self._wait_present(self.PAGE_ITEMS)
        return [
            int(element.text.strip())
            for element in self._find_elements(self.PAGE_ITEMS)
            if element.text.strip().isdigit()
        ]

    @allure.step("Open News page number {page_number}")
    def click_page(self, page_number: int) -> None:
        """Open a page by its visible page number."""
        locator: Locator = (
            By.CSS_SELECTOR,
            f"li.ant-pagination-item[title='{page_number}'] a",
        )
        self._wait_clickable(locator).click()

    @allure.step("Open the next News page")
    def click_next(self) -> None:
        """Open the next News page."""
        self._wait_clickable(self.NEXT_BUTTON).click()

    @allure.step("Open the previous News page")
    def click_previous(self) -> None:
        """Open the previous News page."""
        self._wait_clickable(self.PREVIOUS_BUTTON).click()

    def is_next_enabled(self) -> bool:
        """Return False when the Next control is disabled."""
        classes = self._find_element(
            self.NEXT_CONTAINER
        ).get_attribute("class") or ""
        return "ant-pagination-disabled" not in classes

    def is_previous_enabled(self) -> bool:
        """Return False when the Previous control is disabled."""
        classes = self._find_element(
            self.PREVIOUS_CONTAINER
        ).get_attribute("class") or ""
        return "ant-pagination-disabled" not in classes
