from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.modals.add_club_modal import AddClubModal
from pages.types import Locator


class ContactsStep(AddClubModal):
    """Page object for the Contacts step (Контакти) of the Add Club modal."""

    LOCATION_LIST: Locator = (By.CSS_SELECTOR, ".add-club-location-list")
    ADD_LOCATION_BUTTON: Locator = (By.CSS_SELECTOR, "span.add-club-location")
    EMPTY_LIST_TEXT: Locator = (
        By.CSS_SELECTOR,
        ".add-club-location-list .ant-empty-description",
    )
    EDIT_LOCATION_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "span[aria-label='edit']"
    )
    DELETE_LOCATION_BUTTON: Locator = (
            By.CSS_SELECTOR,
            "span[aria-label='delete']"
        )

    ONLINE_SWITCH: Locator = (By.CSS_SELECTOR, "button.ant-switch")
    ONLINE_INFO_ICON: Locator = (By.CSS_SELECTOR, ".anticon-info-circle.info-icon")

    WORK_DAYS_GROUP: Locator = (By.ID, "basic_workDay")

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    @staticmethod
    def work_day_label(value: str) -> Locator:
        """Return a locator for the label of a work day checkbox."""
        return (
            By.XPATH,
            f".//label[.//input[@value='{value}']]"
        )

    @staticmethod
    def work_day_input(value: str) -> Locator:
        """Return a locator for the input of a work day."""
        return (
            By.CSS_SELECTOR,
            f"input[value='{value}']"
        )

    PHONE_INPUT: Locator = (By.ID, "basic_contactТелефон")
    FACEBOOK_INPUT: Locator = (By.ID, "basic_contactFacebook")
    WHATSAPP_INPUT: Locator = (By.ID, "basic_contactWhatsApp")
    EMAIL_INPUT: Locator = (By.ID, "basic_contactПошта")
    SKYPE_INPUT: Locator = (By.ID, "basic_contactSkype")
    SITE_INPUT: Locator = (By.ID, "basic_contactSite")

    @allure.step("Check if locations list is empty")
    def is_locations_list_empty(self) -> bool:
        """Check whether the locations list shows 'No data'."""
        return self._find(self.EMPTY_LIST_TEXT).text.strip() == "No data"

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
        switch = self._find(self.ONLINE_SWITCH)
        return switch.get_attribute("aria-checked") == "true"

    @allure.step("Select work day: {day_value}")
    def select_work_day(self, day_value: str) -> ContactsStep:
        """Select a work day by its value (e.g. ContactsStep.MONDAY)."""
        self._wait_clickable(self.work_day_label(day_value)).click()
        return self

    @allure.step("Check if work day '{day_value}' is selected")
    def is_work_day_selected(self, day_value: str) -> bool:
        """Check whether a specific work day checkbox is selected."""
        return self._find(self.work_day_input(day_value)).is_selected()

    @allure.step("Select work days: {days}")
    def select_work_days(self, days: list[str]) -> ContactsStep:
        """Select multiple work days at once."""
        for day in days:
            self.select_work_day(day)
        return self

    @allure.step("Enter phone (Телефон): '{phone}'")
    def enter_phone(self, phone: str) -> ContactsStep:
        """Enter phone number (+38 prefix is already present)."""
        el = self._find(self.PHONE_INPUT)
        self._clear(el)
        el.send_keys(phone)
        return self

    @allure.step("Clear phone (Телефон)")
    def clear_phone(self) -> ContactsStep:
        """Clear the phone input field."""
        self._clear(self._find(self.PHONE_INPUT))
        return self

    @allure.step("Enter Facebook: '{url}'")
    def enter_facebook(self, url: str) -> ContactsStep:
        """Enter Facebook URL or profile name."""
        el = self._find(self.FACEBOOK_INPUT)
        self._clear(el)
        el.send_keys(url)
        return self

    @allure.step("Clear Facebook url")
    def clear_facebook(self) -> ContactsStep:
        """Clear the Facebook input field."""
        self._clear(self._find(self.FACEBOOK_INPUT))
        return self

    @allure.step("Enter WhatsApp: '{phone}'")
    def enter_whatsapp(self, phone: str) -> ContactsStep:
        """Enter WhatsApp contact number."""
        el = self._find(self.WHATSAPP_INPUT)
        self._clear(el)
        el.send_keys(phone)
        return self

    @allure.step("Clear WhatsApp number")
    def clear_whatsapp(self) -> ContactsStep:
        """Clear the WhatsApp input field."""
        self._clear(self._find(self.WHATSAPP_INPUT))
        return self

    @allure.step("Enter email (Пошта): '{email}'")
    def enter_email(self, email: str) -> ContactsStep:
        """Enter email address."""
        el = self._find(self.EMAIL_INPUT)
        self._clear(el)
        el.send_keys(email)
        return self

    @allure.step("Clear email")
    def clear_email(self) -> ContactsStep:
        """Clear the email input field."""
        self._clear(self._find(self.EMAIL_INPUT))
        return self

    @allure.step("Enter Skype: '{skype}'")
    def enter_skype(self, skype: str) -> ContactsStep:
        """Enter Skype login."""
        el = self._find(self.SKYPE_INPUT)
        self._clear(el)
        el.send_keys(skype)
        return self

    @allure.step("Clear Skype")
    def clear_skype(self) -> ContactsStep:
        """Clear the Skype input field."""
        self._clear(self._find(self.SKYPE_INPUT))
        return self

    @allure.step("Enter site URL: '{url}'")
    def enter_site(self, url: str) -> ContactsStep:
        """Enter website URL."""
        el = self._find(self.SITE_INPUT)
        self._clear(el)
        el.send_keys(url)
        return self

    @allure.step("Clear site URL")
    def clear_site(self) -> ContactsStep:
        """Clear the site input field."""
        self._clear(self._find(self.SITE_INPUT))
        return self

    @allure.step("Fill Step 2 — Контакти")
    def fill(
        self,
        phone: str | None = None,
        facebook: str | None = None,
        whatsapp: str | None = None,
        email: str | None = None,
        skype: str | None = None,
        site: str | None = None,
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

        return self
