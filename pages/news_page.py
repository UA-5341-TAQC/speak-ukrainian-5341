"""Page Object for the public News list page."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.components.news_list_component import NewsListComponent
from pages.components.news_pagination_component import NewsPaginationComponent
from pages.types import Locator


class NewsPage(BasePage):
    """Represents the public News page."""

    NEWS_CONTENT: Locator = (By.CSS_SELECTOR, ".news-content")
    NEWS_LIST: Locator = (By.CSS_SELECTOR, ".news-content > div:first-child")
    PAGINATION: Locator = (
        By.CSS_SELECTOR,
        ".news-content ul.ant-pagination.pagination",
    )

    def __init__(self, driver: WebDriver):
        """Initialize the News page with a WebDriver."""
        super().__init__(driver)

    @allure.step("Open the News page")
    def open(self) -> "NewsPage":
        """Open the News page and wait until its main content is visible."""
        self.driver.get(f"{self.get_base_url()}/news")
        self._wait_visible(self.NEWS_CONTENT)
        return self

    def wait_loaded(self) -> "NewsPage":
        """Wait until the main News content is visible."""
        self._wait_visible(self.NEWS_CONTENT)
        return self

    def get_news_list(self) -> NewsListComponent:
        """Return the News list component."""
        root = self._wait_visible(self.NEWS_LIST)
        return NewsListComponent(root)

    def get_pagination(self) -> NewsPaginationComponent:
        """Return the News pagination component."""
        root = self._wait_visible(self.PAGINATION)
        return NewsPaginationComponent(root)
