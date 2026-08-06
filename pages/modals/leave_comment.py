"""Leave comment / complaint modal, opened from the club details page."""

from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class LeaveCommentModal(BaseModal):
    """Modal for leaving a comment or a complaint about a club."""

    # Modal container and header
    MODAL_DIALOG: Locator = (By.CSS_SELECTOR, ".comment-modal")
    MODAL_TITLE: Locator = (By.CSS_SELECTOR, ".comment-edit-title")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")

    # Tabs -> switch between "Коментар" and "Скарга"
    COMMENT_TAB: Locator = (By.CSS_SELECTOR, "[data-node-key='1']")
    COMPLAINT_TAB: Locator = (By.CSS_SELECTOR, "[data-node-key='2']")

    # Club name shown inside the form
    CLUB_TITLE: Locator = (By.CSS_SELECTOR, ".club-title-note")

    # Contact fields, autofilled from user profile
    NAME_INPUT: Locator = (
        By.XPATH, "//label[@title=\"Ім'я\"]/ancestor::div[contains(@class,'ant-form-item-row')]//input"  # noqa: E501
    )
    PHONE_INPUT: Locator = (
        By.XPATH, "//label[@title='Телефон']/ancestor::div[contains(@class,'ant-form-item-row')]//input"  # noqa: E501
    )
    EMAIL_INPUT: Locator = (
        By.XPATH, "//label[@title='Email']/ancestor::div[contains(@class,'ant-form-item-row')]//input"  # noqa: E501
    )

    # Rating and description -> only editable fields, "Коментар" tab
    RATING_WIDGET: Locator = (By.CSS_SELECTOR, "#comment-edit_rate")
    RATING_STAR_TEMPLATE: Locator = (
        By.CSS_SELECTOR, "#comment-edit_rate div[role='radio'][aria-posinset='{stars}']")

    #Description field
    DESCRIPTION_LABEL: Locator = (By.CSS_SELECTOR, "label[for='comment-edit_commentText']")
    DESCRIPTION_FIELD: Locator = (By.CSS_SELECTOR, "#comment-edit_commentText")

    # Complaint note "Скарга не відображається у коментарі..."
    COMPLAINT_NOTE: Locator = (By.CSS_SELECTOR, ".complaint-note")

    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "button.do-comment-button")

    def is_modal_displayed(self) -> bool:
        """Check if the modal is currently open."""
        return self._find_element(self.MODAL_DIALOG).is_displayed()

    def click_comment_tab(self) -> None:
        """Switch to the 'Коментар' tab."""
        self._wait_clickable(self.COMMENT_TAB).click()

    def click_complaint_tab(self) -> None:
        """Switch to the 'Скарга' tab."""
        self._wait_clickable(self.COMPLAINT_TAB).click()

    def get_club_title(self) -> str:
        """Return the club name shown inside the form (same on both tabs)."""
        return self._find_element(self.CLUB_TITLE).text

    def get_name_value(self) -> str | None:
        """Return the value of the readonly Імя field."""
        return self._find_element(self.NAME_INPUT).get_attribute("value")

    def get_phone_value(self) -> str | None:
        """Return the value of the readonly 'Телефон' field."""
        return self._find_element(self.PHONE_INPUT).get_attribute("value")

    def get_email_value(self) -> str | None:
        """Return the value of the readonly 'Email' field."""
        return self._find_element(self.EMAIL_INPUT).get_attribute("value")

    def select_rating(self, stars: int) -> None:
        """Select a rating by clicking the star at the given position (1-5)."""
        if not 1 <= stars <= 5:
            raise ValueError(f"Rating must be between 1 and 5, got {stars}")

        # тут розпаковується кортеж локатора на тип і селектор
        by, value = self.RATING_STAR_TEMPLATE
        star = self._find_element((by, value.format(stars=stars)))
        star.click()

    def enter_description(self, text: str) -> None:
        """Enter text into the description field."""
        field = self._find_element(self.DESCRIPTION_FIELD)
        field.click()
        self.clear(field)
        field.send_keys(text)

    def get_complaint_note_text(self) -> str:
        """Return the complaint explanation note text (visible on 'Скарга' tab)."""
        return self._find_element(self.COMPLAINT_NOTE).text

    def is_submit_button_enabled(self) -> bool:
        """Check if the submit button is enabled (not disabled)."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    def click_submit(self) -> None:
        """Click the submit button to send the comment/complaint."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    def close_modal(self) -> None:
        """Close the modal via x button."""
        self._wait_clickable(self.CLOSE_BUTTON).click()

    def is_comment_tab_selected(self) -> bool:
        """Check if the 'Коментар' tab is currently selected."""
        tab = self._find_element(self.COMMENT_TAB)
        # get_attribute завжди повертає рядок, тому порівнюється з текстом "true", а не з булевим True  # noqa: E501
        return tab.get_attribute("aria-selected") == "true"

    def is_complaint_tab_selected(self) -> bool:
        """Check if the 'Скарга' tab is currently selected."""
        tab = self._find_element(self.COMPLAINT_TAB)
        return tab.get_attribute("aria-selected") == "true"

