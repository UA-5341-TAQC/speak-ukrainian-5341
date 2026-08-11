"""Component object for a challenge webinar video block.

Each video block on the challenge page is a Quill rich-text pair: a title
heading followed by an embedded YouTube iframe. This component wraps the
iframe element and exposes operations on the embedded YouTube player:
the thumbnail preview, the play button and the watch-on-YouTube link live
inside the YouTube iframe, while the block title is the heading positioned
directly before the iframe in the description markup.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from typing import cast

import allure
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from data.config import Config
from pages.components.base_component import BaseComponent
from pages.types import Locator


class ChallengeVideoCard(BaseComponent):
    """Represent one webinar video block on a challenge page."""

    TITLE: Locator = (By.XPATH, "./preceding-sibling::h1[1]")
    THUMBNAIL: Locator = (By.CSS_SELECTOR, "div.ytmVideoCoverThumbnail")
    PLAY_BUTTON: Locator = (By.CSS_SELECTOR, "button[aria-label='Відтворити відео']")
    YOUTUBE_LINK: Locator = (By.CSS_SELECTOR, "a[href*='youtube.com/watch']")

    def __init__(self, root: WebElement) -> None:
        """Initialize the video card with the embedded YouTube iframe element."""
        super().__init__(root)

    @contextmanager
    def _inside_frame(self) -> Iterator[None]:
        """Temporarily switch the WebDriver context into the embedded YouTube player."""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.root)
        wait: WebDriverWait[WebDriver] = WebDriverWait(
            self.driver,
            Config.EXPLICIT_WAIT,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        )
        wait.until(lambda _: len(self.driver.find_elements(*self.YOUTUBE_LINK)) > 0)
        try:
            yield
        finally:
            self.driver.switch_to.default_content()

    def _video_element_state(self) -> dict[str, object] | None:
        """Return {paused, error} of the embedded player's video element."""
        state = self.driver.execute_script(
            "var v = document.querySelector('video');"
            "return v ? {paused: v.paused, error: v.error ? v.error.code : null} : null;"
        )
        return cast(dict[str, object] | None, state)

    @allure.step("Get webinar video title")
    def get_title_text(self) -> str:
        """Return the webinar title shown above the video."""
        return self._find_element(self.TITLE).text.strip()

    @allure.step("Get embedded YouTube video id")
    def get_video_id(self) -> str:
        """Return the YouTube video id from the embed source URL."""
        src = self.root.get_attribute("src") or ""
        return src.split("/embed/")[-1].split("?")[0]

    @allure.step("Get watch-on-YouTube URL")
    def get_youtube_url(self) -> str:
        """Return the watch URL of the corresponding YouTube video."""
        with self._inside_frame():
            return self.driver.find_element(*self.YOUTUBE_LINK).get_attribute("href") or ""

    @allure.step("Check whether webinar play button is present")
    def is_play_button_present(self) -> bool:
        """Return whether the embedded player shows the play button."""
        with self._inside_frame():
            return len(self.driver.find_elements(*self.PLAY_BUTTON)) > 0

    def _get_element_rect(self, element: WebElement) -> dict[str, float]:
        """Return the on-screen bounding rectangle of an element in the parent document."""
        rect = self.driver.execute_script(
            "var r = arguments[0].getBoundingClientRect();"
            "return {top: r.top, bottom: r.bottom, left: r.left, right: r.right};",
            element,
        )
        return {key: float(value) for key, value in rect.items()}

    @allure.step("Get video player bounding rect")
    def get_player_rect(self) -> dict[str, float]:
        """Return the on-screen rectangle of the embedded video player."""
        return self._get_element_rect(self.root)

    @allure.step("Get video title bounding rect")
    def get_title_rect(self) -> dict[str, float]:
        """Return the on-screen rectangle of the video title heading."""
        return self._get_element_rect(self._find_element(self.TITLE))

    @allure.step("Scroll webinar video player into view")
    def scroll_into_view(self) -> None:
        """Scroll the embedded player into the center of the viewport."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
            self.root,
        )

    @allure.step("Scroll webinar video title into view")
    def scroll_title_into_view(self) -> None:
        """Scroll the video title heading into the center of the viewport."""
        element = self._find_element(self.TITLE)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
            element,
        )

    @allure.step("Check whether webinar video title is fully visible")
    def is_title_fully_visible(self) -> bool:
        """Return whether the video title is visible and not clipped or overlapped."""
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
        """Return whether the thumbnail preview is visible and has an image source."""
        with self._inside_frame():
            thumbnail = self.driver.find_element(*self.THUMBNAIL)
            style = thumbnail.value_of_css_property("background-image")
            rect = self.driver.execute_script(
                "var e = arguments[0]; var r = e.getBoundingClientRect();"
                "return {width: r.width, height: r.height};",
                thumbnail,
            )
        has_source = style not in ("", "none")
        has_size = float(rect["width"]) > 0 and float(rect["height"]) > 0
        return has_source and has_size

    @allure.step("Click webinar play button")
    def click_play_button(self) -> None:
        """Start the webinar video in the embedded player."""
        with self._inside_frame():
            self.driver.find_element(*self.PLAY_BUTTON).click()

    @allure.step("Check whether webinar video is playing")
    def is_video_playing(self) -> bool:
        """Return whether the embedded video is playing without a loading error."""
        with self._inside_frame():
            state = self._video_element_state()
        if state is None:
            return False
        return state["paused"] is False and state["error"] is None

    @allure.step("Click watch-on-YouTube link")
    def click_youtube_link(self) -> None:
        """Open the webinar on YouTube in a new tab."""
        with self._inside_frame():
            link = self.driver.find_element(*self.YOUTUBE_LINK)
            self.driver.execute_script("arguments[0].click();", link)
