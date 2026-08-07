"""Write to club manager modal, opened from the club details page."""

from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class WriteToManagerModal(BaseModal):
    """Modal for sending a message to the club manager."""

    # Modal container and header
    MODAL_DIALOG: Locator = (By.XPATH, "//div[contains(@class, 'MessageToClubManager')]")
    MODAL_TITLE: Locator = (By.XPATH, "//div[contains(@class, 'MessageToClubManager_title')]")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")

    # Club name and contacts, shown inside the form
    CLUB_NAME: Locator = (By.XPATH, "//div[contains(@class, 'MessageToClubManager_content')]/div[1]")  # noqa: E501
    CONTACT_WEBSITE_LINK: Locator = (By.CSS_SELECTOR, ".links .contact .contact-name a")
    CONTACT_ITEMS: Locator = (By.CSS_SELECTOR, ".links .contact .contact-name")

    # Form fields
    DESCRIPTION_LABEL: Locator = (By.CSS_SELECTOR, "label[for='message-from-club_text']")
    DESCRIPTION_FIELD: Locator = (By.CSS_SELECTOR, "#message-from-club_text")

    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "#message-from-club button[type='submit']")

    def is_modal_displayed(self) -> bool:
        """Check if the modal is open."""
        return self._find_element(self.MODAL_DIALOG).is_displayed()

    def get_club_name(self) -> str:
        """Return the club name shown inside the form."""
        return self._find_element(self.CLUB_NAME).text

    def get_phone(self) -> str:
        """Return the phone number from the contacts section."""
        contacts = self._find_elements(self.CONTACT_ITEMS)

        for contact in contacts:
            if not contact.find_elements(By.TAG_NAME, "a"):
                return contact.text.strip()
        raise ValueError("Phone contact not found")

    def enter_description(self, text: str) -> None:
        """Enter text into the description field."""
        field = self._find_element(self.DESCRIPTION_FIELD)
        field.click()
        self.clear(field)
        field.send_keys(text)

    def is_submit_button_enabled(self) -> bool:
        """Check if the submit button is enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    def click_submit(self) -> None:
        """Click the submit button to send the message."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    def is_description_label_displayed(self) -> bool:
        """Check if the description field label is visible."""
        return self._find_element(self.DESCRIPTION_LABEL).is_displayed()

    def is_modal_title_displayed(self) -> bool:
        """Check if the "Написати менеджеру" title is visible."""
        return self._find_element(self.MODAL_TITLE).is_displayed()

    def send_message(self, text: str) -> None:
        """Send message to the club manager."""
        self.enter_description(text)
        self.click_submit()

    def close_modal(self) -> None:
        """Close the modal via x button."""
        self._wait_clickable(self.CLOSE_BUTTON).click()
