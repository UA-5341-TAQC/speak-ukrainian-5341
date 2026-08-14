"""Automated test for TC-60: automatic "Доступний онлайн" status assignment
when no location is specified in the "Додати гурток" modal form.
"""
from __future__ import annotations

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.components.add_club.basic_info_step import BasicInfoStep
from pages.components.add_club.contacts_step import ContactsStep
from pages.components.add_club.description_step import DescriptionStep
from pages.home_page import HomePage

VALID_PHONE = "0991234567"  # yields +380991234567 per the pre-rendered +38 prefix
EXPECTED_INFO_BANNER_TEXT = "Ви не додали жодної локації, гурток автоматично є онлайн"

STEP_CONTACTS = "Контакти"
STEP_DESCRIPTION = "Опис"

# Real category value, found via DevTools inspection of the checkbox input.
BASIC_INFO_CATEGORY = "Студії раннього розвитку"


@allure.feature("Add Club modal")
@allure.story("TC-60: Auto-assign 'Доступний онлайн' when no location is added")
@pytest.mark.regression
def test_online_status_auto_assigned_when_no_location(authenticated_driver: WebDriver) -> None:
    """TC-60: verify "Доступний онлайн" auto-toggles on when no location is added.

    Preconditions covered inline (per TC-60):
        - User is authenticated (via `authenticated_driver`).
        - "Додати гурток" modal is opened through the header user menu.
        - Step "Основна інформація" is completed.

    NOTE: the info message ("Ви не додали жодної локації, гурток автоматично
    є онлайн") renders as an antd `ant-message` toast at the top of the
    modal, so it's checked via `DescriptionStep.is_toast_displayed()` /
    `.get_toast_text()`, which already exist in the codebase. Since toasts
    can be transient, the check happens immediately after `click_next()`.
    """
    with allure.step("Precondition: open 'Додати гурток' modal"):
        header = HomePage(authenticated_driver).header
        header.click_add_club_menu_item()

    with allure.step("Precondition: complete step 'Основна інформація'"):
        basic_info = BasicInfoStep(authenticated_driver)
        basic_info.fill(
            name="QA Test Club",
            categories=[BASIC_INFO_CATEGORY],
            age_from=6,
            age_to=12,
        )
        basic_info.click_next()

    contacts_step = ContactsStep(authenticated_driver)

    with allure.step("Step 1: verify no location has been added"):
        assert contacts_step.is_locations_list_empty(), (
            "Expected the locations list to show the 'No data' placeholder "
            "when no location has been added."
        )

    with allure.step("Step 2: verify the 'Доступний онлайн' switch is off"):
        assert not contacts_step.is_online_enabled(), (
            "Expected the 'Доступний онлайн' switch to be off before proceeding."
        )

    # Required to be able to proceed to step "Опис".
    contacts_step.enter_phone(VALID_PHONE)

    with allure.step("Step 3: move to step 'Опис' and check the info banner"):
        contacts_step.click_next()
        description_step = DescriptionStep(authenticated_driver)

        assert description_step.get_active_step() == STEP_DESCRIPTION, (
            "Expected step 'Опис' to open after clicking 'Наступний крок'."
        )
        assert description_step.is_toast_displayed(), (
            "Expected an info toast to be displayed on step 'Опис'."
        )
        assert description_step.get_toast_text() == EXPECTED_INFO_BANNER_TEXT, (
            "Toast text does not match the expected message."
        )

    with allure.step("Step 4: go back to step 'Контакти' and check the switch"):
        description_step.click_prev()
        contacts_step = ContactsStep(authenticated_driver)

        assert contacts_step.get_active_step() == STEP_CONTACTS, (
            "Expected step 'Контакти' to open after clicking 'Назад'."
        )
        assert contacts_step.is_online_enabled(), (
            "Expected the 'Доступний онлайн' switch to be automatically "
            "turned on after returning from step 'Опис'."
        )

    with allure.step("Postcondition: close the Add Club modal"):
        contacts_step.close()