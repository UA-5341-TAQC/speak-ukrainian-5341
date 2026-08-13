"""Page object for the Clubs catalog page of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from data.config import Config
from pages.base_page import BasePage
from pages.components.club_card_component import ClubCardComponent
from pages.components.club_filters_component import ClubFiltersComponent
from pages.components.club_sort_component import ClubSortComponent


class ClubPage(BasePage):
    """Page object representing the Speak Ukrainian clubs catalog page."""

    URL = f"{Config.BASE_UI_URL.rstrip('/')}/clubs"
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-box, input[type='search']")
    CLUB_CARDS = (By.CSS_SELECTOR, "div.ant-card, div.type-list-card")
    FILTERS_PANEL = (By.CSS_SELECTOR, '[data-testid="filters-panel"]')
    SORT_PANEL = (By.CSS_SELECTOR, '[data-testid="sort-panel"]')
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div.clubs-not-found")
    PAGINATION_NEXT = (By.CSS_SELECTOR, "li.ant-pagination-next")

    def __init__(self, driver: WebDriver):
        """Initialize the News page with a WebDriver."""
        super().__init__(driver)

    def find(self, locator):
        """Helper to find one element."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        """Helper to find all elements for locator."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))


    @allure.step("Open the Clubs page")
    def open(self) -> "ClubPage":
        """Open the Clubs page and wait until its main content is visible."""
        self.driver.get(self.URL)
        self._wait_visible(self.CLUB_CARDS)

    def wait_loaded(self) -> "ClubPage":
        """Wait until the main Clubs content is visible."""
        self._wait_visible(self.CLUB_CARDS)
        return self
    """
    @allure.step("Get list of all club cards on page")
    def get_club_cards(self) -> list[ClubCardComponent]:
        Get list of all club cards on page.
        self.wait.until(EC.presence_of_element_located(self.CLUB_CARDS))
        elements = self.driver.find_elements(self.CLUB_CARDS)
        return [ClubCardComponent(elem) for elem in elements]
    """

    @allure.step("Get clubs count")
    def get_clubs_count(self) -> int:
        """Return number of clubs displayed on page."""
        return len(self.driver.find_elements(self.CLUB_CARDS))

    @allure.step("Check if 'No clubs' message is displayed")
    def is_no_results_displayed(self) -> bool:
        """Check if 'No clubs' message is displayed."""
        return len(self.driver.find_elements(*self._NO_RESULTS_MESSAGE)) > 0

    def filter(self) -> ClubFiltersComponent:
        """Return filter object."""
        return ClubFiltersComponent(self.filter(self.FILTERS_PANEL))

    def sort(self) -> ClubSortComponent:
        """Return sort object."""
        return ClubSortComponent(self.find(self.SORT_PANEL))

    @allure.step("Get first club card")
    def get_first_club_card(self) -> ClubCardComponent:
        """Return the first visible club card."""
        cards = self._find_elements(self.CLUB_CARDS)
        if not cards:
            raise RuntimeError("No club cards found")
        return ClubCardComponent(cards[0])
