"""TC-32: Login — non-existent email — Вхід modal (unknown user)."""
import allure

from pages.home_page import HomePage

EMAIL = "nobody@nowhere.com"
PASSWORD = "AnyPass123!"
EXPECTED_ERROR = "Введено невірний пароль або email"


@allure.feature("Login")
@allure.title("TC-32: Login — non-existent email — Вхід modal (unknown user)")
def test_login_non_existent_email(driver) -> None:
    """Verify that login with a non-existent email is rejected with an error, keeping the user unauthenticated and the modal open."""
    home_page = HomePage(driver)
    sign_in_modal = home_page.header.click_user_profile().click_login()
    assert sign_in_modal.is_displayed()

    sign_in_modal.fill_login_form(EMAIL, PASSWORD)
    sign_in_modal.click_submit()

    with allure.step("Verify login is rejected"):
        error_text = sign_in_modal.wait_for_login_error()
        assert error_text == EXPECTED_ERROR
        assert sign_in_modal.is_displayed()