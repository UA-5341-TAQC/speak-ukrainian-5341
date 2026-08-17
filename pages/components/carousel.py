<<<<<<< HEAD
"""Component representing the home page carousel."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.components.carousel_item import CarouselItem
from pages.types import Locator


class Carousel(BaseComponent):
    """Component representing the home page carousel."""

    ITEMS: Locator = (
        By.CSS_SELECTOR,
        ".slick-slide:not(.slick-cloned)",
    )

    ACTIVE_ITEM: Locator = (
        By.CSS_SELECTOR,
        ".slick-slide.slick-active",
    )

    PREVIOUS_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".anticon-arrow-left.arrow",
    )

    NEXT_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".anticon-arrow-right.arrow",
    )

    @allure.step("Click previous carousel arrow")
    def click_previous_arrow(self) -> None:
        """Click the previous carousel arrow."""
        self._wait_clickable(self.PREVIOUS_ARROW).click()

    @allure.step("Click next carousel arrow")
    def click_next_arrow(self) -> None:
        """Click the next carousel arrow."""
        self._wait_clickable(self.NEXT_ARROW).click()

    @allure.step("Get active carousel item")
    def get_active_item(self) -> CarouselItem:
        """Return the active carousel item."""
        return CarouselItem(self._find_element(self.ACTIVE_ITEM))

    @allure.step("Get active carousel item link href")
    def get_active_link_href(self) -> str:
        """Return the href of the active slide's link, without a trailing slash."""
        return self.get_active_item().get_link().rstrip("/")

    @allure.step("Get carousel items")
    def get_items(self) -> list[CarouselItem]:
        """Return all non-cloned carousel items."""
        return [CarouselItem(item) for item in self.driver.find_elements(*self.ITEMS)]
=======
"""Component representing the home page carousel."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.components.carousel_item import CarouselItem
from pages.types import Locator


class Carousel(BaseComponent):
    """Component representing the home page carousel."""

    ITEMS: Locator = (
        By.CSS_SELECTOR,
        ".slick-slide:not(.slick-cloned)",
    )

    ACTIVE_ITEM: Locator = (
        By.CSS_SELECTOR,
        ".slick-slide.slick-active",
    )

    PREVIOUS_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".anticon-arrow-left.arrow",
    )

    NEXT_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".anticon-arrow-right.arrow",
    )

    @allure.step("Click previous carousel arrow")
    def click_previous_arrow(self) -> None:
        """Click the previous carousel arrow."""
        self._wait_clickable(self.PREVIOUS_ARROW).click()

    @allure.step("Click next carousel arrow")
    def click_next_arrow(self) -> None:
        """Click the next carousel arrow."""
        self._wait_clickable(self.NEXT_ARROW).click()

    @allure.step("Get active carousel item")
    def get_active_item(self) -> CarouselItem:
        """Return the active carousel item."""
        return CarouselItem(self._find_element(self.ACTIVE_ITEM))

    @allure.step("Get active carousel item link href")
    def get_active_link_href(self) -> str:
        """Return the href of the active slide's link, without a trailing slash."""
        return self.get_active_item().get_link().rstrip("/") or ""

    @allure.step("Get carousel items")
    def get_items(self) -> list[CarouselItem]:
        """Return all non-cloned carousel items."""
        return [CarouselItem(item) for item in self.driver.find_elements(*self.ITEMS)]
>>>>>>> main
