import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage
from pages.modals.add_location_modal import AddLocationModal


@allure.epic("Center Management")
@allure.feature("Add Center")
@allure.title("TC-58: Center creation functionality")
@allure.description(
    "Verify that an authenticated user can successfully fill out the 'Add Center' modal "
    "and reach the final step to submit the center."
)
def test_center_creation_flow(authenticated_driver: WebDriver) -> None:
    with allure.step("Open 'Add Center' modal"):
        home_page = HomePage(authenticated_driver)
        add_center_modal = home_page.header.click_user_profile().click_add_centre_menu_item()

    with allure.step("Fill Basic Information step"):
        basic_info = add_center_modal.get_basic_info_step()
        basic_info.wait_loaded()
        basic_info.enter_center_name("Test Center 1")

        basic_info.click_add_location()
        add_location = AddLocationModal(authenticated_driver)
        add_location.fill(
            name="Test Location",
            city="Київ",
            address="вулиця Тестова 1",
            coordinates="50.4501, 30.5234",
            phone="0501111111",
        )
        add_location.click_add_button()

        basic_info.select_first_location()
        basic_info.click_next()

    with allure.step("Fill Contacts step"):
        contacts = add_center_modal.get_contacts_step()
        contacts.wait_loaded()
        contacts.enter_phone("0501111111")
        contacts.click_next()

    with allure.step("Fill Description step"):
        description = add_center_modal.get_description_step()
        description.wait_loaded()
        description_text = "Test center created for functional testing."
        description.enter_description(description_text)
        description.click_next()

    with allure.step("Fill Clubs step and verify completion"):
        clubs = add_center_modal.get_clubs_step()
        clubs.select_first_club()

        assert (
            clubs.is_next_button_enabled()
        ), "Finish button should be enabled after completing all steps"
        clubs.click_next()
