"""Club Card Sort Component for the Speak Ukrainian website."""

from typing import Literal

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ClubSortComponent(BaseComponent):
    """Component for Club Card Filters Component (Advanced search)."""

    # Toggle icon that opens the sider with sorting controls
    SEARCH_ICON: Locator = (By.CSS_SELECTOR, "span.anticon.anticon-control.advanced-icon")
    SORT_CONTROL: Locator = (By.CSS_SELECTOR, "div.club-control-sort")

    # Sort options
    ALPHABET_SORT_LABEL: Locator = (
        By.XPATH,
        "//span[contains(@class, 'control-sort-option') and contains(., 'за алфавітом')]",
    )
    RATE_SORT_LABEL: Locator = (
        By.XPATH,
        "//span[contains(@class, 'control-sort-option') and contains(., 'за рейтингом')]",
    )
    ACTIVE_SORT_OPTION: Locator = (
        By.XPATH,
        "//span[contains(@class, 'control-sort-option') and "
        "(contains(@class, 'checked') or contains(@class, 'active'))]",
    )

    # Direction arrows
    ARROW_UP: Locator = (By.CSS_SELECTOR, "span.anticon.anticon-arrow-up.control-sort-arrow")
    ARROW_DOWN: Locator = (By.CSS_SELECTOR, "span.anticon.anticon-arrow-down.control-sort-arrow")

    # Club cards
    CLUB_CARDS: Locator = (By.CSS_SELECTOR, ".club-list .club-item")
    CLUB_TITLE_NAMES: Locator = (By.CSS_SELECTOR, ".club-list .title .name")
    CLUB_RATING: Locator = (By.CSS_SELECTOR, "ul.ant-rate.rating")
    RATING_STAR_FULL: Locator = (By.CSS_SELECTOR, ".ant-rate-star-full")
    RATING_STAR_HALF: Locator = (By.CSS_SELECTOR, ".ant-rate-star-half")

    SPINNER: Locator = (By.CSS_SELECTOR, ".ant-spin-spinning")

    def __init__(self, root: WebElement) -> None:
        """Initialize the base component with a WebElement root."""
        super().__init__(root)

    #Helpers

    def _is_element_active(self, locator: Locator) -> bool:
        """Check whether an element (or its parent) is in an active/checked state."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        parent = element.find_element(By.XPATH, "..")

        element_classes = (element.get_attribute("class") or "").split()
        parent_classes = (parent.get_attribute("class") or "").split()
        classes = set(element_classes) | set(parent_classes)

        is_checked_attr = (
            element.get_attribute("aria-checked") == "true"
            or parent.get_attribute("aria-checked") == "true"
        )
        has_active_class = any(cls in ("checked", "active") for cls in classes)

        return has_active_class or is_checked_attr

    def _wait_for_clubs_to_reload(self) -> None:
        """Wait for the club list to reload after a sorting action."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.SPINNER))
        except Exception:
            pass
        self.wait.until(EC.invisibility_of_element_located(self.SPINNER))

    # Advanced search toggle

    @allure.step("Click on 'Advanced search' icon")
    def toggle_advanced_search(self) -> "ClubSortComponent":
        """Click the advanced-search icon to open/close the sider with filters."""
        icon = self.wait.until(EC.element_to_be_clickable(self.SEARCH_ICON))
        icon.click()
        return self

    @allure.step("Check if sort control is displayed")
    def is_sort_visible(self) -> bool:
        """Check if the sort control is currently displayed."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.SORT_CONTROL)
            ).is_displayed()
        except Exception:
            return False

    @allure.step("Open sider with filters")
    def ensure_sort_displayed(self) -> "ClubSortComponent":
        """Open the sider with filters/sorting if it is not already open."""
        if not self.is_sort_visible():
            self.toggle_advanced_search()
        return self


    # Common helpers (alphabet/rating sorting)

    @allure.step("Get sorting direction from arrow state")
    def get_current_direction(self) -> Literal["asc", "desc"]:
        """Get the current sort direction based on which arrow is active."""
        arrow_up = self.wait.until(EC.visibility_of_element_located(self.ARROW_UP))
        classes = (arrow_up.get_attribute("class") or "").split()
        return "asc" if "active" in classes else "desc"

    def is_arrow_up_active(self) -> bool:
        """Return True if the ascending-direction arrow is active."""
        return self._is_element_active(self.ARROW_UP)

    def is_arrow_down_active(self) -> bool:
        """Return True if the descending-direction arrow is active."""
        return self._is_element_active(self.ARROW_DOWN)

    @allure.step("Get list of club titles in current order")
    def get_club_titles(self) -> list[str]:
        """Return club titles in the order they currently appear on the page."""
        elements = self._find_elements(self.CLUB_TITLE_NAMES)
        return [el.text.strip() for el in elements]

    @allure.step("Get active sort option label")
    def get_active_sort_option(self) -> str:
        """Return the text of the currently active sorting option."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.ACTIVE_SORT_OPTION)
            ).text.strip()
        except Exception:
            return self._find_element(self.SORT_CONTROL).text.strip()

    # Sorting by rating (за рейтингом)

    @allure.step("Select 'sort by rating' option")
    def sort_by_rate(self) -> "ClubSortComponent":
        """Select the 'sort by rating' option."""
        element = self.wait.until(EC.element_to_be_clickable(self.RATE_SORT_LABEL))
        element.click()
        self._wait_for_clubs_to_reload()
        return self

    @allure.step("Set sorting direction by rating to '{direction}'")
    def set_sort_direction_by_rating(
        self, direction: Literal["asc", "desc"]
    ) -> "ClubSortComponent":
        """Ensure rating sort direction matches the requested one."""
        self.sort_by_rate()
        if self.get_current_direction() != direction:
            arrow_locator = self.ARROW_UP if direction == "asc" else self.ARROW_DOWN
            self.wait.until(EC.element_to_be_clickable(arrow_locator)).click()
            self._wait_for_clubs_to_reload()
        return self


    # Sorting by alphabet (за алфавітом)

    @allure.step("Actual alphabet sort direction from displayed titles")
    def get_actual_alphabet_direction(self) -> Literal["asc", "desc", "unknown"]:
        """Determine direction by comparing actual club titles with their sorted version."""
        titles = self.get_club_titles()
        if not titles:
            raise ValueError("Club list is empty, cannot determine sort direction")

        if titles == sorted(titles):
            return "asc"
        if titles == sorted(titles, reverse=True):
            return "desc"
        return "unknown"

    def _is_alphabet_sort_active(self) -> bool:
        """Check whether the alphabet sort option is explicitly marked active in the UI."""
        return self._is_element_active(self.ALPHABET_SORT_LABEL)

    @allure.step("Get current alphabet sorting state")
    def get_alphabet_sort_state(self) -> Literal["asc", "desc", "unknown"]:
        """Get the current alphabet sort direction."""
        
        if self._is_alphabet_sort_active():
            return self.get_current_direction()
        return self.get_actual_alphabet_direction()

    @allure.step("Click on 'alphabet' sorting option")
    def click_alphabet_sort(self) -> "ClubSortComponent":
        """Click the alphabet sort label."""
        element = self.wait.until(EC.element_to_be_clickable(self.ALPHABET_SORT_LABEL))
        element.click()
        self._wait_for_clubs_to_reload()
        return self

    @allure.step("Ensure default alphabet sorting is applied (asc, а -> я)")
    def sort_by_alphabet(self) -> "ClubSortComponent":
        """Ensure ascending alphabet sort is applied."""
        self.ensure_sort_displayed()

        if self.get_alphabet_sort_state() == "asc":
            return self  # already default asc, or explicitly selected asc

        self.click_alphabet_sort()  # currently desc -> flip back to asc
        return self

    @allure.step("Toggle alphabet sorting direction (asc <-> desc)")
    def toggle_alphabet_sort_direction(self) -> "ClubSortComponent":
        """Click the alphabet sort option to flip the current direction."""
        direction_before = self.get_alphabet_sort_state()
        expected_direction = "desc" if direction_before == "asc" else "asc"

        self.click_alphabet_sort()

        direction_after = self.get_alphabet_sort_state()
        assert direction_after == expected_direction, (
            f"Expected alphabet sort direction '{expected_direction}' "
            f"after toggle, got '{direction_after}'"
        )
        return self

    @allure.step("Set alphabet sorting direction explicitly to '{direction}'")
    def set_sort_direction_by_alphabet(
        self, direction: Literal["asc", "desc"]
    ) -> "ClubSortComponent":
        """Ensure alphabet sort is set to the requested direction, from any starting state."""
        self.ensure_sort_displayed()

        if self.get_alphabet_sort_state() != direction:
            self.click_alphabet_sort()

        return self
