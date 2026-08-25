"""Page object for the Clubs catalog page of the Speak Ukrainian website."""

from __future__ import annotations

import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.club_details_page import ClubDetailsPage
from pages.components.club_card_component import ClubCardComponent
from pages.components.club_filters_component import ClubFiltersComponent
from pages.components.club_sort_component import ClubSortComponent
from pages.modals.map_modal import MapModal
from pages.types import Locator


class ClubPage(BasePage):
    """Page object representing the Speak Ukrainian clubs catalog page."""

    CLUBS_CONTENT: Locator = (
        By.CSS_SELECTOR,
        "div.content-clubs-list, div.ant-layout-content",
    )
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-box, input[type='search']")
    CLUB_CARDS = (By.CSS_SELECTOR, "div.ant-card, div.type-list-card")
    FILTERS_PANEL = (By.CSS_SELECTOR, 'aside.club-list-sider')
    SORT_PANEL = (By.CSS_SELECTOR, '[data-testid="sort-panel"]')
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div.clubs-not-found")
    PAGINATION_NEXT = (By.CSS_SELECTOR, "li.ant-pagination-next")
    SHOW_MAP_BUTTON = (
        By.CSS_SELECTOR,
        "button.show-map-button, .map-button, "
        "button.ant-btn-icon-only, div.control-box button.ant-btn",
    )

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
    def open(self) -> ClubPage:
        """Open the Clubs page and wait until its main content is visible."""
        self.driver.get(f"{self.get_base_url()}/clubs")
        self._wait_visible(self.CLUBS_CONTENT)
        return self

    def wait_loaded(self) -> ClubPage:
        """Wait until the main Clubs content is visible."""
        self._wait_visible(self.CLUB_CARDS)
        return self

    @allure.step("Wait for search results to match '{keyword}'")
    def wait_for_search_results_contain(self, keyword: str) -> None:
        """Wait until the first club card contains the search keyword."""

        def _first_card_matches(_driver: WebDriver) -> bool:
            try:
                first_card = self._find_element(self.CLUB_CARDS)
                return keyword.lower() in (first_card.get_attribute("textContent") or "").lower()
            except StaleElementReferenceException:
                return False

        self.wait.until(_first_card_matches, message=f"First club card did not contain '{keyword}'")

    @allure.step("Get list of all club cards on page")
    def get_club_cards(self) -> list[ClubCardComponent]:
        """Get list of all club cards on page."""
        self._wait_visible(self.CLUB_CARDS)
        elements = self._find_elements(self.CLUB_CARDS)
        return [ClubCardComponent(elem) for elem in elements]

    @allure.step("Get clubs count")
    def get_clubs_count(self) -> int:
        """Return number of clubs displayed on page."""
        return len(self._find_elements(self.CLUB_CARDS))

    @allure.step("Check if 'No clubs' message is displayed")
    def is_no_results_displayed(self) -> bool:
        """Check if 'No clubs' message is displayed."""
        return len(self._find_elements(self.NO_RESULTS_MESSAGE)) > 0

    @allure.step("Open the first club details page")
    def open_first_club_details(self) -> ClubDetailsPage:
        """Click the 'Детальніше' button of the first club card.

        Returns:
            The club details page of the selected club.
        """
        self._wait_visible(self.CLUB_CARDS)
        self._wait_clickable(self.CLUB_DETAILS_BUTTON).click()
        return ClubDetailsPage(self.driver)

    def filter_club(self) -> ClubFiltersComponent:
        """Return filter object."""
        return ClubFiltersComponent(self.find(self.FILTERS_PANEL))

    def sort_club(self) -> ClubSortComponent:
        """Return sort object."""
        return ClubSortComponent(self._wait_visible(self.CLUBS_CONTENT))

    def is_no_results_message_displayed(self) -> bool:
        """Check if the 'No results' message is displayed."""
        try:
            return self._wait_visible(self.NO_RESULTS_MESSAGE).is_displayed()
        except Exception:
            return False

    @allure.step("Click 'Показати на мапі' button")
    def open_map_modal(self) -> MapModal:
        """Open map modal and return MapModal."""
        self._wait_clickable(self.SHOW_MAP_BUTTON).click()

        map_modal = MapModal(self.driver)

        self.wait.until(lambda _: map_modal.is_displayed())
        return map_modal

    @allure.step("Get first club card")
    def get_first_club_card(self) -> ClubCardComponent:
        """Return the first visible club card."""
        cards = self._find_elements(self.CLUB_CARDS)
        if not cards:
            raise RuntimeError("No club cards found")
        return ClubCardComponent(cards[0])

    @allure.step("Check if panel is displayed")
    def is_panel_visible(self) -> bool:
        """Check if the FILTERS_PANEL is currently displayed."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.FILTERS_PANEL)
            ).is_displayed()
        except Exception:
            return False
