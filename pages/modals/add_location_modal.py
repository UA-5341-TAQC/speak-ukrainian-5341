from __future__ import annotations

import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class AddLocationModal(BaseModal):
    """Page object for the Add Location modal window."""

    MODAL_CONTENT: Locator = (By.CSS_SELECTOR, "div.ant-modal-content:has(div.add-club-locations)")
    CLOSE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content:has(div.add-club-locations) button.ant-modal-close",
    )
    MODAL_TITLE: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content:has(div.add-club-locations) div.add-club-header",
    )

    LOCATION_NAME_INPUT: Locator = (By.ID, "name")

    CITY_NAME_FIELD: Locator = (By.CSS_SELECTOR, "div.ant-select-selector:has(input#cityName)")
    CITY_NAME_DROPDOWN: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:has(div#cityName_list)",
    )
    CITY_NAME_OPTIONS: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:has(div#cityName_list) .ant-select-item-option",
    )
    SELECTED_CITY = (
        By.CSS_SELECTOR,
        "div.ant-select-selector:has(input#cityName) span.ant-select-selection-item",
    )

    CITY_DISTRICT_NAME_FIELD: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-selector:has(input#districtName)",
    )
    CITY_DISTRICT_NAME_DROPDOWN: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:has(div#districtName_list)",
    )
    CITY_DISTRICT_NAME_OPTIONS: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:has(div#districtName_list) .ant-select-item-option",
    )
    SELECTED_CITY_DISTRICT = (
        By.CSS_SELECTOR,
        "div.ant-select-selector:has(input#districtName) span.ant-select-selection-item",
    )
    EMPTY_DISTRICT_LIST_TEXT: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:has(div#districtName_list) .ant-empty-description",
    )

    STATION_NAME_FIELD: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-selector:has(input#stationName)",
    )
    STATION_NAME_DROPDOWN: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:has(div#stationName_list)",
    )
    STATION_NAME_OPTIONS: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:has(div#stationName_list) .ant-select-item-option",
    )
    SELECTED_STATION = (
        By.CSS_SELECTOR,
        "div.ant-select-selector:has(input#stationName) span.ant-select-selection-item",
    )
    EMPTY_STATION_LIST_TEXT: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:has(div#stationName_list) .ant-empty-description",
    )

    ADDRESS_INPUT: Locator = (By.ID, "address")
    COORDINATES_INPUT: Locator = (By.ID, "coordinates")
    PHONE_INPUT: Locator = (By.ID, "phone")

    ADD_BUTTON: Locator = (By.CSS_SELECTOR, "div.add-club-add-location-button button")

    INFO_ICON: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content:has(div.add-club-locations) span.info-icon",
    )
    FEEDBACK_ICON: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content:has(div.add-club-locations) span.ant-form-item-feedback-icon",
    )
    FIELD_ERROR_MESSAGES: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content:has(div.add-club-locations) div.ant-form-item-explain-error",
    )

    def is_opened(self) -> bool:
        """Check whether the Add Location modal is currently opened."""
        return self._find_element(self.MODAL_CONTENT).is_displayed()

    @allure.step("Close Add Location modal")
    def close(self) -> None:
        """Close the Add Location modal by clicking the close button."""
        self._wait_clickable(self.CLOSE_BUTTON).click()

    @allure.step("Get modal title text")
    def get_title(self) -> str:
        """Return the header text of the modal."""
        return self._find_element(self.MODAL_TITLE).text.strip()

    @allure.step("Enter location name: '{name}'")
    def enter_location_name(self, name: str) -> AddLocationModal:
        """Enter a location name into the location name field."""
        el = self._find_element(self.LOCATION_NAME_INPUT)
        self._clear(el)
        el.send_keys(name)
        return self

    @allure.step("Clear location name")
    def clear_location_name(self) -> AddLocationModal:
        """Clear the location name field."""
        self._clear(self._find_element(self.LOCATION_NAME_INPUT))
        return self

    @allure.step("Open city dropdown")
    def open_city_dropdown(self) -> AddLocationModal:
        """Open the city selection dropdown."""
        self._wait_clickable(self.CITY_NAME_FIELD).click()
        return self

    def _select_dropdown_option(self, options_locator: Locator, text: str) -> None:
        """Helper to safely select a dropdown option by text, handling stale elements."""

        def _predicate(_: object) -> bool:
            try:
                options = self._find_elements(options_locator)
                for option in options:
                    if option.text.strip() == text:
                        option.click()
                        return True
                return False
            except StaleElementReferenceException:
                return False

        self.wait.until(_predicate, message=f"Failed to select option '{text}'")

    @allure.step("Select city: '{city_name}'")
    def select_city(self, city_name: str) -> AddLocationModal:
        """Select a city from the city dropdown."""
        self.open_city_dropdown()
        self._select_dropdown_option(self.CITY_NAME_OPTIONS, city_name)
        return self

    @allure.step("Get selected city text")
    def get_selected_city(self) -> str:
        """Return the currently selected city name."""
        return self._find_element(self.SELECTED_CITY).text.strip()

    @allure.step("Check if city dropdown is visible")
    def is_city_dropdown_visible(self) -> bool:
        """Check whether the city dropdown is displayed."""
        try:
            return self._find_element(self.CITY_NAME_DROPDOWN).is_displayed()
        except Exception:
            return False

    @allure.step("Get city options count")
    def get_city_options_count(self) -> int:
        """Return the number of available city options."""
        return len(self._find_elements(self.CITY_NAME_OPTIONS))

    @allure.step("Open district dropdown")
    def open_district_dropdown(self) -> AddLocationModal:
        """Open the district selection dropdown."""
        self._wait_clickable(self.CITY_DISTRICT_NAME_FIELD).click()
        return self

    @allure.step("Select district: '{district_name}'")
    def select_district(self, district_name: str) -> AddLocationModal:
        """Select a district from the district dropdown."""
        self.open_district_dropdown()
        self._select_dropdown_option(self.CITY_DISTRICT_NAME_OPTIONS, district_name)
        return self

    @allure.step("Get selected district text")
    def get_selected_district(self) -> str:
        """Return the currently selected district name."""
        return self._find_element(self.SELECTED_CITY_DISTRICT).text.strip()

    @allure.step("Check if district dropdown is empty")
    def is_district_dropdown_empty(self) -> bool:
        """Check whether the district dropdown contains no options."""
        try:
            text = self._find_elements(self.EMPTY_DISTRICT_LIST_TEXT)[0].text.strip()
            return text == "No data"
        except Exception:
            return False

    @allure.step("Open station dropdown")
    def open_station_dropdown(self) -> AddLocationModal:
        """Open the station selection dropdown."""
        self._wait_clickable(self.STATION_NAME_FIELD).click()
        return self

    @allure.step("Select station: '{station_name}'")
    def select_station(self, station_name: str) -> AddLocationModal:
        """Select a station from the station dropdown."""
        self.open_station_dropdown()
        self._select_dropdown_option(self.STATION_NAME_OPTIONS, station_name)
        return self

    @allure.step("Get selected station text")
    def get_selected_station(self) -> str:
        """Return the currently selected station name."""
        return self._find_element(self.SELECTED_STATION).text.strip()

    @allure.step("Check if station dropdown is empty")
    def is_station_dropdown_empty(self) -> bool:
        """Check whether the station dropdown contains no options."""
        try:
            text = self._find_elements(self.EMPTY_STATION_LIST_TEXT)[0].text.strip()
            return text == "No data"
        except Exception:
            return False

    @allure.step("Enter address: '{address}'")
    def enter_address(self, address: str) -> AddLocationModal:
        """Enter an address into the address field."""
        el = self._find_element(self.ADDRESS_INPUT)
        self._clear(el)
        el.send_keys(address)
        return self

    @allure.step("Clear address")
    def clear_address(self) -> AddLocationModal:
        """Clear the address field."""
        self._clear(self._find_element(self.ADDRESS_INPUT))
        return self

    @allure.step("Enter coordinates: '{coordinates}'")
    def enter_coordinates(self, coordinates: str) -> AddLocationModal:
        """Enter coordinates into the coordinates field."""
        el = self._find_element(self.COORDINATES_INPUT)
        self._clear(el)
        el.send_keys(coordinates)
        return self

    @allure.step("Clear coordinates")
    def clear_coordinates(self) -> AddLocationModal:
        """Clear the coordinates field."""
        self._clear(self._find_element(self.COORDINATES_INPUT))
        return self

    @allure.step("Enter phone: '{phone}'")
    def enter_phone(self, phone: str) -> AddLocationModal:
        """Enter a phone number into the phone field."""
        el = self._find_element(self.PHONE_INPUT)
        self._clear(el)
        el.send_keys(phone)
        return self

    @allure.step("Clear phone")
    def clear_phone(self) -> AddLocationModal:
        """Clear the phone field."""
        self._clear(self._find_element(self.PHONE_INPUT))
        return self

    @allure.step("Click 'Додати' button")
    def click_add_button(self) -> None:
        """Click the 'Додати' button in the Add Location modal."""
        self._wait_clickable(self.ADD_BUTTON).click()

    @allure.step("Check if 'Додати' button is enabled")
    def is_add_button_enabled(self) -> bool:
        """Verify whether the add button is clickable."""
        return self._find_element(self.ADD_BUTTON).is_enabled()

    @allure.step("Check if all info icons are displayed")
    def are_all_info_icons_displayed(self) -> bool:
        """Check whether all info icons in the modal are visible."""
        icons = self._find_elements(self.INFO_ICON)

        return bool(icons) and all(icon.is_displayed() for icon in icons)

    @allure.step("Click info icon")
    def click_info_icon(self) -> AddLocationModal:
        """Click the first info icon."""
        self._wait_clickable(self.INFO_ICON).click()
        return self

    @allure.step("Check if all feedback icons are visible")
    def are_all_feedback_icons_displayed(self) -> bool:
        """Check whether all feedback icons in the modal are visible."""
        icons = self._find_elements(self.FEEDBACK_ICON)

        return bool(icons) and all(icon.is_displayed() for icon in icons)

    @allure.step("Get all displayed validation error messages")
    def get_errors(self) -> list[str]:
        """Get all displayed validation error messages in the Add Location modal."""
        elems = self._find_elements(self.FIELD_ERROR_MESSAGES)
        return [e.text.strip() for e in elems if e.is_displayed()]

    @allure.step("Fill Add Location form")
    def fill(
        self,
        name: str | None = None,
        city: str | None = None,
        district: str | None = None,
        station: str | None = None,
        address: str | None = None,
        coordinates: str | None = None,
        phone: str | None = None,
    ) -> AddLocationModal:
        """Fill the form. Only provided fields are touched."""
        if name:
            self.enter_location_name(name)
        if city:
            self.select_city(city)
        if district:
            self.select_district(district)
        if station:
            self.select_station(station)
        if address:
            self.enter_address(address)
        if coordinates:
            self.enter_coordinates(coordinates)
        if phone:
            self.enter_phone(phone)
        return self
