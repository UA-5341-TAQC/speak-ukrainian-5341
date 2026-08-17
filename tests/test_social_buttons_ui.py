<<<<<<< HEAD
import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.components.social_buttons import SocialButtons
from pages.news_details_page import NewsDetailsPage


@allure.title("TC-28: Verify 'Наші контакти' section display")
@allure.description(
    "Test verifies that the 'Наші контакти' block is displayed on the news page, "
    "has the correct title, and contains all required social media icons: "
    "Facebook, YouTube, Instagram, and Mail."
)
@allure.tag("news", "contacts", "ui", "social_media", "button")
def test_tc28_contacts_section_display(driver: WebDriver) -> None:
    """Verify the 'Наші контакти' section is displayed on the news page with all required social media icons."""
    with allure.step("Step 1: Open news page"):
        page = NewsDetailsPage(driver)
        page.open(news_id=27)

    with allure.step("Step 1: Scroll down to 'Наші контакти' block"):
        page.scroll_to_contacts()

    with allure.step("Get social buttons component"):
        social: SocialButtons = page.social_buttons

    with allure.step("Step 2: Verify section title is 'Наші контакти'"):
        title = social.get_social_section_title_text().strip()
        assert title == "Наші контакти", (
            f"Expected title 'Наші контакти', but got '{title}'"
        )

    with allure.step("Step 3: Verify Facebook icon availability"):
        fb = social.root.find_element(*SocialButtons.FACEBOOK_BUTTON)
        assert fb.is_displayed(), "Facebook icon should be visible"

    with allure.step("Step 4: Verify YouTube icon availability"):
        yt = social.root.find_element(*SocialButtons.YOUTUBE_BUTTON)
        assert yt.is_displayed(), "YouTube icon should be visible"

    with allure.step("Step 5: Verify Instagram icon availability"):
        ig = social.root.find_element(*SocialButtons.INSTAGRAM_BUTTON)
        assert ig.is_displayed(), "Instagram icon should be visible"

    with allure.step("Step 6: Verify Mail icon availability"):
        mail = social.root.find_element(*SocialButtons.MAIL_BUTTON)
=======
import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.components.social_buttons import SocialButtons
from pages.news_details_page import NewsDetailsPage


@allure.title("TC-28: Verify 'Наші контакти' section display")
@allure.description(
    "Test verifies that the 'Наші контакти' block is displayed on the news page, "
    "has the correct title, and contains all required social media icons: "
    "Facebook, YouTube, Instagram, and Mail."
)
@allure.tag("news", "contacts", "ui", "social_media", "button")
def test_tc28_contacts_section_display(driver: WebDriver) -> None:
    """Verify the 'Наші контакти' section is displayed on the news page with all required social media icons."""
    with allure.step("Step 1: Open news page"):
        page = NewsDetailsPage(driver)
        page.open(27)

    with allure.step("Step 1: Scroll down to 'Наші контакти' block"):
        page.scroll_to_contacts()

    with allure.step("Get social buttons component"):
        social: SocialButtons = page.social_buttons

    with allure.step("Step 2: Verify section title is 'Наші контакти'"):
        title = social.get_social_section_title_text().strip()
        assert title == "Наші контакти", (
            f"Expected title 'Наші контакти', but got '{title}'"
        )

    with allure.step("Step 3: Verify Facebook icon availability"):
        fb = social.root.find_element(*SocialButtons.FACEBOOK_BUTTON)
        assert fb.is_displayed(), "Facebook icon should be visible"

    with allure.step("Step 4: Verify YouTube icon availability"):
        yt = social.root.find_element(*SocialButtons.YOUTUBE_BUTTON)
        assert yt.is_displayed(), "YouTube icon should be visible"

    with allure.step("Step 5: Verify Instagram icon availability"):
        ig = social.root.find_element(*SocialButtons.INSTAGRAM_BUTTON)
        assert ig.is_displayed(), "Instagram icon should be visible"

    with allure.step("Step 6: Verify Mail icon availability"):
        mail = social.root.find_element(*SocialButtons.MAIL_BUTTON)
>>>>>>> main
        assert mail.is_displayed(), "Mail icon should be visible"