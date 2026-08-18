"""Automated test for TC-37: Checking the structure and presence of elements 
in the "Основна інформація" step of the "Додати гурток" modal form.
"""
from __future__ import annotations

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.components.add_club.basic_info_step import BasicInfoStep
from pages.home_page import HomePage

EXPECTED_CATEGORIES_COUNT = 12

EXPECTED_MODAL_TITLE = "Додати гурток"

STEP_BASIC_INFO = "Основна інформація"
STEP_CONTACTS = "Контакти"
STEP_DESCRIPTION = "Опис"


@allure.feature("Add Club modal")
@allure.story("TC-37: Checking the structure of 'Основна інформація' step")
@pytest.mark.smoke
def test_add_club_modal_basic_info_structure(authenticated_driver: WebDriver) -> None:
    """TC-37: Verify the structure and presence of elements in the 
    "Основна інформація" step of "Додати гурток" modal.

    Preconditions:
        - User is registered and logged into the Навчай Українською

    Test Steps:
        1. Open the "Додати гурток" form
        2. Verify the window title
        3. Verify the step indicator on the left
        4. Verify the "Назва гуртка" field
        5. Verify the "Категорія" section with 12 checkboxes
        6. Verify the "Вік дитини" section with "Від" and "До" fields
        7. Verify the "Приналежність до центру" dropdown
        8. Verify the "Наступний крок" button is active
    """
    with allure.step("Step 1: Open the 'Додати гурток' form"):
        header = HomePage(authenticated_driver).header
        header.click_add_club_menu_item()
        basic_info = BasicInfoStep(authenticated_driver)

    with allure.step("Verify: The form opens on step 'Основна інформація'"):
        assert basic_info.get_active_step() == STEP_BASIC_INFO, (
            f"Expected the active step to be '{STEP_BASIC_INFO}', "
            f"but got '{basic_info.get_active_step()}'."
        )

    with allure.step("Step 2: Verify the window title"):
        modal_title = basic_info.get_modal_title()
        assert modal_title == EXPECTED_MODAL_TITLE, (
            f"Expected modal title to be '{EXPECTED_MODAL_TITLE}', "
            f"but got '{modal_title}'."
        )

    with allure.step("Step 3: Verify the step indicator on the left"):
        assert basic_info.is_step_active(STEP_BASIC_INFO), (
            f"Expected step '{STEP_BASIC_INFO}' to be active."
        )
        assert basic_info.is_step_inactive(STEP_CONTACTS), (
            f"Expected step '{STEP_CONTACTS}' to be inactive."
        )
        assert basic_info.is_step_inactive(STEP_DESCRIPTION), (
            f"Expected step '{STEP_DESCRIPTION}' to be inactive."
        )

    with allure.step("Step 4: Verify the 'Назва гуртка' field"):
        assert basic_info.is_name_input_visible(), (
            "Expected the 'Назва гуртка' input field to be visible."
        )
        name_input = basic_info._find_element(basic_info.NAME_INPUT)
        placeholder = name_input.get_attribute("placeholder")
        assert placeholder == "Назва гуртка", (
            f"Expected placeholder 'Назва гуртка', but got '{placeholder}'."
        )

    with allure.step("Step 5: Verify the 'Категорія' section"):
        assert basic_info.is_categories_container_visible(), (
            "Expected the categories container to be visible."
        )
        categories_count = basic_info.get_categories_count()
        assert categories_count == EXPECTED_CATEGORIES_COUNT, (
            f"Expected {EXPECTED_CATEGORIES_COUNT} category checkboxes, "
            f"but found {categories_count}."
        )

    with allure.step("Step 6: Verify the 'Вік дитини' section"):
        assert basic_info.is_age_from_visible(), (
            "Expected the 'Від' age input field to be visible."
        )
        assert basic_info.is_age_to_visible(), (
            "Expected the 'До' age input field to be visible."
        )
        age_from_input = basic_info._find_element(basic_info.AGE_FROM_INPUT)
        age_to_input = basic_info._find_element(basic_info.AGE_TO_INPUT)
        assert age_from_input.is_displayed(), (
            "Expected AGE_FROM input to be displayed."
        )
        assert age_to_input.is_displayed(), (
            "Expected AGE_TO input to be displayed."
        )

    with allure.step("Step 7: Verify the 'Приналежність до центру' field"):
        assert basic_info.is_center_select_visible(), (
            "Expected the center selection dropdown to be visible."
        )
        center_selector = basic_info._find_element(basic_info.CENTER_SELECT_SELECTOR)
        placeholder = center_selector.get_attribute("placeholder")
        assert placeholder or center_selector.is_displayed(), (
            "Expected the center dropdown to have a placeholder or be displayed."
        )

    with allure.step("Step 8: Verify the navigation button"):
        assert basic_info.is_next_button_enabled(), (
            "Expected the 'Наступний крок' button to be enabled."
        )

    with allure.step("Postcondition: Close the Add Club modal"):
        basic_info.close()
