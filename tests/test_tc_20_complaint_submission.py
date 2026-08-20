"""TC-20: Verify that an authenticated user can submit a complaint (Скарга).

The test walks the user through the club complaint flow described in the issue:
    1. Login (precondition - handled by the ``authenticated_driver`` fixture).
    2. Click 'Гуртки' in the header.
    3. Select a club and click 'Детальніше'.
    4. Click 'Залишити коментар' to open the comment modal.
    5. Switch to the 'Скарга' (complaint) tab.
    6. Verify the 'Надіслати' button is disabled.
    7. Verify the 'Ім''я', 'Телефон' and 'Email' fields are auto-populated with
       the authenticated user's data.
    8. Enter a complaint longer than 30 characters in the 'Опис' field.
    9. Verify the 'Надіслати' button becomes enabled.
   10. Click 'Надіслати' to submit the complaint.
   11. Navigate to 'Особистий кабінет' and open the 'Скарги' page.
   12. Verify the submitted complaint is displayed on the 'Скарги' page.

KNOWN BUG (see issue #20 - discovered while implementing this test case):
Submitting a complaint from the 'Скарга' tab currently fails. The frontend
throws a JavaScript ``TypeError: Cannot read properties of null (reading 'id')``
in ``CommentEditComponent.js`` (``onFinish``) when the 'Надіслати' button is
pressed. As a result the modal never closes, no success/error toast is shown and
no complaint is persisted (the 'Скарги' page stays empty - 'Скарг немає').
This test asserts the EXPECTED behaviour and therefore fails at the submission
step until the bug is fixed, which is the intent of this test case - exactly the
same convention as TC-62 (``test_profile_photo_upload.py``).
"""

from __future__ import annotations

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.club_details_page import ClubDetailsPage
from pages.clubs_page import ClubPage
from pages.home_page import HomePage
from pages.modals.leave_comment import LeaveCommentModal
from pages.profile_page import ProfilePage

# The complaint description used as test data (must be longer than 30 characters, see step 8).
COMPLAINT_TEXT = "Test text complaint Test text complaint 12345 Тестова скарга"


@allure.epic("Clubs")
@allure.feature("Club Comments")
@allure.story("TC-20: Authenticated user can submit a complaint")
@pytest.mark.regression
def test_tc_20_authenticated_user_can_submit_complaint(authenticated_driver: WebDriver) -> None:
    """Verify that an authenticated user can submit a complaint about a club.

    Args:
        authenticated_driver: Browser already signed in via the API fixture.
    """
    home_page = HomePage(authenticated_driver)

    with allure.step("Step 2: Click 'Гуртки' in the navigation bar"):
        home_page.header.click_clubs()
        club_page = ClubPage(authenticated_driver).wait_loaded()
        assert "/clubs" in authenticated_driver.current_url

    with allure.step("Step 3: Select a club and click 'Детальніше'"):
        club_page.open_first_club_details()
        assert "/club/" in authenticated_driver.current_url

    with allure.step("Step 4: Click 'Залишити коментар'"):
        details_page = ClubDetailsPage(authenticated_driver)
        details_page.click_leave_comment_button()
        modal = LeaveCommentModal(authenticated_driver).wait_for_visible()
        assert modal.is_modal_displayed(), "Expected the 'Залишити коментар' modal to open."

    with allure.step("Step 5: Select the 'Скарга' tab"):
        modal.click_complaint_tab()
        assert modal.is_complaint_tab_selected(), "Expected the 'Скарга' tab to be selected."

    with allure.step("Step 6: Verify the 'Надіслати' button is disabled"):
        assert not modal.is_submit_button_enabled(), (
            "Expected the 'Надіслати' button to be disabled before entering a complaint."
        )

    with allure.step("Step 7: Verify the contact fields are auto-populated"):
        assert modal.get_name_value(), "Expected the 'Ім''я' field to be pre-filled."
        assert modal.get_phone_value(), "Expected the 'Телефон' field to be pre-filled."
        assert modal.get_email_value() == Config.USER_EMAIL, (
            "Expected the 'Email' field to contain the authenticated user's email."
        )

    with allure.step("Step 8: Enter a complaint longer than 30 characters in 'Опис'"):
        assert len(COMPLAINT_TEXT) > 30
        modal.enter_description(COMPLAINT_TEXT)

    with allure.step("Step 9: Verify the 'Надіслати' button becomes enabled"):
        assert modal.is_submit_button_enabled(), (
            "Expected the 'Надіслати' button to become enabled after entering a complaint."
        )

    with allure.step("Step 10: Click 'Надіслати' to submit the complaint"):
        modal.click_submit()
        modal.wait_for_closed()

    with allure.step("Step 11: Navigate to 'Особистий кабінет' and open the 'Скарги' page"):
        header = HomePage(authenticated_driver).header
        header.click_user_profile().click_profile_menu_item()
        complaints_page = ProfilePage(authenticated_driver).open_complaints()

    with allure.step("Step 12: Verify the submitted complaint is displayed"):
        assert complaints_page.is_complaint_displayed(COMPLAINT_TEXT), (
            "Expected the submitted complaint to be displayed on the 'Скарги' page."
        )
