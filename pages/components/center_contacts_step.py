"""Component Object for the Contacts step of Add Center."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.types import Locator


class CenterContactsStep(BaseComponent):
    """Represent the 'Контакти' step."""

    CONTACTS_FORM: Locator = (
        By.ID,
        "contacts",
    )
    PHONE_INPUT: Locator = (By.ID, "contacts_contactТелефон")
    EMAIL_INPUT: Locator = (By.ID, "contacts_contactПошта")
    FACEBOOK_INPUT: Locator = (By.ID, "contacts_contactFacebook")
    WHATSAPP_INPUT: Locator = (By.ID, "contacts_contactWhatsApp")
    SKYPE_INPUT: Locator = (By.ID, "contacts_contactSkype")
    SITE_INPUT: Locator = (By.ID, "contacts_contactSite")
    BACK_BUTTON: Locator = (By.CSS_SELECTOR, "button.prev-btn")
    NEXT_BUTTON: Locator = (By.CSS_SELECTOR, "button.next-btn")

    def __init__(self, root: WebElement):
        """Initialize the Contacts step."""
        super().__init__(root)

    def wait_loaded(self) -> "CenterContactsStep":
        """Wait until the Contacts step is visible."""
        self._wait_visible(self.CONTACTS_FORM)
        return self

    def _enter_text(self, locator: Locator, value: str) -> None:
        """Clear a field and enter text."""
        field = self._wait_visible(locator)
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(value)

    @allure.step("Enter center phone")
    def enter_phone(self, phone: str) -> None:
        """Enter center phone number."""
        self._enter_text(self.PHONE_INPUT, phone)

    @allure.step("Enter center email")
    def enter_email(self, email: str) -> None:
        """Enter center email."""
        self._enter_text(self.EMAIL_INPUT, email)

    @allure.step("Enter center Facebook link")
    def enter_facebook(self, url: str) -> None:
        """Enter center Facebook URL."""
        self._enter_text(self.FACEBOOK_INPUT, url)

    @allure.step("Return to the Basic Information step")
    def click_back(self) -> None:
        """Return to the previous Add Center step."""
        self._wait_clickable(self.BACK_BUTTON).click()

    @allure.step("Go to the Description step")
    def click_next(self) -> None:
        """Go to the next Add Center step."""
        self._wait_clickable(self.NEXT_BUTTON).click()
