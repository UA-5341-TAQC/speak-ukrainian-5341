from __future__ import annotations

from collections.abc import Callable

import allure
from selenium.webdriver.common.by import By

from pages.modals.add_club_modal import AddClubModal
from pages.types import Locator, Weekday


class ContactsStep(AddClubModal):
    """Page object for the Contacts step (Контакти) of the Add Club modal."""

    LOCATION_LIST: Locator = (By.CSS_SELECTOR, ".add-club-location-list")
    ADD_LOCATION_BUTTON: Locator = (By.CSS_SELECTOR, "span.add-club-location")
    EMPTY_LIST_TEXT: Locator = (
        By.CSS_SELECTOR,
        ".add-club-location-list .ant-empty-description",
    )
    EDIT_LOCATION_BUTTON: Locator = (By.CSS_SELECTOR, "span[aria-label='edit']")
    DELETE_LOCATION_BUTTON: Locator = (By.CSS_SELECTOR, "span[aria-label='delete']")

    ONLINE_SWITCH: Locator = (By.CSS_SELECTOR, "button.ant-switch")
    ONLINE_INFO_ICON: Locator = (By.CSS_SELECTOR, ".anticon-info-circle.info-icon")

    WORK_DAYS_GROUP: Locator = (By.ID, "basic_workDay")

    WORK_DAY_LABEL: Callable[[str], Locator] = staticmethod(
        lambda value: (By.XPATH, f".//label[.//input[@value='{value}']]")
    )

    WORK_DAY_INPUT: Callable[[str], Locator] = staticmethod(
        lambda value: (By.CSS_SELECTOR, f"input[value='{value}']")
    )

    WORK_TIME_PICKER: Locator = (By.CSS_SELECTOR, ".ant-picker-range")

    WORK_TIME_INPUTS: Locator = (By.CSS_SELECTOR, ".ant-picker-range input[placeholder='HH:mm']")

    TIME_PANEL: Locator = (By.CSS_SELECTOR, ".ant-picker-time-panel")

    TIME_PANEL_COLUMNS: Locator = (By.CSS_SELECTOR, ".ant-picker-time-panel-column")

    TIME_PANEL_CELL: Locator = (By.CSS_SELECTOR, ".ant-picker-time-panel-cell-inner")

    TIME_OK_BUTTON: Locator = (By.CSS_SELECTOR, ".ant-picker-ok button")

    PHONE_INPUT: Locator = (By.ID, "basic_contactТелефон")
    FACEBOOK_INPUT: Locator = (By.ID, "basic_contactFacebook")
    WHATSAPP_INPUT: Locator = (By.ID, "basic_contactWhatsApp")
    EMAIL_INPUT: Locator = (By.ID, "basic_contactПошта")
    SKYPE_INPUT: Locator = (By.ID, "basic_contactSkype")
    SITE_INPUT: Locator = (By.ID, "basic_contactSite")

    @allure.step("Check if locations list is empty")
    def is_locations_list_empty(self) -> bool:
        """Check whether the locations list shows 'No data'."""
        return self._find_element(self.EMPTY_LIST_TEXT).text.strip() == "No data"

    @allure.step("Click 'Додати локацію' button")
    def click_add_location(self) -> ContactsStep:
        """Click the button to add a new location."""
        self._wait_clickable(self.ADD_LOCATION_BUTTON).click()
        return self

    @allure.step("Click edit icon button for the first location")
    def click_edit_location(self) -> ContactsStep:
        """Click the edit button for the first location in the list."""
        self._wait_clickable(self.EDIT_LOCATION_BUTTON).click()
        return self

    @allure.step("Click delete icon button for the first location")
    def click_delete_location(self) -> ContactsStep:
        """Click the delete button for the first location in the list."""
        self._wait_clickable(self.DELETE_LOCATION_BUTTON).click()
        return self

    @allure.step("Toggle 'Доступний онлайн' switch")
    def toggle_online(self) -> ContactsStep:
        """Click the online availability switch."""
        self._wait_clickable(self.ONLINE_SWITCH).click()
        return self

    @allure.step("Check if 'Доступний онлайн' is enabled")
    def is_online_enabled(self) -> bool:
        """Check whether the online switch is turned on (Так)."""
        switch = self._find_element(self.ONLINE_SWITCH)
        return switch.get_attribute("aria-checked") == "true"

    @allure.step("Select work day: {day_value}")
    def select_work_day(self, day_value: Weekday) -> ContactsStep:
        """Select a work day by its value (e.g. ContactsStep.MONDAY)."""
        self._wait_clickable(self.WORK_DAY_LABEL(day_value)).click()
        return self

    @allure.step("Check if work day '{day_value}' is selected")
    def is_work_day_selected(self, day_value: str) -> bool:
        """Check whether a specific work day checkbox is selected."""
        return self._find_element(self.WORK_DAY_INPUT(day_value)).is_selected()

    @allure.step("Select work days: {days}")
    def select_work_days(self, days: list[Weekday]) -> ContactsStep:
        """Select multiple work days at once."""
        for day in days:
            self.select_work_day(day)
        return self

    @allure.step("Check if work time picker is visible")
    def is_work_time_visible(self) -> bool:
        """Check whether work time picker is visible."""
        return self._find_element(self.WORK_TIME_PICKER).is_displayed()

    @allure.step("Open start time picker")
    def open_start_time_picker(self) -> ContactsStep:
        """Click start time input."""
        inputs = self.driver.find_elements(*self.WORK_TIME_INPUTS)

        inputs[0].click()
        return self

    @allure.step("Open end time picker")
    def open_end_time_picker(self) -> ContactsStep:
        """Click end time input."""
        inputs = self.driver.find_elements(*self.WORK_TIME_INPUTS)

        inputs[1].click()
        return self

    @allure.step("Select time {hour}:{minute}")
    def select_time(
        self,
        hour: str,
        minute: str,
    ) -> ContactsStep:
        """Select hour and minute from opened time picker."""
        columns = self.driver.find_elements(*self.TIME_PANEL_COLUMNS)

        hour_cells = columns[0].find_elements(By.CSS_SELECTOR, ".ant-picker-time-panel-cell-inner")

        for cell in hour_cells:
            if cell.text == hour:
                cell.click()
                break

        minute_cells = columns[1].find_elements(
            By.CSS_SELECTOR, ".ant-picker-time-panel-cell-inner"
        )

        for cell in minute_cells:
            if cell.text == minute:
                cell.click()
                break

        return self

    @allure.step("Select work time range {start_hour}:{start_minute} - {end_hour}:{end_minute}")
    def select_work_time_range(
        self,
        start_hour: str,
        start_minute: str,
        end_hour: str,
        end_minute: str,
    ) -> ContactsStep:
        """Select start and end working time."""
        self.open_start_time_picker()
        self.select_time(start_hour, start_minute)

        self.open_end_time_picker()
        self.select_time(end_hour, end_minute)

        self._wait_clickable(self.TIME_OK_BUTTON).click()

        return self

    @allure.step("Enter phone (Телефон): '{phone}'")
    def enter_phone(self, phone: str) -> ContactsStep:
        """Enter phone number (+38 prefix is already present)."""
        el = self._find_element(self.PHONE_INPUT)
        self._clear(el)
        el.send_keys(phone)
        return self

    @allure.step("Clear phone (Телефон)")
    def clear_phone(self) -> ContactsStep:
        """Clear the phone input field."""
        self._clear(self._find_element(self.PHONE_INPUT))
        return self

    @allure.step("Enter Facebook: '{url}'")
    def enter_facebook(self, url: str) -> ContactsStep:
        """Enter Facebook URL or profile name."""
        el = self._find_element(self.FACEBOOK_INPUT)
        self._clear(el)
        el.send_keys(url)
        return self

    @allure.step("Clear Facebook url")
    def clear_facebook(self) -> ContactsStep:
        """Clear the Facebook input field."""
        self._clear(self._find_element(self.FACEBOOK_INPUT))
        return self

    @allure.step("Enter WhatsApp: '{phone}'")
    def enter_whatsapp(self, phone: str) -> ContactsStep:
        """Enter WhatsApp contact number."""
        el = self._find_element(self.WHATSAPP_INPUT)
        self._clear(el)
        el.send_keys(phone)
        return self

    @allure.step("Clear WhatsApp number")
    def clear_whatsapp(self) -> ContactsStep:
        """Clear the WhatsApp input field."""
        self._clear(self._find_element(self.WHATSAPP_INPUT))
        return self

    @allure.step("Enter email (Пошта): '{email}'")
    def enter_email(self, email: str) -> ContactsStep:
        """Enter email address."""
        el = self._find_element(self.EMAIL_INPUT)
        self._clear(el)
        el.send_keys(email)
        return self

    @allure.step("Clear email")
    def clear_email(self) -> ContactsStep:
        """Clear the email input field."""
        self._clear(self._find_element(self.EMAIL_INPUT))
        return self

    @allure.step("Enter Skype: '{skype}'")
    def enter_skype(self, skype: str) -> ContactsStep:
        """Enter Skype login."""
        el = self._find_element(self.SKYPE_INPUT)
        self._clear(el)
        el.send_keys(skype)
        return self

    @allure.step("Clear Skype")
    def clear_skype(self) -> ContactsStep:
        """Clear the Skype input field."""
        self._clear(self._find_element(self.SKYPE_INPUT))
        return self

    @allure.step("Enter site URL: '{url}'")
    def enter_site(self, url: str) -> ContactsStep:
        """Enter website URL."""
        el = self._find_element(self.SITE_INPUT)
        self._clear(el)
        el.send_keys(url)
        return self

    @allure.step("Clear site URL")
    def clear_site(self) -> ContactsStep:
        """Clear the site input field."""
        self._clear(self._find_element(self.SITE_INPUT))
        return self

    @allure.step("Fill Step 2 — Контакти")
    def (
        self,
        phone: str | None = None,
        facebook: str | None = None,
        whatsapp: str | None = None,
        email: str | None = None,
        skype: str | None = None,
        site: str | None = None,
        start_hour: str | None = None,
        start_minute: str | None = None,
        end_hour: str | None = None,
        end_minute: str | None = None,
    ) -> ContactsStep:
        """Fill contacts step fields."""
        if phone:
            self.enter_phone(phone)

        if facebook:
            self.enter_facebook(facebook)

        if whatsapp:
            self.enter_whatsapp(whatsapp)

        if email:
            self.enter_email(email)

        if skype:
            self.enter_skype(skype)

        if site:
            self.enter_site(site)

        if start_hour and start_minute and end_hour and end_minute:
            self.select_work_time_range(
                start_hour,
                start_minute,
                end_hour,
                end_minute,
            )

        return self

    @allure.step("Get phone number")
    def get_phone(self) -> str:
        """Return the current phone number."""
        return self._find_element(self.PHONE_INPUT).get_attribute("value") or ""
