"""TC-39 Verify header navigation links redirect to the correct pages.

Test Steps
Step 1  Click the "Гуртки" menu item in the header.                       -> User is redirected to the Clubs page.
Step 2  Navigate back to the homepage (click the browser Back button).    -> Homepage is displayed again.
Step 3  Click the "Челенжди" menu item in the header.                     -> The challenges dropdown menu is displayed.
Step 4  Click the "Єдині" challenge in the dropdown list.                 -> User is redirected to the "Єдині" challenge page.
Step 5  Navigate back to the homepage (click the browser Back button).    -> Homepage is displayed again.
Step 6  Repeat the previous step for the remaining challenge items.       -> Each challenge opens its corresponding page.
Step 7  Click the "Новини" menu item.                                     -> User is redirected to the News page.
Step 8  Navigate back to the homepage (click the browser Back button).    -> Homepage is displayed again.
Step 9  Click the "Про нас" menu item.                                    -> User is redirected to the About Us page.
Step 10 Navigate back to the homepage (click the browser Back button).    -> Homepage is displayed again.
Step 11 Click the "Послуги українською" menu item.                        -> User is redirected to the Services in Ukrainian page.
"""

import allure
import pytest

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from data.config import Config
from pages.components.header_component import HeaderComponent
from pages.types import Locator

CHALLENGE_MENU: Locator = (
        By.CSS_SELECTOR,
        ".nav-menu .challenge-text",
    )


@allure.title("TC-39 Verify header navigation links redirect to the correct pages.")
@pytest.mark.smoke
def test_header_navigation(driver: WebDriver) -> None:
    """Verify header navigation links redirect to the correct pages."""

    driver.get(Config.BASE_UI_URL)
    header = HeaderComponent(driver)

    with allure.step("1.Click the 'Гуртки' menu item in the header."):
        header.click_clubs()
        assert (
            "/clubs" in driver.current_url
        ), "User is redirected to the Clubs page."

    with allure.step("2.Navigate back to the homepage"):
        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
            "/"
        ), "Homepage is displayed again."

    with allure.step("3.Click the 'Челенжди menu' item in the header."):
        header.click_challenge()
        assert header.is_challenge_dropdown_visibile() == True, "The challenges dropdown menu is displayed."

    with allure.step("4.Click the 'Єдині' challenge in the dropdown list."):
        challenge_dropdown = header.get_challenge_dropdown()
        challenge_dropdown.click_unique_challenge()
        
        assert (
                    "/challenges/5" in driver.current_url
                ), "User is redirected to the 'Єдині' challenge page."


    




