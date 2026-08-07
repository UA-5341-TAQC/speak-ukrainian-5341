"""MasterPass payment tab component for WayForPay page."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.types import Locator


class MasterPassTab(BasePage):
    """Component for WayForPay MasterPass payment tab (#master)."""

    PHONE_INPUT: Locator = (By.CSS_SELECTOR, "#mpauth-phone")
    PASSWORD_INPUT: Locator = (By.CSS_SELECTOR, "#mpauth-pwd")
    LOGIN_BUTTON: Locator = (By.CSS_SELECTOR, "#mpauth-submit")
    FORGOT_PASSWORD_LINK: Locator = (
        By.CSS_SELECTOR,
        "#mp-block-auth .form-subactions a",
    )

    @allure.step("Fill MasterPass credentials in WayForPay")
    def fill_credentials(self, phone: str, password: str) -> "MasterPassTab":
        """Fill phone number and password for MasterPass authentication."""
        phone_el = self._find_element(self.PHONE_INPUT)
        self.clear(phone_el)
        phone_el.send_keys(phone)

        pwd_el = self._find_element(self.PASSWORD_INPUT)
        self.clear(pwd_el)
        pwd_el.send_keys(password)
        return self

    @allure.step("Click 'Увійти' button on WayForPay MasterPass tab")
    def click_login(self) -> None:
        """Click MasterPass login submit button."""
        self._find_element(self.LOGIN_BUTTON).click()

    @allure.step("Click 'Забули пароль?' link on WayForPay MasterPass tab")
    def click_forgot_password(self) -> None:
        """Click forgot password link."""
        self._find_element(self.FORGOT_PASSWORD_LINK).click()
