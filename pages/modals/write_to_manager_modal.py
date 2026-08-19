"""Write to club manager modal, opened from the club details page."""

import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class WriteToManagerModal(BaseModal):
    """Modal for sending a message to the club manager."""

    # Modal container and header
    MODAL_DIALOG: Locator = (
        By.XPATH,
        "//div[contains(@class, 'MessageToClubManager')]",
    )
    MODAL_TITLE: Locator = (
        By.XPATH,
        "//div[contains(@class, 'MessageToClubManager_title')]",
    )
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")

    # Club name and contacts, shown inside the form
    CLUB_NAME: Locator = (
        By.CSS_SELECTOR,
        ".ant-modal div[class*='MessageToClubManager_content'] > div:first-child",
    )
    CONTACT_WEBSITE_LINK: Locator = (
        By.CSS_SELECTOR,
        ".ant-modal .links .contact .contact-name a",
    )
    CONTACT_ITEMS: Locator = (
        By.CSS_SELECTOR,
        ".ant-modal .links .contact .contact-name",
    )
    # Form fields
    DESCRIPTION_LABEL: Locator = (
        By.CSS_SELECTOR,
        "label[for='message-from-club_text']",
    )
    DESCRIPTION_FIELD: Locator = (By.CSS_SELECTOR, "#message-from-club_text")

    SUBMIT_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "#message-from-club button[type='submit']",
    )

    @allure.step("Check if modal is displayed")
    def is_modal_displayed(self) -> bool:
        """Check if the modal is open."""
        return self._find_element(self.MODAL_DIALOG).is_displayed()

    @allure.step("Get club name")
    def get_club_name(self) -> str:
        """Return the club name shown inside the form."""
        return self._get_text(self.CLUB_NAME)

    @allure.step("Get phone")
    def get_phone(self) -> str:
        """Return the phone number from the contacts section."""
        contacts = self._find_elements(self.CONTACT_ITEMS)

        for contact in contacts:
            if not contact.find_elements(By.TAG_NAME, "a"):
                return contact.text.strip()
        raise ValueError("Phone contact not found")

    @allure.step("Click website link")
    def click_website_link(self) -> None:
        """Click the website link inside the modal."""
        self._wait_clickable(self.CONTACT_WEBSITE_LINK).click()

    @allure.step("Enter description")
    def enter_description(self, text: str) -> None:
        """Enter text into the description field."""
        field = self._wait_clickable(self.DESCRIPTION_FIELD)
        ActionChains(self.driver).move_to_element(field).click().send_keys(text).perform()

    @allure.step("Check if submit button enabled")
    def is_submit_button_enabled(self) -> bool:
        """Check if the submit button is enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    @allure.step("Click submit")
    def click_submit(self) -> None:
        """Click the submit button to send the message."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    @allure.step("Check if description label is displayed")
    def is_description_label_displayed(self) -> bool:
        """Check if the description field label is visible."""
        return self._find_element(self.DESCRIPTION_LABEL).is_displayed()

    @allure.step("Check if modal title is displayed")
    def is_modal_title_displayed(self) -> bool:
        """Check if the "Написати менеджеру" title is visible."""
        return self._find_element(self.MODAL_TITLE).is_displayed()

    @allure.step("Send message")
    def send_message(self, text: str) -> None:
        """Send message to the club manager."""
        self.enter_description(text)
        self.click_submit()

    @allure.step("Close modal")
    def close_modal(self) -> None:
        """Close the modal via x button."""
        self._wait_clickable(self.CLOSE_BUTTON).click()
