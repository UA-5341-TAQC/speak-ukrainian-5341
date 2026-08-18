"""TC-62 Profile: Attempt to upload an unsupported file format for profile photo (Negative).

Verifies that selecting an unsupported file format (e.g. a ``.pdf``) for the
profile photo in the "Редагувати профіль" modal is rejected gracefully:
    - an error message is shown (e.g. "Формат файлу не підтримується"),
    - the file is NOT added to the "Фото" section,
    - the "Зберегти зміни" button becomes disabled,
    - closing the modal keeps the profile avatar unchanged.

KNOWN BUG (see issue #62 - Additional Context): the current system does NOT
validate the format gracefully - it adds the file to the upload list and, on
save, the server returns an HTTP 500 instead of a client-side validation error.
This test asserts the EXPECTED behaviour and therefore fails until the bug is
fixed, which is the intent of this negative test case.

Preconditions (covered inline):
    - The user is logged into the system (`authenticated_driver`).
    - The user is on the "My Profile" page (route: /user/{id}/page).
    - An unsupported file (``document.pdf``) is prepared under ``data/assets``.
"""

from __future__ import annotations

from pathlib import Path

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage
from pages.modals.edit_profile_modal import EditProfileModal
from pages.profile_page import ProfilePage

# Unsupported file used as the profile photo test data (TC-62).
UNSUPPORTED_FILE = Path(__file__).parent.parent / "data" / "assets" / "document.pdf"


@allure.epic("Profile")
@allure.feature("Profile Photo Upload")
@allure.story("TC-62: Reject unsupported profile photo file format")
@pytest.mark.regression
class TestProfilePhotoUpload:
    """Negative test for uploading an unsupported file as the profile photo."""

    def test_unsupported_profile_photo_is_rejected(self, authenticated_driver: WebDriver) -> None:
        """TC-62: verify an unsupported profile photo format is rejected.

        Test steps (from TC-62):
            1. Click "Редагувати профіль" - the modal opens.
            2. Click "Завантажити фото" - the file dialog opens (simulated).
            3. Select the unsupported ``document.pdf`` - an error is shown, the
               file is not added and the save button becomes disabled.
            4. Click Close (X) - the modal closes.
            5. The avatar on the profile page remains unchanged.
        """
        with allure.step("Precondition: navigate to the 'My Profile' page"):
            header = HomePage(authenticated_driver).header
            header.click_profile_menu_item()

        profile_page = ProfilePage(authenticated_driver)
        avatar_before = profile_page.get_avatar_state()

        with allure.step("Click the 'Редагувати профіль' button"):
            modal: EditProfileModal = profile_page.click_edit_profile()
            assert modal.is_displayed(), "Expected the 'Редагувати профіль' modal to open."

        with allure.step("Click the 'Завантажити фото' button"):
            modal.click_upload_photo()

        with allure.step("Select the unsupported file and confirm"):
            modal.upload_photo(str(UNSUPPORTED_FILE)).wait_for_upload_settle()

        with allure.step("Verify an upload error message is displayed"):
            assert modal.is_photo_upload_error_displayed(), (
                "Expected an error message for the unsupported file format "
                "(e.g. 'Формат файлу не підтримується')."
            )

        with allure.step("Verify the file is NOT added to the 'Фото' section"):
            assert UNSUPPORTED_FILE.name not in modal.get_uploaded_file_names(), (
                "Expected the unsupported file NOT to be added to the photo section."
            )

        with allure.step("Verify the 'Зберегти зміни' button becomes disabled"):
            assert not modal.is_save_changes_enabled(), (
                "Expected the 'Зберегти зміни' button to become disabled after "
                "selecting an unsupported file."
            )

        with allure.step("Step 4: close the modal"):
            modal.close_modal()

        with allure.step("Step 5: verify the profile avatar remains unchanged"):
            avatar_after = profile_page.get_avatar_state()
            assert avatar_after == avatar_before, (
                "Expected the avatar to remain unchanged after a rejected upload."
            )
