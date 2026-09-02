import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.club_details_page import ClubDetailsPage
from pages.clubs_page import ClubPage
from pages.home_page import HomePage
from pages.modals.add_child_modal import AddChildModal
from pages.modals.enroll_to_club_modal import EnrollToClubModal

from utils.child_data import generate_child


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

@allure.title("TC-26: Verify visitor can add a child and register for a club")
@allure.tag("club-registration", "child", "visitor", "authentication")
def test_tc26_add__and_register_child(authenticated_driver: WebDriver) -> None:

    with allure.step("Step 1: Log in to the 'Навчай українською' site"):
        home_page = HomePage(authenticated_driver)

    with allure.step("Step 2: Click 'Гуртки' in the navigation bar"):
        home_page.header.click_clubs()
        club_page = ClubPage(authenticated_driver).wait_loaded()

    with allure.step("Step 3: Select a club and click 'Детальніше'"):
        club_page.open_first_club_details()
        details_page = ClubDetailsPage(authenticated_driver)

    with allure.step("Step 4: Click the 'Записатися на гурток' button"):
        details_page.click_enroll_button()
        modal = EnrollToClubModal(authenticated_driver).wait_for_visible()
        assert modal.is_modal_displayed(), "Expected the 'Записатися на гурток' modal to open."

    with allure.step("Step 5: Click the '+ Додати дитину' button"):
        modal.click_add_child()
        add_child_modal = AddChildModal(authenticated_driver).wait_for_visible()
        assert add_child_modal.is_modal_displayed(), "Expected the 'Додати дитину' modal to open."

    with allure.step("Step 6: Enter the child's valid information"):
        child = generate_child()

        add_child_modal.enter_first_name(child.first_name)
        add_child_modal.enter_last_name(child.last_name)
        add_child_modal.enter_age(child.age)

    with allure.step("Step 7: Select any gender"):
        add_child_modal.select_girl()

    with allure.step("Step 8: Click the 'Додати' button."):
        add_child_modal.click_submit()
        assert modal.is_child_added_message_displayed(), (
            "Success message should be displayed"
        )

    with allure.step("Step 9: Check that the newly added child is displayed"):
        assert modal.is_child_displayed(child.displayed_info), (
        "The newly added child should be displayed in the enrollment modal."
    )

    with allure.step("Step 10: Click the checkbox next to the newly added child"):
        modal.click_child_checkbox(child.displayed_info)
        assert modal.is_child_checkbox_selected(child.displayed_info), (
            "The checkbox for the newly added child should be selected."
        )

    with allure.step("Step 11: Click the 'Записати' button"):
        modal.click_submit()
        assert details_page.is_registration_success_message_displayed(), (
            "Success message should be displayed after club registration."
        )