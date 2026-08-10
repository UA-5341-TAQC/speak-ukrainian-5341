"""Modal Object for the multi-step Add Center wizard."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.components.center_basic_info_step import CenterBasicInfoStep
from pages.components.center_clubs_step import CenterClubsStep
from pages.components.center_contacts_step import CenterContactsStep
from pages.components.center_description_step import CenterDescriptionStep
from pages.modals.base_modal import BaseModal
from pages.types import Locator


class AddCenterModal(BaseModal):
    """Represent the multi-step 'Додати центр' modal window."""

    MODAL: Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-modal-content')][.//*[normalize-space()='Додати центр']]",
    )
    CLOSE_BUTTON: Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-modal-content')]"
        "[.//*[normalize-space()='Додати центр']]"
        "//button[contains(@class, 'ant-modal-close')]",
    )

    def __init__(self, driver: WebDriver):
        """Initialize the Add Center modal."""
        super().__init__(driver)

    def wait_opened(self) -> "AddCenterModal":
        """Wait until the Add Center modal is visible."""
        self._wait_visible(self.MODAL)
        return self

    def _get_modal_root(self):
        """Return the current modal root element."""
        return self._wait_visible(self.MODAL)

    def get_basic_info_step(self) -> CenterBasicInfoStep:
        """Return the Basic Information step component."""
        return CenterBasicInfoStep(self._get_modal_root())

    def get_contacts_step(self) -> CenterContactsStep:
        """Return the Contacts step component."""
        return CenterContactsStep(self._get_modal_root())

    def get_description_step(self) -> CenterDescriptionStep:
        """Return the Description step component."""
        return CenterDescriptionStep(self._get_modal_root())

    def get_clubs_step(self) -> CenterClubsStep:
        """Return the Clubs step component."""
        return CenterClubsStep(self._get_modal_root())

    @allure.step("Close the Add Center modal")
    def close(self) -> None:
        """Close the Add Center modal."""
        self._wait_clickable(self.CLOSE_BUTTON).click()
