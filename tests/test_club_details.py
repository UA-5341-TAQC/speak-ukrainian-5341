import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage


@allure.title(
    "TC-30: Verify that an authenticated user can send a message to a club manager"
)
def test_send_message_to_manager(authenticated_driver: WebDriver) -> None:
    home_page = HomePage(authenticated_driver)
    clubs_page = home_page.header.click_clubs()

    with allure.step("Select a club and click details"):
        cards = clubs_page.get_club_cards()
        assert len(cards) > 0, "Precondition: At least one club exists in the system"
        club_details = cards[0].click_more_details()
        club_name = club_details.get_title()

    modal = club_details.click_write_to_manager_button()

    with allure.step("Check that the club's name and phone number are displayed"):
        assert (
            club_name in modal.get_club_name()
        ), f"Expected {club_name} in modal title"
        assert modal.get_phone(), "Phone number should be displayed in the modal"

    original_window = club_details.get_current_window_handle()
    expected_windows = len(club_details.get_window_handles()) + 1

    modal.click_website_link()
    club_details.wait_for_new_window(expected_windows)

    assert (
        len(club_details.get_window_handles()) == expected_windows
    ), "New browser tab should be opened"

    club_details.switch_to_window(original_window)
    assert (
        modal.is_modal_displayed()
    ), "Modal should still be displayed after switching back"

    with allure.step("Enter a message"):
        message = "I would like to know more about the schedule and registration process for this club."
        modal.enter_description(message)
        assert modal.is_submit_button_enabled(), "Submit button should be enabled"

    modal.click_submit()
