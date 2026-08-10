"""Component Object for the Description step of Add Center."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.types import Locator


class CenterDescriptionStep(BaseComponent):
    """Represent the 'Опис' step."""

    DESCRIPTION_FORM: Locator = (By.CSS_SELECTOR, "form#basic.description")
    DESCRIPTION_TEXTAREA: Locator = (By.ID, "basic_description")
    BACK_BUTTON: Locator = (By.CSS_SELECTOR, "button.prev-btn")
    NEXT_BUTTON: Locator = (By.CSS_SELECTOR, "button.next-btn")
    LOGO_INPUT: Locator = (By.ID, "basic_urlLogo")
    PHOTO_INPUT: Locator = (By.ID, "basic_urlBackground")

    def __init__(self, root: WebElement):
        """Initialize the Description step."""
        super().__init__(root)

    def wait_loaded(self) -> "CenterDescriptionStep":
        """Wait until the Description step is visible."""
        self._wait_visible(self.STEP_TITLE)
        return self

    @allure.step("Upload center logo")
    def upload_logo(self, file_path: str) -> None:
        """Upload center logo."""
        # Ми не отримуємо шлях із Windows-вікна і не відкриваєм його.
        self._wait_present(self.LOGO_INPUT).send_keys(file_path)

    @allure.step("Upload center photo")
    def upload_photo(self, file_path: str) -> None:
        """Upload center photo."""
        # Ми не отримуємо шлях із Windows-вікна і не відкриваєм його.
        self._wait_present(self.PHOTO_INPUT).send_keys(file_path)

    @allure.step("Enter center description")
    def enter_description(self, description: str) -> None:
        """Enter the center description."""
        field = self._wait_visible(self.DESCRIPTION_TEXTAREA)
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(description)

    def get_description(self) -> str:
        """Return the current description value."""
        return self._wait_visible(self.DESCRIPTION_TEXTAREA).get_attribute("value") or ""

    @allure.step("Return to the Contacts step")
    def click_back(self) -> None:
        """Return to the previous Add Center step."""
        self._wait_clickable(self.BACK_BUTTON).click()

    @allure.step("Go to the Clubs step")
    def click_next(self) -> None:
        """Go to the next Add Center step."""
        self._wait_clickable(self.NEXT_BUTTON).click()
