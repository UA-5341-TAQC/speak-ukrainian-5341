"""TC-61 Profile: Attempt to update Last Name with invalid special characters (Negative).

Verifies that entering special characters into the "Прізвище" (Last Name) field of
the "Редагувати профіль" modal triggers client-side validation:
    - a validation error message is shown below the field,
    - the field border turns red and an error icon is displayed,
    - the "Зберегти зміни" button stays visually active (no disabled attribute),
    - clicking "Зберегти зміни" does not submit the form and the modal stays open.

Preconditions (covered inline):
    - The user is logged into the system (`authenticated_driver`).
    - The user is navigated to the "My Profile" page (route: /user/{id}/page).
"""

from __future__ import annotations

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage
from pages.modals.edit_profile_modal import EditProfileModal
from pages.profile_page import ProfilePage

# Invalid special characters used as the Last Name test data (TC-61).
INVALID_LAST_NAME = "(})_@#"

# Expected client-side validation message (TC-61).
EXPECTED_LAST_NAME_ERROR = "Прізвище не може містити спеціальні символи"


@allure.epic("Profile")
@allure.feature("Profile Last Name Update")
@allure.story("TC-61: Reject Last Name with invalid special characters")
@pytest.mark.regression
class TestProfileLastNameUpdate:
    """Negative test for updating the profile Last Name with special characters."""

    def test_last_name_rejects_special_characters(self, authenticated_driver: WebDriver) -> None:
        """TC-61: verify the Last Name field rejects invalid special characters.

        Test steps (from TC-61):
            1. Click "Редагувати профіль" - the modal opens.
            2. Clear "Прізвище", type invalid special characters and remove focus.
               A validation error appears, the border turns red, an error icon is
               shown and the save button remains active (no disabled attribute).
            3. Click "Зберегти зміни" - the form is not submitted, the modal stays
               open and the validation error is still displayed.
        """
        with allure.step("Precondition: navigate to the 'My Profile' page"):
            header = HomePage(authenticated_driver).header
            header.click_profile_menu_item()

        profile_page = ProfilePage(authenticated_driver)

        with allure.step("Click the 'Редагувати профіль' button"):
            modal: EditProfileModal = profile_page.click_edit_profile()
            assert modal.is_displayed(), "Expected the 'Редагувати профіль' modal to open."

        with allure.step(
            "Enter invalid special characters into the 'Прізвище' field and remove focus"
        ):
            modal.set_last_name(INVALID_LAST_NAME).blur_last_name()

        with allure.step("Verify the Last Name validation error message appears"):
            assert modal.is_last_name_error_displayed(), (
                "Expected a validation error message below the Last Name field."
            )
            assert modal.get_last_name_error_text() == EXPECTED_LAST_NAME_ERROR, (
                "Validation message does not match the expected text."
            )

        with allure.step("Verify the field shows the error state"):
            assert modal.has_last_name_error_border(), (
                "Expected the Last Name field border to turn red."
            )
            assert modal.is_last_name_error_icon_displayed(), (
                "Expected an error icon inside the Last Name field."
            )

        with allure.step("Verify the 'Зберегти зміни' button remains active"):
            assert modal.is_save_changes_enabled(), (
                "Expected the 'Зберегти зміни' button to remain enabled."
            )

        with allure.step("Click the 'Зберегти зміни' button"):
            modal.save_changes()

        with allure.step("Verify the form is not submitted and the modal stays open"):
            assert modal.is_displayed(), (
                "Expected the modal to remain open after submitting an invalid form."
            )
            assert modal.is_last_name_error_displayed(), (
                "Expected the validation error message to persist after submission."
            )
