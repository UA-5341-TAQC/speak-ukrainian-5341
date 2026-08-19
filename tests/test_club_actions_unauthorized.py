import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.clubs_page import ClubPage
from pages.club_details_page import ClubDetailsPage
from pages.components.header.header_component import HeaderComponent


@allure.title("TC-15: Verify unauthorized user cannot use restricted club actions")
@allure.description(
    "Test verifies that 'Записатися на гурток', 'Написати менеджеру', "
    "'Залишити коментар', and 'Відповісти' are unavailable for unauthenticated users."
)
@allure.tag("clubs", "ui", "button", "unauthenticated")
def test_tc15_unauthorized_user_cannot_use_club_actions(driver: WebDriver) -> None:
    """Verify that the buttons functionalities are unavailable for unauthenticated users"""
    with allure.step("Step 1: Open the site"):
        driver.get(Config.BASE_UI_URL)

    with allure.step("Step 2: Click 'Гуртки' in navigation"):
        header = HeaderComponent(
            driver.find_element(By.TAG_NAME, "header")
        )
        
        header.click_clubs()

    with allure.step("Step 3: Select first club and click 'Детальніше'"):
        club_page = ClubPage(driver)
        club_page.wait_loaded()
        card = club_page.get_first_club_card()
        card.click_more_details()

    details_page = ClubDetailsPage(driver)

    with allure.step("Step 4: Check 'Записатись на гурток' button is disabled"):
        assert details_page.is_enroll_button_disabled(), \
            "Enroll button should be disabled for unauthenticated user"

    with allure.step("Step 5: Hover over enroll button, check tooltip and cursor"):
        details_page.hover_enroll_button()
        tooltip = details_page.get_tooltip_text()
        assert "Ця функціональність доступна тільки користувачу" in tooltip, \
            f"Unexpected tooltip text: {tooltip}"
        cursor = details_page.get_enroll_button_cursor()
        assert cursor == "not-allowed", \
            f"Expected cursor 'not-allowed', got '{cursor}'"

    with allure.step("Step 6: Click 'Написати менеджеру' and check popup"):
        details_page.click_write_to_manager_button()
        assert details_page.is_login_popup_displayed(), \
            "Login popup should appear after clicking 'Написати менеджеру'"
        popup_title = details_page.get_login_popup_title()
        assert "Увійдіть або зареєструйтеся!!!" in popup_title, \
            f"Unexpected popup title: {popup_title}"

    with allure.step("Step 7: Close popup"):
        details_page.close_login_popup()

    with allure.step(f"Step 8: Click 'Залишити коментар' and check toast"):
        details_page.click_leave_comment_button()
        toast = details_page.get_error_message_text()
        assert "Увійдіть або зареєструйтеся!" in toast, \
            f"Unexpected toast after leave comment: {toast}"

    with allure.step("Step 9: Click 'Відповісти' on first comment and check toast"):
        details_page.click_reply_on_first_comment()
        toast = details_page.get_error_message_text()
        print("Toast after reply:", toast)
        assert "Увійдіть або зареєструйтеся!" in toast, \
            f"Unexpected toast after reply: {toast}"
