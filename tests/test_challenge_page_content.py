"""Test suite for verifying challenge page content (TC-35)."""

from __future__ import annotations

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.challenge_page import ChallengePage


@allure.feature("Challenge")
class TestChallengePageContent:
    """Test suite for verifying challenge page content."""

    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver) -> None:
        """Open challenge page before each test."""
        driver.get(
            f"{Config.BASE_UI_URL}/challenges/2"
        )

    @allure.issue("TC-35")
    @allure.title(
        "TC-35: Verify challenge page content — "
        "title, description and header icons"
    )
    @allure.description(
        "Verify that the 'Навчай українською' challenge page "
        "displays the correct title, description paragraphs, "
        "social media links and donation button."
    )
    @allure.label("owner", "Svitlana Kovalova")
    @pytest.mark.regression
    def test_challenge_page_content(self, driver: WebDriver,) -> None:
        """Verify title, description and header content."""

        challenge_page = ChallengePage(driver)

        with allure.step(
            "Step 1: Open the 'Навчайся' challenge page"
        ):

            challenge_page.wait.until(
                lambda _: "/challenges/2" in driver.current_url
            ), "Challenge page is not opened"

        print(f"\n[DEBUG] Current URL after Step 1: {driver.current_url}")

        with allure.step(
            "Step 2: Verify the main challenge title"
        ):
            title = challenge_page.get_content_title()

            assert title == (
                "Програма челенджу «Навачайся»"
            ), (
                "Unexpected challenge content title: "
                f"'{title}'"
            )

        with allure.step(
                "Step 3: Verify challenge description paragraphs"
        ):
            paragraphs = challenge_page.get_description_paragraphs()

            assert len(paragraphs) > 0, "Description paragraphs are missing"

            assert "Проблематика та мета проєкту:" in paragraphs[0]
            assert "Вільне володіння державною мовою" in paragraphs[1]
            assert "Онлайн-курс «Челендж “Навчай українською”»" in paragraphs[2]

            full_text = " ".join(paragraphs)
            assert "Для кого цей курс?" in full_text
            assert "Структура та тривалість курсу:" in full_text

        with allure.step(
            "Step 4: Verify 'Наші контакти' and social media links"
        ):
            social = challenge_page.get_social_buttons()

            assert social.get_social_section_title_text() == (
                "Наші контакти"
            )

            assert (
                "facebook.com/teach.in.ukrainian"
                in social.get_facebook_url()
            )

            assert (
                "youtube.com/channel/UCP38C0jxC8aNbW34eBoQKJw"
                in social.get_youtube_url()
            )

            assert (
                "instagram.com/yedyni.ruh"
                in social.get_instagram_url()
            )

            assert social.get_email_address() == (
                "teach.in.ukrainian@gmail.com"
            )

        with allure.step(
            "Step 5: Verify 'Допомогти проєкту' button"
        ):
            donate_text = social.get_donate_button_text()

            assert donate_text == (
                "Допомогти проєкту"
            ), (
                "Unexpected donation button text: "
                f"'{donate_text}'"
            )

            donate_url = social.get_donate_url()

            assert "secure.wayforpay.com/payment" in donate_url, (
                "Donation button does not contain "
                "WayForPay payment URL"
            )
