import allure
import pytest
from selenium.webdriver import ActionChains
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
        assert mail.is_displayed(), "Mail icon should be visible"

@allure.title("TC-42: Verify Facebook social media link functionality")
@allure.description(
    "Test verifies that the Facebook icon on the news details page "
    "opens the project's official Facebook page in a new browser tab."
)
@allure.tag("news", "social_media", "facebook", "link")
@pytest.mark.regression
def test_tc42_facebook_link_redirects_to_official_page(
    driver: WebDriver,
) -> None:
    """Verify Facebook social media link opens the official Facebook page."""

    expected_facebook_url = (
        "https://www.facebook.com/teach.in.ukrainian"
    )

    with allure.step("Step 1: Open news article"):
        page = NewsDetailsPage(driver)
        page.open(news_id=27)

    with allure.step("Step 2: Scroll to 'Наші контакти' block"):
        page.scroll_to_contacts()

    with allure.step("Step 3: Get social buttons component"):
        social = page.social_buttons

    with allure.step("Step 4: Verify Facebook link URL"):
        actual_facebook_url = social.get_facebook_url()

        assert actual_facebook_url == expected_facebook_url, (
            f"Expected Facebook URL '{expected_facebook_url}', "
            f"but got '{actual_facebook_url}'"
        )

    with allure.step("Step 5: Click Facebook icon"):
        original_window = driver.current_window_handle
        original_windows = driver.window_handles

        social.click_facebook_button()

    with allure.step("Step 6: Verify Facebook page opens in a new tab"):
        def new_tab_opened(driver: WebDriver) -> bool:
            return len(driver.window_handles) > len(original_windows)

        page.wait.until(new_tab_opened)

        new_window = next(
            window
            for window in driver.window_handles
            if window != original_window
        )

        driver.switch_to.window(new_window)

        assert driver.current_url.startswith(expected_facebook_url), (
            f"Expected Facebook URL '{expected_facebook_url}', "
            f"but got '{driver.current_url}'"
        )

@allure.title("TC-43: Verify YouTube social media link functionality")
@allure.description(
    "Test verifies that the YouTube icon on the news details page "
    "opens the project's official YouTube page in a new browser tab."
)
@allure.tag("news", "social_media", "youtube", "link")
@pytest.mark.regression
def test_tc43_youtube_link_redirects_to_official_page(
    driver: WebDriver,
) -> None:
    """Verify YouTube social media link opens the official YouTube page."""

    expected_youtube_url = (
        "https://www.youtube.com/channel/UCP38C0jxC8aNbW34eBoQKJw"
    )

    with allure.step("Step 1: Open news article"):
        page = NewsDetailsPage(driver)
        page.open(news_id=27)

    with allure.step("Step 2: Scroll to 'Наші контакти' block"):
        page.scroll_to_contacts()

    with allure.step("Step 3: Get social buttons component"):
        social = page.social_buttons

    with allure.step("Step 4: Verify YouTube link URL"):
        actual_youtube_url = social.get_youtube_url()

        assert actual_youtube_url == expected_youtube_url, (
            f"Expected YouTube URL '{expected_youtube_url}', "
            f"but got '{actual_youtube_url}'"
        )

    with allure.step("Step 5: Click YouTube icon"):
        original_window = driver.current_window_handle
        original_windows = driver.window_handles

        social.click_youtube_button()

    with allure.step("Step 6: Verify YouTube page opens in a new tab"):
        def new_tab_opened(driver: WebDriver) -> bool:
            return len(driver.window_handles) > len(original_windows)

        page.wait.until(new_tab_opened)

        new_window = next(
            window
            for window in driver.window_handles
            if window != original_window
        )

        driver.switch_to.window(new_window)

        assert driver.current_url.startswith(expected_youtube_url), (
            f"Expected YouTube URL '{expected_youtube_url}', "
            f"but got '{driver.current_url}'"
        )

@allure.title("TC-44: Verify Instagram social media link functionality")
@allure.description(
    "Test verifies that the Instagram icon on the news details page "
    "opens the project's official Instagram page in a new browser tab."
)
@allure.tag("news", "social_media", "instagram", "link")
@pytest.mark.regression
def test_tc44_instagram_link_redirects_to_official_page(
    driver: WebDriver,
) -> None:
    """Verify Instagram social media link opens the official Instagram page."""

    expected_instagram_url = (
        "https://www.instagram.com/yedyni.ruh/"
    )

    with allure.step("Step 1: Open news article"):
        page = NewsDetailsPage(driver)
        page.open(news_id=27)

    with allure.step("Step 2: Scroll to 'Наші контакти' block"):
        page.scroll_to_contacts()

    with allure.step("Step 3: Get social buttons component"):
        social = page.social_buttons

    with allure.step("Step 4: Verify Instagram link URL"):
        actual_instagram_url = social.get_instagram_url()

        assert actual_instagram_url == expected_instagram_url, (
            f"Expected Instagram URL '{expected_instagram_url}', "
            f"but got '{actual_instagram_url}'"
        )

    with allure.step("Step 5: Click Instagram icon"):
        original_window = driver.current_window_handle
        original_windows = driver.window_handles

        social.click_instagram_button()

    with allure.step("Step 6: Verify Instagram page opens in a new tab"):
        def new_tab_opened(driver: WebDriver) -> bool:
            return len(driver.window_handles) > len(original_windows)

        page.wait.until(new_tab_opened)

        new_window = next(
            window
            for window in driver.window_handles
            if window != original_window
        )

        driver.switch_to.window(new_window)

        current_url = driver.current_url

        is_instagram_profile = current_url.startswith(
            expected_instagram_url
        )

        is_instagram_login_redirect = (
            current_url.startswith(
                "https://www.instagram.com/accounts/login/"
            )
            and "next=https%3A%2F%2Fwww.instagram.com%2Fyedyni.ruh%2F"
            in current_url
        )

        assert is_instagram_profile or is_instagram_login_redirect, (
            "Expected Instagram profile URL or Instagram login "
            f"redirect to '{expected_instagram_url}', "
            f"but got '{current_url}'"
        )

@allure.title("TC-45: Verify email link functionality in contacts section")
@allure.description(
    "Test verifies that the email icon in the 'Наші контакти' section "
    "contains the correct project email address and uses a mailto link."
)
@allure.tag("news", "social_media", "email", "link")
@pytest.mark.regression
def test_tc45_email_link_contains_correct_recipient(
    driver: WebDriver,
) -> None:
    """Verify the email link contains the correct recipient address."""

    expected_email = "teach.in.ukrainian@gmail.com"
    expected_mailto = f"mailto:{expected_email}"

    with allure.step("Step 1: Open news article"):
        page = NewsDetailsPage(driver)
        page.open(news_id=27)

    with allure.step("Step 2: Scroll to 'Наші контакти' block"):
        page.scroll_to_contacts()

    with allure.step("Step 3: Get social buttons component"):
        social = page.social_buttons

    with allure.step("Step 4: Verify email recipient address"):
        actual_email = social.get_email_address()

        assert actual_email == expected_email, (
            f"Expected email address '{expected_email}', "
            f"but got '{actual_email}'"
        )

    with allure.step("Step 5: Verify email link uses mailto scheme"):
        actual_mailto_url = social.get_email_url()

        assert actual_mailto_url == expected_mailto, (
            f"Expected mailto URL '{expected_mailto}', "
            f"but got '{actual_mailto_url}'"
        )

@allure.title(
    "TC-47: Verify 'Допомогти проєкту' button display, "
    "styling, and payment redirection"
)
@allure.description(
    "Test verifies that the donation button is displayed, "
    "has the correct text and cursor, contains the expected "
    "WayForPay URL, and redirects to the payment page."
)
@allure.tag("news", "donation", "ui", "payment")
@pytest.mark.regression
def test_tc47_donate_button_redirects_to_wayforpay(
    driver: WebDriver,
) -> None:
    """Verify donation button display and WayForPay redirection."""

    expected_donate_text = "Допомогти проєкту"
    expected_payment_url = (
        "https://secure.wayforpay.com/payment/s0f2891d77061"
    )

    with allure.step("Step 1: Open news article"):
        page = NewsDetailsPage(driver)
        page.open(news_id=27)

    with allure.step("Step 2: Scroll to donation block"):
        page.scroll_to_contacts()

    with allure.step("Step 3: Get social buttons component"):
        social = page.social_buttons

    with allure.step("Step 4: Verify donation button is displayed"):
        assert social.is_donate_button_displayed(), (
            "Donate button should be visible"
        )

    with allure.step("Step 5: Verify donation button text"):
        actual_text = social.get_donate_button_text().strip()

        assert actual_text == expected_donate_text, (
            f"Expected donate button text "
            f"'{expected_donate_text}', "
            f"but got '{actual_text}'"
        )

    with allure.step("Step 6: Verify donation button cursor"):
        donate_button = social._find_element(
            social.DONATE_BUTTON
        )

        ActionChains(driver).move_to_element(
            donate_button
        ).perform()

        cursor = social.get_donate_button_cursor()

        assert cursor == "pointer", (
            f"Expected cursor 'pointer', but got '{cursor}'"
        )

    with allure.step("Step 7: Verify WayForPay URL"):
        actual_payment_url = social.get_donate_url()

        assert actual_payment_url == expected_payment_url, (
            f"Expected payment URL "
            f"'{expected_payment_url}', "
            f"but got '{actual_payment_url}'"
        )

    with allure.step("Step 8: Click donation button"):
        original_window = driver.current_window_handle
        original_windows = driver.window_handles

        social.click_donate_button()

    with allure.step("Step 9: Verify WayForPay payment page"):
        def new_tab_opened(driver: WebDriver) -> bool:
            return len(driver.window_handles) > len(original_windows)

        page.wait.until(new_tab_opened)

        new_window = next(
            window
            for window in driver.window_handles
            if window != original_window
        )

        driver.switch_to.window(new_window)

        assert driver.current_url.startswith(
            expected_payment_url
        ), (
            f"Expected WayForPay URL "
            f"'{expected_payment_url}', "
            f"but got '{driver.current_url}'"
        )