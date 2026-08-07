"""Enroll to club modal, opened from the club details page."""

from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class EnrollToClubModal(BaseModal):
    """Modal for enrolling a child to a club."""

    # Modal container and header
    MODAL_DIALOG: Locator = (By.CSS_SELECTOR, "div[role='dialog'][class*='SignUpForClubModal']")
    MODAL_TITLE: Locator = (By.CSS_SELECTOR, "div.ant-modal-title")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")

    # Club name, shown inside the form
    CLUB_NAME: Locator = (By.XPATH, "//div[contains(@class, 'SignUpForClub_content')]/div[1]")

    # Checkbox
    SELF_ENROLL_CHECKBOX: Locator = (By.CSS_SELECTOR, "input.ant-checkbox-input[value='self']")
    CHILD_ENROLL_CHECKBOX: Locator = (By.XPATH, "//div[contains(@class,'SignUpForClub_label')][contains(.,'{child_info}')]/ancestor::label//input[@type='checkbox']")  # noqa: E501

    ADD_CHILD_BUTTON: Locator = (By.CSS_SELECTOR, "button.add-children-btn")

    # Comment field
    COMMENT_FIELD: Locator = (By.CSS_SELECTOR, "#registration-to-club_comment")

    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "#registration-to-club button[type='submit']")

    def is_modal_displayed(self) -> bool:
        """Check if the modal is open."""
        return self._find_element(self.MODAL_DIALOG).is_displayed()

    def is_modal_title_displayed(self) -> bool:
        """Check if the "Записати на гурток" title is visible."""
        return self._find_element(self.MODAL_TITLE).is_displayed()

    def get_club_name(self) -> str:
        """Return the club name shown inside the form."""
        return self._find_element(self.CLUB_NAME).text

    def click_self_enroll_checkbox(self) -> None:
        """Click the "Записати мене на гурток" checkbox."""
        self._wait_clickable(self.SELF_ENROLL_CHECKBOX).click()

    def is_self_enroll_checkbox_selected(self) -> bool:
        """Check if the "Записати мене на гурток" checkbox is selected."""
        return self._find_element(self.SELF_ENROLL_CHECKBOX).is_selected()

    # Підставляє конкретні дані дитини в шаблон і повертає вже готовий локатор
    # (дітей може бути кілька, і кожна має свій чекбокс)
    def _get_child_checkbox_locator(self, child_info: str) -> Locator:
        """Get a locator for a child's checkbox by their displayed info."""
        by, value = self.CHILD_ENROLL_CHECKBOX
        return by, value.format(child_info=child_info)

    def click_child_checkbox(self, child_info: str) -> None:
        """Click the checkbox for a child by their displayed info."""
        self._wait_clickable(self._get_child_checkbox_locator(child_info)).click()

    def is_child_checkbox_selected(self, child_info: str) -> bool:
        """Check if the checkbox for a child by their displayed info is selected."""
        return self._find_element(self._get_child_checkbox_locator(child_info)).is_selected()

    def click_add_child(self) -> None:
        """Click the "Додати дитину" button."""
        self._wait_clickable(self.ADD_CHILD_BUTTON).click()

    def enter_comment(self, text: str) -> None:
        """Enter text into the comment field."""
        field = self._find_element(self.COMMENT_FIELD)
        field.click()
        self.clear(field)
        field.send_keys(text)

    def is_submit_button_enabled(self) -> bool:
        """Check if the submit button is enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    def click_submit(self) -> None:
        """Click the submit button to enroll to the club."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    def close_modal(self) -> None:
        """Close the modal via x button."""
        self._wait_clickable(self.CLOSE_BUTTON).click()
