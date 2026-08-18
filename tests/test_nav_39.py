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

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from data.config import Config
from pages.components.header.header_component import HeaderComponent


@allure.title("TC-39 Verify header navigation links redirect to the correct pages.")
def test_header_navigation(driver: WebDriver) -> None:
    driver.get(Config.BASE_UI_URL)
    header = HeaderComponent(driver.find_element(By.TAG_NAME, "header"))

    with allure.step("1. Click the 'Гуртки' menu item in the header."):
        header.click_clubs()
        assert (
            "/clubs" in driver.current_url
        ), "User is redirected to the Clubs page."

    with allure.step("2. Navigate back to the homepage."):
        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
            "/"
        ), "Homepage is displayed again."

    with allure.step("3. Click the 'Челенжди menu' item in the header."):
       header.click_challenge()
       assert header.is_challenge_dropdown_visibile() == True

    with allure.step("4. Click the 'Єдині' challenge in the dropdown list."):
        challenge_dropdown = header.get_challenge_dropdown()
        challenge_dropdown.click_unique_challenge()          
        assert (
                    "/challenges/5" in driver.current_url
                ), "User is redirected to the 'Єдині' challenge page."

    with allure.step("5. Navigate back to the homepage."):
        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
            "/"
        ), "Homepage is displayed again."

    with allure.step("6.1. Repeat for 'Клуб Української мови Розмовляй'."):
        header.click_challenge()
        challenge_dropdown = header.get_challenge_dropdown()

        assert header.is_challenge_dropdown_visibile() == True

        challenge_dropdown.click_speaking_club_challenge()

        assert (
            "/challenges/4" in driver.current_url
                ), "User is redirected to the 'Клуб української мови 'Розмовляй' challenge page."

        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
               "/"
        ), "Homepage is displayed again."

    with allure.step("6.2. Repeat for 'Навчай українською челендж'."):
            header.click_challenge()
            challenge_dropdown = header.get_challenge_dropdown()

            assert header.is_challenge_dropdown_visibile() == True

            challenge_dropdown.click_teach_ukrainian_challenge()

            assert (
                "/challenges/3" in driver.current_url
                    ), "User is redirected to the 'Навчай українською челендж' challenge page."

            driver.back()
            assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
                    "/"
                ), "Homepage is displayed again."

    with allure.step("6.3. Repeat for 'Мовомаратон'."):
        header.click_challenge()
        challenge_dropdown = header.get_challenge_dropdown()
    
        assert header.is_challenge_dropdown_visibile() == True
    
        challenge_dropdown.click_language_marathon()
        assert (
            "/challenges/1" in driver.current_url
            ), "User is redirected to the 'Мовомаратон' challenge page."

        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
               "/"
        ), "Homepage is displayed again."

    with allure.step("6.4. Repeat for 'Навчай українською'."):
        header.click_challenge()
        challenge_dropdown = header.get_challenge_dropdown()
        
        assert header.is_challenge_dropdown_visibile() == True
        
        challenge_dropdown.click_teach_ukrainian()
        assert (
            "/challenges/2" in driver.current_url
             ), "User is redirected to the 'Навчай українською' challenge page."
        
        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
            "/"
        ), "Homepage is displayed again."

    with allure.step("7. Click the 'Новини' menu item."):
        header.click_news()
        assert (
            "/news" in driver.current_url
        ), "User is redirected to the News page."

    with allure.step("8. Navigate back to the homepage."):
        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
            "/"
        ), "Homepage is displayed again."

    with allure.step("9.Click the 'Про нас' menu item."):
        header.click_about()
        assert (
            "/about" in driver.current_url
        ), "User is redirected to the News page."

    with allure.step("10. Navigate back to the homepage."):
        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip(
            "/"
        ), "Homepage is displayed again."

    with allure.step("11.Click the 'Послуги українською' menu item."):
        header.click_services()
        assert (
            "/service" in driver.current_url
        ), "User is redirected to the 'Послуги українською' page."