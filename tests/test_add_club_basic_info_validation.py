"""TC-36: Validation check for required fields in the 'Основна інформація' step of the 'Додати гурток' modal form."""
import allure

from pages.home_page import HomePage
from pages.profile_page import ProfilePage

BASIC_INFO_TITLE = "Основна інформація"
ERROR_CLUB_NAME = "Введіть назву гуртка"
ERROR_CLUB_CATEGORY = "Це поле є обов'язковим"
ERROR_CHILD_AGE = "Вік є обов'язковим"


@allure.feature("Add club basic info validation")
@allure.title(
    "TC-36: Validation check for required fields in the 'Основна інформація' step of the 'Додати гурток' modal form"
)
def test_add_club_basic_info_validation(authenticated_driver) -> None:
    home_page = HomePage(authenticated_driver)
    home_page.header.click_profile_menu_item()
    profile_page = ProfilePage(authenticated_driver)

    with allure.step("Open the 'Додати гурток' form."):
        basic_info_page = profile_page.click_add_club_button()
        assert basic_info_page.get_active_step() == BASIC_INFO_TITLE

    with allure.step("Leave the 'Назва гуртка', 'Категорія', 'Вік дитини' and 'Приналежність до центру' fields empty"):
        assert basic_info_page.get_errors() == []

    with allure.step("Click the 'Наступний крок' button"):
        basic_info_page.click_next()
        errors = basic_info_page.get_errors(expected_count=4)
        assert ERROR_CLUB_NAME in errors
        assert ERROR_CLUB_CATEGORY in errors
        assert errors.count(ERROR_CHILD_AGE) == 2

    with allure.step("Check the 'Приналежність до центру' field"):
        assert not basic_info_page.is_center_field_has_error()

    with allure.step("Verify form"):
        basic_info_page.click_next()
        assert basic_info_page.get_active_step() == BASIC_INFO_TITLE