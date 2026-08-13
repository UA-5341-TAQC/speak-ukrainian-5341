"""Test suite for verifying challenge page content (TC-35)."""

from __future__ import annotations

import allure
import pytest

from data.config import Config
from pages.challenge_page import ChallengePage


@allure.feature("Challenge")
class TestChallengePageContent:
    """Test suite for verifying challenge page content."""

    @pytest.fixture(autouse=True)
    def setup(self, driver) -> None:
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
    def test_challenge_page_content(
        self,
        driver,
    ) -> None:
        """Verify title, description and header content."""

        challenge_page = ChallengePage(driver)

        with allure.step(
            "Step 1: Open the 'Навчай українською' challenge page"
        ):
            challenge_page.open(2)

            challenge_page.wait.until(
                lambda _: "/challenges/2" in driver.current_url
            ), "Challenge page is not opened"

        with allure.step(
            "Step 2: Verify the main challenge title"
        ):
            title = challenge_page.get_content_title()

            assert title == (
                "Навчання українською у дитячих гуртках, "
                "студіях та секціях є важливим"
            ), (
                "Unexpected challenge content title: "
                f"'{title}'"
            )

        with allure.step(
                "Step 3: Verify challenge description paragraphs"
        ):
            paragraphs = challenge_page.get_description_paragraphs()

            assert len(paragraphs) == 5, (
                "Expected 5 description paragraphs, "
                f"but found {len(paragraphs)}"
            )

            assert paragraphs[0] == (
                "Ми разом з вами хочемо, щоб молоде покоління "
                "добре володіло і користувалось українською мовою, "
                "і розуміємо, як важливо, щоб нею навчали у "
                "дитячих гуртках, студіях та секціях."
            )

            assert paragraphs[1] == (
                "Ви можете вдосконалити свої знання та навички, "
                "щоб викладати українською мовою, взявши участь "
                "у челенджі “Навчай українською”."
            )

            assert paragraphs[2] == (
                "Ми записали для вас мотиваційні та практичні "
                "вебінари з експертами, зібрали корисні матеріали "
                "та придумали цікаві завдання. Завдяки челенджу "
                "“Навчай українською” перехід на українську мову "
                "викладання стане для вас комфортним."
            )

            assert paragraphs[3].startswith(
                "Близько двох тисяч учасників з усієї України уже взяли участь "
                "у двох 21-денних челенджах “Навчай українською”"
            )

            assert "Перший челендж відбувся у листопаді 2020 року." in paragraphs[3]

            assert "Другий челендж відбувся у квітні 2021 року." in paragraphs[3]

            assert "Тисяча викладачів із Києва, Харкова, Дніпра, Одеси, Запоріжжя" in paragraphs[3]

            assert paragraphs[4] == (
                "Ви можете переглянути вебінари, які допоможуть "
                "вам у переході на українську мову викладання."
            )

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