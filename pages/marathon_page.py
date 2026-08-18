"""Page object for the language marathon page of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.types import Locator


class MarathonPage(BasePage):
    """Page object representing the /marathon language marathon page."""

    REGISTER_BUTTON: Locator = (
        By.CSS_SELECTOR,
        'a[href$="/marathon/registration"]',
    )
    TASKS_PREV_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".arrows-prev",
    )
    TASKS_NEXT_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".arrows-next",
    )
    PAGINATION_DOTS: Locator = (
        By.CSS_SELECTOR,
        ".slick-dots li",
    )
    VISIBLE_TASK_TITLES: Locator = (
        By.CSS_SELECTOR,
        ".slick-slide.slick-active .name",
    )

    @allure.step("Get 'Зареєструватись' button href")
    def get_register_button_href(self) -> str | None:
        """Get the href of the 'Зареєструватись' registration button."""
        return self._find_element(self.REGISTER_BUTTON).get_attribute("href")

    @allure.step("Click 'Зареєструватись' button")
    def click_register(self) -> None:
        """Click the 'Зареєструватись' registration button."""
        self._wait_clickable(self.REGISTER_BUTTON).click()

    @allure.step("Get titles of the currently visible task cards")
    def get_visible_task_titles(self) -> list[str]:
        """Get the titles of the task cards visible on the current carousel page."""

        def _has_visible_titles(_: object) -> list[str]:
            return [
                el.text for el in self._find_elements(self.VISIBLE_TASK_TITLES)
                if el.text.strip()
            ]

        self.get_wait(5).until(_has_visible_titles)
        return _has_visible_titles(None)

    @allure.step("Get pagination dot count")
    def get_pagination_dot_count(self) -> int:
        """Get the total number of pagination dots below the task carousel."""
        return len(self._find_elements(self.PAGINATION_DOTS))

    @allure.step("Get active pagination dot index")
    def get_active_dot_index(self) -> int:
        """Get the 1-based index of the currently active pagination dot."""
        dots = self._find_elements(self.PAGINATION_DOTS)
        for index, dot in enumerate(dots, start=1):
            if "slick-active" in (dot.get_attribute("class") or ""):
                return index
        raise ValueError("No active pagination dot found.")

    @allure.step("Click the task carousel's previous arrow")
    def click_prev(self) -> None:
        """Click the left arrow to move the task carousel to the previous page."""
        current_dot = self.get_active_dot_index()
        self._wait_clickable(self.TASKS_PREV_ARROW).click()

        if current_dot > 1:
            def _is_dot_changed(_: object) -> bool:
                try:
                    return self.get_active_dot_index() != current_dot
                except ValueError:
                    return False

            self.get_wait(5).until(_is_dot_changed)

    @allure.step("Click the task carousel's next arrow")
    def click_next(self) -> None:
        """Click the right arrow to move the task carousel to the next page."""
        current_dot = self.get_active_dot_index()
        self._wait_clickable(self.TASKS_NEXT_ARROW).click()
        total_dots = self.get_pagination_dot_count()

        if current_dot < total_dots:
            def _is_dot_changed(_: object) -> bool:
                try:
                    return self.get_active_dot_index() != current_dot
                except ValueError:
                    return False

            self.get_wait(5).until(_is_dot_changed)

    @allure.step("Click pagination dot {index}")
    def click_dot(self, index: int) -> None:
        """Click a pagination dot to jump the task carousel to that page.

        Args:
            index: 1-based position of the dot to click.

        Raises:
            ValueError: If index is not within the range of available dots.
        """
        dots = self._find_elements(self.PAGINATION_DOTS)
        if not 1 <= index <= len(dots):
            raise ValueError(f"Dot index {index} out of range (1..{len(dots)}).")

        dots[index - 1].click()

        self.get_wait(5).until(
            lambda _: self.get_active_dot_index() == index
        )

    @allure.step("Scroll to task carousel section")
    def scroll_to_tasks(self) -> None:
        """Scroll the task carousel into view so elements load properly."""
        self._scroll_into_view(self.VISIBLE_TASK_TITLES)
