"""TC-17: Profile - Update phone number using valid 10-digit numeric value."""

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage
from pages.profile_page import ProfilePage

NEW_PHONE_NUMBER_INPUT = "0823459034"

@allure.feature("Update personal information")
@allure.title("TC-17: Update phone number using valid 10-digit numeric value")
def test_update_phone_number(authenticated_driver: WebDriver) -> None:
    """Verify updating phone number with a valid 10-digit value persists after refresh."""
    home_page = HomePage(authenticated_driver)
    home_page.header.click_user_profile().click_profile_menu_item()
    profile_page = ProfilePage(authenticated_driver)

    with allure.step("Click the Редагувати профіль button."):
        edit_profile_modal = profile_page.click_edit_profile()

    with allure.step("Clear the Телефон field and input a 10-digit numeric value."):
        edit_profile_modal.set_phone(NEW_PHONE_NUMBER_INPUT)
        assert edit_profile_modal.is_phone_valid_icon_displayed()

    with allure.step("Click the Зберегти зміни button."):
        edit_profile_modal.save_changes()
        assert "Профіль змінено успішно" in profile_page.get_success_message_text()

    with allure.step("Observe the phone number displayed on the main profile page."):
        assert profile_page.get_user_phone() == NEW_PHONE_NUMBER_INPUT

    with allure.step("Refresh the page and observe the phone number"):
        authenticated_driver.refresh()
        assert profile_page.get_user_phone() == NEW_PHONE_NUMBER_INPUT



