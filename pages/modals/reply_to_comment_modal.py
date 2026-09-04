"""Reply to comment modal, opened from the club details page."""

from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class ReplyToCommentModal(BaseModal):
    """Modal for replying to a comment."""

    # Modal container and header
    MODAL_DIALOG: Locator = (By.CSS_SELECTOR, ".comment-modal")
    MODAL_TITLE: Locator = (By.CSS_SELECTOR, ".comment-reply-title")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")

    # Contact fields, autofilled from user profile
    NAME_INPUT: Locator = (
        By.XPATH,
        "//label[@title=\"Ім'я\"]/ancestor::div[contains(@class,'ant-form-item-row')]//input",  # noqa: E501
    )
    PHONE_INPUT: Locator = (
        By.XPATH,
        "//label[@title='Телефон']/ancestor::div[contains(@class,'ant-form-item-row')]//input",  # noqa: E501
    )
    EMAIL_INPUT: Locator = (
        By.XPATH,
        "//label[@title='Email']/ancestor::div[contains(@class,'ant-form-item-row')]//input",  # noqa: E501
    )

    # Comment field
    DESCRIPTION_FIELD: Locator = (By.CSS_SELECTOR, "#commentText")

    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "button.do-comment-button")

    def is_modal_displayed(self) -> bool:
        """Check if the modal is currently open."""
        return self._find_element(self.MODAL_DIALOG).is_displayed()

    def is_modal_title_displayed(self) -> bool:
        """Check if the "Відповісти на коментар" title is visible."""
        return self._find_element(self.MODAL_TITLE).is_displayed()

    def get_name_value(self) -> str | None:
        """Return the value of the readonly Імя field."""
        return self._find_element(self.NAME_INPUT).get_attribute("value")

    def get_phone_value(self) -> str | None:
        """Return the value of the readonly 'Телефон' field."""
        return self._find_element(self.PHONE_INPUT).get_attribute("value")

    def get_email_value(self) -> str | None:
        """Return the value of the readonly 'Email' field."""
        return self._find_element(self.EMAIL_INPUT).get_attribute("value")

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
        """Click the submit button to send the reply."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    def reply(self, text: str) -> None:
        """Reply to the comment."""
        self.enter_description(text)
        self.click_submit()

    def close_modal(self) -> None:
        """Close the modal via x button."""
        self._wait_clickable(self.CLOSE_BUTTON).click()
