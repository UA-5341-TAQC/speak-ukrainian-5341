"""Component object for a challenge webinar video block."""

from collections.abc import Iterator
from contextlib import contextmanager
from typing import cast

import allure
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from data.config import Config
from pages.components.base_component import BaseComponent
from pages.types import Locator


class ChallengeVideoCard(BaseComponent):
    """Represent one webinar video block on the challenge page."""

    TITLE: Locator = (By.XPATH, "./preceding-sibling::h1[1]",)

    THUMBNAIL: Locator = (By.CSS_SELECTOR, "div.ytmVideoCoverThumbnail",)

    PLAY_BUTTON: Locator = (By.CSS_SELECTOR, "button.ytmCuedOverlayPlayButton")

    YOUTUBE_LINK: Locator = (By.CSS_SELECTOR, "a[href*='youtube.com/watch']",)

    def __init__(self, root: WebElement) -> None:
        """Initialize the video card with the YouTube iframe."""
        super().__init__(root)

    def _scroll_to_player(self) -> None:
        """Scroll the iframe into the center of the viewport."""
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: 'instant',
                block: 'center'
            });
            """,
            self.root,)

    @contextmanager
    def _inside_frame(self) -> Iterator[None]:
        """Temporarily switch into the embedded YouTube iframe."""
        self.driver.switch_to.default_content()

        self._scroll_to_player()

        WebDriverWait(
            self.driver,
            Config.EXPLICIT_WAIT,
            ignored_exceptions=(
                NoSuchElementException,
                StaleElementReferenceException,
            ),
        ).until(lambda _: self.root.is_displayed())

        self.driver.switch_to.frame(self.root)

        try:
            yield
        finally:
            self.driver.switch_to.default_content()

    def _video_element_state(self) -> dict[str, object] | None:
        """Return the current state of the HTML video element."""
        state = self.driver.execute_script(
            """
            const video = document.querySelector('video');

            if (!video) {
                return null;
            }

            return {
                paused: video.paused,
                error: video.error ? video.error.code : null
            };
            """)

        return cast(dict[str, object] | None, state)

    @allure.step("Get webinar video title")
    def get_title_text(self) -> str:
        """Return the webinar title shown above the video."""
        return self._find_element(self.TITLE).text.strip()

    @allure.step("Get embedded YouTube video ID")
    def get_video_id(self) -> str:
        """Return the YouTube video ID from the iframe source."""
        src = self.root.get_attribute("src") or ""

        return src.split("/embed/")[-1].split("?")[0]

    @allure.step("Get watch-on-YouTube URL")
    def get_youtube_url(self) -> str:
        """Return the watch URL of the corresponding YouTube video."""
        with self._inside_frame():
            link = WebDriverWait(
                self.driver,
                Config.EXPLICIT_WAIT,
            ).until(
                lambda _: self.driver.find_element(
                    *self.YOUTUBE_LINK
                )
            )

            return link.get_attribute("href") or ""

    @allure.step("Check whether webinar play button is present")
    def is_play_button_present(self) -> bool:
        """Return whether the embedded player shows the play button."""
        try:
            with self._inside_frame():
                WebDriverWait(
                    self.driver,
                    Config.EXPLICIT_WAIT,
                ).until(lambda _: self.driver.find_elements(*self.PLAY_BUTTON))
                return bool(self.driver.find_elements(*self.PLAY_BUTTON))
        except Exception:
            return False

    @allure.step("Get video player bounding rect")
    def get_player_rect(self) -> dict[str, float]:
        """Return the bounding rectangle of the video iframe."""
        rect = self.root.rect

        return {
            "top": float(rect["y"]),
            "bottom": float(rect["y"] + rect["height"]),
            "left": float(rect["x"]),
            "right": float(rect["x"] + rect["width"]),
        }

    @allure.step("Get video title bounding rect")
    def get_title_rect(self) -> dict[str, float]:
        """Return the bounding rectangle of the video title."""
        title = self._find_element(self.TITLE)
        rect = title.rect

        return {
            "top": float(rect["y"]),
            "bottom": float(rect["y"] + rect["height"]),
            "left": float(rect["x"]),
            "right": float(rect["x"] + rect["width"]),
        }

    @allure.step("Scroll webinar video player into view")
    def scroll_into_view(self) -> None:
        """Scroll the video player into the center of the viewport."""
        self._scroll_to_player()

    @allure.step("Scroll webinar video title into view")
    def scroll_title_into_view(self) -> None:
        """Scroll the video title into the center of the viewport."""
        title = self._find_element(self.TITLE)

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: 'instant',
                block: 'center'
            });
            """,
            title,
        )

    @allure.step("Check whether webinar video title is fully visible")
    def is_title_fully_visible(self) -> bool:
        """Return whether the title is visible and not clipped."""
        title = self._find_element(self.TITLE)

        return bool(
            self.driver.execute_script(
                """
                const title = arguments[0];
                const player = title.nextElementSibling;

                if (!title || !player) {
                    return false;
                }

                const titleRect = title.getBoundingClientRect();
                const playerRect = player.getBoundingClientRect();

                const isVisible =
                    title.offsetParent !== null &&
                    titleRect.width > 0 &&
                    titleRect.height > 0;

                const isNotClipped =
                    title.scrollWidth <= title.clientWidth + 1 &&
                    title.scrollHeight <= title.clientHeight + 1;

                const isNotOverlapped =
                    titleRect.bottom <= playerRect.top;

                return (
                    isVisible &&
                    isNotClipped &&
                    isNotOverlapped
                );
                """,
                title,
            )
        )

    @allure.step("Check whether webinar thumbnail is loaded")
    def is_thumbnail_loaded(self) -> bool:
        """Return whether the YouTube thumbnail is visible."""
        try:
            with self._inside_frame():
                thumbnail = WebDriverWait(
                    self.driver,
                    Config.EXPLICIT_WAIT,
                ).until(
                    lambda _: self.driver.find_elements(
                        *self.THUMBNAIL
                    )
                )

                if not thumbnail:
                    return False

                element = thumbnail[0]

                return bool(
                    self.driver.execute_script(
                        """
                        const element = arguments[0];
                        const rect = element.getBoundingClientRect();

                        return (
                            rect.width > 0 &&
                            rect.height > 0
                        );
                        """,
                        element,
                    )
                )

        except Exception:
            return False

    @allure.step("Click webinar play button")
    def click_play_button(self) -> None:
        """Start the webinar video in the embedded player."""
        with self._inside_frame():
            button = WebDriverWait(
                self.driver,
                Config.EXPLICIT_WAIT,
            ).until(
                lambda _: self.driver.find_element(
                    *self.PLAY_BUTTON
                )
            )

            button.click()

    @allure.step("Check whether webinar video is playing")
    def is_video_playing(self) -> bool:
        """Return whether the webinar video is currently playing."""
        try:
            with self._inside_frame():
                state = WebDriverWait(
                    self.driver,
                    Config.EXPLICIT_WAIT,
                ).until(
                    lambda _: self._video_element_state()
                )

            if state is None:
                return False

            return (
                state["paused"] is False
                and state["error"] is None
            )

        except Exception:
            return False

    @allure.step("Click watch-on-YouTube link")
    def click_youtube_link(self) -> None:
        """Open the webinar on YouTube in a new tab."""
        with self._inside_frame():
            link = WebDriverWait(
                self.driver,
                Config.EXPLICIT_WAIT,
            ).until(
                lambda _: self.driver.find_element(
                    *self.YOUTUBE_LINK
                )
            )

            link.click()
