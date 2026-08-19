"""Page object for the Clubs catalog page of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.club_details_page import ClubDetailsPage

# from pages.components.club_card_component import ClubCardComponent
from pages.components.club_filters_component import ClubFiltersComponent
from pages.components.club_sort_component import ClubSortComponent
from pages.types import Locator


class ClubPage(BasePage):
    """Page object representing the Speak Ukrainian clubs catalog page."""

    CLUBS_CONTENT: Locator = (By.TAG_NAME, "body")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-box, input[type='search']")
    CLUB_CARDS = (By.CSS_SELECTOR, "div.ant-card, div.type-list-card")
    FILTERS_PANEL = (By.CSS_SELECTOR, '[data-testid="filters-panel"]')
    SORT_PANEL = (By.CSS_SELECTOR, '[data-testid="sort-panel"]')
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div.clubs-not-found")
    PAGINATION_NEXT = (By.CSS_SELECTOR, "li.ant-pagination-next")

    # "Детальніше" ("More details") button of a club card on the catalog page.
    CLUB_DETAILS_BUTTON: Locator = (By.CSS_SELECTOR, "a.details-button")

    def __init__(self, driver: WebDriver):
        """Initialize the News page with a WebDriver."""
        super().__init__(driver)

    def find(self, locator: Locator) -> WebElement:
        """Helper to find one element."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: Locator) -> list[WebElement]:
        """Helper to find all elements for locator."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Open the Clubs page")
    def open(self) -> "ClubPage":
        """Open the Clubs page and wait until its main content is visible."""
        self.driver.get(f"{self.get_base_url()}/clubs")
        self._wait_visible(self.CLUBS_CONTENT)
        return self

    def wait_loaded(self) -> "ClubPage":
        """Wait until the main Clubs content is visible."""
        self._wait_visible(self.CLUBS_CONTENT)
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
        """Get the count of club cards currently displayed on the page."""
        elements = self.wait.until(lambda _: self._find_elements(self.CLUB_CARDS))
        return len(elements)

    @allure.step("Check if 'No clubs' message is displayed")
    def is_no_results_displayed(self) -> bool:
        """Check if 'No clubs' message is displayed."""
        return len(self.driver.find_elements(*self.NO_RESULTS_MESSAGE)) > 0

    @allure.step("Open the first club details page")
    def open_first_club_details(self) -> "ClubDetailsPage":
        """Click the 'Детальніше' button of the first club card.

        Returns:
            The club details page of the selected club.
        """
        self._wait_visible(self.CLUB_CARDS)
        self._wait_clickable(self.CLUB_DETAILS_BUTTON).click()
        return ClubDetailsPage(self.driver)

    def filter(self) -> ClubFiltersComponent:
        """Return filter object."""
        return ClubFiltersComponent(self._wait_visible(self.CLUBS_CONTENT))

    def sort(self) -> ClubSortComponent:
        """Return sort object."""
        return ClubSortComponent(self._wait_visible(self.CLUBS_CONTENT))
