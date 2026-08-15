"""Module containing the MapItem component of the map modal."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class MapItem(BaseComponent):
    """Component representing a single club entry in the map modal club list.

    Domain facts:
        - The item is one `.club-item` inside `.map-modal .mapSider .clubList`; the list holds
          one entry per club location for the selected city and category.
        - Clicking the item selects the club, zooms the map to level 15 and centres it on the
          club location, which opens the club info window on the map.
        - The icon box holds either the category icon or, when the club has one, its logo, so
          the icon is located on `.icon-box img` rather than on `img.icon`.
        - It inherits BaseComponent rather than BaseModal because the item is a repeated
          element that has to be constructed from its own root, as in ClubCardComponent.
    """

    TITLE: Locator = (By.CSS_SELECTOR, "div.title")
    NAME: Locator = (By.CSS_SELECTOR, "div.title div.name")
    ICON_BOX: Locator = (By.CSS_SELECTOR, "div.title div.icon-box")
    ICON: Locator = (By.CSS_SELECTOR, "div.title div.icon-box img")
    ADDRESS: Locator = (By.CSS_SELECTOR, "div.address")
    ADDRESS_TEXT: Locator = (By.CSS_SELECTOR, "div.address span.text")

    @allure.step("Get club name of the map item")
    def get_name(self) -> str:
        """Return the club name shown in the item."""
        return self._get_text(self.NAME).strip()

    @allure.step("Get club address of the map item")
    def get_address(self) -> str:
        """Return the club address shown in the item."""
        return self._get_text(self.ADDRESS_TEXT).strip()

    @allure.step("Get icon URL of the map item")
    def get_icon_url(self) -> str:
        """Return the source URL of the category icon or club logo."""
        return self._find_element(self.ICON).get_attribute("src") or ""

    @allure.step("Get icon background colour of the map item")
    def get_icon_background_color(self) -> str:
        """Return the category background colour of the icon box, e.g. 'rgb(19, 194, 194)'."""
        return self._find_element(self.ICON_BOX).value_of_css_property("background-color")

    @allure.step("Select the map item")
    def select(self) -> None:
        """Click the item to select the club and centre the map on it.

        The click lands on the title, which bubbles to the handler on the item itself.
        """
        self._scroll_into_view(self.TITLE)
        self._click(self.TITLE)

    @allure.step("Check if the map item is displayed")
    def is_displayed(self) -> bool:
        """Return whether the item is visible."""
        return self._find_element(self.NAME).is_displayed()
