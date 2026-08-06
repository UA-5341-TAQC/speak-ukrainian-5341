"""Club Card Filters Component (Advacned search) for the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ClubFiltersComponent(BaseComponent):
    """Component for Club Card Filters Component (Advacned search)."""

    # Icon + Sider
    SEARCH_ICON: Locator = (By.CSS_SELECTOR, "span.anticon.anticon-control.advanced-icon")
    SIDER_CONTAINER: Locator = (By.CSS_SELECTOR, ".ant-layout-sider-children")

    # Filters
    AGE_INPUT: Locator = (
        By.CSS_SELECTOR,
        ".ant-layout-sider-children input.ant-input-number-input")

    CITY_DROPDOWN: Locator= (By.CSS_SELECTOR, ".ant-layout-sider-children #basic_cityName")
    DISTRICT_DROPDOWN: Locator = (By.CSS_SELECTOR, ".ant-layout-sider-children #basic_districtName")
    STATION_DROPDOWN: Locator = (By.CSS_SELECTOR, ".ant-layout-sider-children #basic_stationName")
    CLEAR_BUTTON:Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-layout-sider-children')]//button[contains(span, 'Очистити')]")

    # XPATH
    _CATEGORY_CHECKBOX_TEMPLATE: Locator = (
        "//div[contains(@class, 'ant-layout-sider-children')]"
        "//span[contains(text(), '{category_name}')]/preceding-sibling::span//input"
    )

    # Online - need to double check
    ONLINE_ONLY_LABEL = (
        By.XPATH,
        "//div[contains(@class,'ant-layout-sider-children')]//*[contains(text(),'онлайн')]"
    )


    def __init__(self, root: WebElement) -> None:
        """Initialize the base component with a WebElement root."""
        super().__init__(root)

    def _get_category_locator(self, category_name: str) -> tuple[str, str]:
        return By.XPATH, self._CATEGORY_CHECKBOX_TEMPLATE.format(category_name=category_name)

    @allure.step("Click on 'Advanced search' icon ")
    def toggle_advanced_search(self) -> None:
        """Click on Advanced search icon to open sider with filters."""
        icon = self.wait.until(EC.element_to_be_clickable(self.SEARCH_ICON))
        icon.click()

    @allure.step("Check if sider with filters is displayed")
    def is_sider_visible(self) -> bool:
        """Check if sider with filters is displayed."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.SIDER_CONTAINER)
            ).is_displayed()
        except Exception:
            return False

    @allure.step("Open sider with filters")
    def ensure_sider_open(self) -> None:
        """Open sider with filters."""
        if not self.is_sider_visible():
            self.toggle_advanced_search()

    @allure.step("Switch Online option: {target_state}")
    def set_online_only(self, target_state: bool = True) -> None:
        """Set online option to true or false."""
        self.ensure_sider_open()

        # Current state of online checkbox input (checkbox/radio)
        checkbox = self.wait.until(EC.presence_of_element_located(self.ONLINE_ONLY_CHECKBOX))
        is_selected = checkbox.is_selected()

        if is_selected != target_state:
            label = self.wait.until(EC.element_to_be_clickable(self.ONLINE_ONLY_LABEL))
            label.click()

    @allure.step("Check Online option")
    def is_online_selected(self) -> bool:
        """Check if online option is selected or not."""
        self.ensure_sider_open()
        checkbox = self.wait.until(EC.presence_of_element_located(self.ONLINE_ONLY_CHECKBOX))
        return checkbox.is_selected()

    @allure.step("Choose age: {age}")
    def set_age(self, age: int) -> None:
        """Set age for Age field."""
        self.ensure_sider_open()
        age_input = self.wait.until(EC.element_to_be_clickable(self.AGE_INPUT))
        age_input.clear() # reminder: from base implementation
        age_input.send_keys(str(age))


    @allure.step("Choose by category name: {category_name}")
    def select_category_by_name(self, category_name: str) -> None:
        """Select categories by name."""
        self.ensure_sider_open()
        locator = self._get_category_locator(category_name)
        checkbox = self.wait.until(EC.presence_of_element_located(locator))

        if not checkbox.is_selected():
            checkbox.click()

    @allure.step("Clear all filters")
    def clear_filters(self) -> None:
        """Clear all filters."""
        self.ensure_sider_open()
        clear_btn = self.wait.until(EC.element_to_be_clickable(self.CLEAR_BUTTON))
        clear_btn.click()
