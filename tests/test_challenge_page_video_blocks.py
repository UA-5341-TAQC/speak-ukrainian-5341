"""Tests for the webinar video blocks on the challenge page."""

from collections.abc import Generator
from contextlib import contextmanager
from urllib.parse import parse_qs, urlparse

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from data.config import Config
from pages.challenge_page import ChallengePage


@contextmanager
def _switch_to_last_tab(
    driver: WebDriver,
) -> Generator[WebDriver, None, None]:
    """Switch to the newest browser tab and restore the original tab."""
    original_handle = driver.current_window_handle
    handles = driver.window_handles

    driver.switch_to.window(handles[-1])

    try:
        yield driver
    finally:
        driver.close()
        driver.switch_to.window(original_handle)


@allure.title(
    "TC-63 Verify video blocks playback and YouTube links "
    "on the challenge page"
)
@pytest.mark.regression
def test_challenge_page_video_blocks(
    driver: WebDriver,
) -> None:
    """Verify webinar video blocks, playback and YouTube links."""
    challenge_page = ChallengePage(driver)

    with allure.step("Open the challenge page"):
        challenge_page.open(2)
        video_cards = challenge_page.wait_for_video_cards()

    with allure.step("Verify all video blocks are present"):
        assert video_cards, (
            "No video blocks found on the challenge page"
        )

        assert len(video_cards) == 4, (
            "Content discrepancy: expected 4 video blocks, "
            f"found {len(video_cards)}"
        )

        for index, card in enumerate(
            video_cards,
            start=1,
        ):
            with allure.step(
                f"Verify video block {index}"
            ):
                card.scroll_into_view()

                assert card.get_title_text(), (
                    f"Video block {index} has no title"
                )

                assert card.is_thumbnail_loaded(), (
                    f"Video block {index} "
                    "thumbnail is not loaded"
                )

                assert card.is_play_button_present(), (
                    f"Video block {index} "
                    "has no play button"
                )

                youtube_url = card.get_youtube_url()

                assert youtube_url.startswith(
                    "https://www.youtube.com/watch?"
                ), (
                    f"Video block {index} has no valid "
                    "watch-on-YouTube link"
                )

    with allure.step(
        "Verify CTA button does not overlap the last video"
    ):
        challenge_page.scroll_cta_button_into_view()

        cta_rect = challenge_page.get_cta_button_rect()
        last_card_rect = video_cards[-1].get_player_rect()

        assert cta_rect["top"] >= last_card_rect["bottom"], (
            "The 'Записатись на челендж' button overlaps "
            "the last video block"
        )

    # Verify YouTube links BEFORE starting the videos.
    for index, card in enumerate(
        video_cards,
        start=1,
    ):
        with allure.step(
            f"Open YouTube link for video block {index}"
        ):
            expected_video_id = card.get_video_id()

            card.scroll_into_view()

            initial_tab_count = len(
                driver.window_handles
            )

            card.click_youtube_link()

            WebDriverWait(
                driver,
                Config.EXPLICIT_WAIT,
            ).until(
                lambda current_driver:
                len(current_driver.window_handles)
                == initial_tab_count + 1
            )

            with _switch_to_last_tab(driver) as youtube_tab:
                WebDriverWait(
                    youtube_tab,
                    Config.EXPLICIT_WAIT,
                ).until(
                    lambda current_driver:
                    "youtube.com"
                    in urlparse(
                        current_driver.current_url
                    ).netloc
                )

                current_url = youtube_tab.current_url
                parsed_url = urlparse(current_url)

                assert "youtube.com" in parsed_url.netloc, (
                    f"Video block {index}: "
                    "new tab is not a YouTube page"
                )

                query = parse_qs(parsed_url.query)

                opened_video_id = query.get(
                    "v",
                    [""],
                )[0]

                assert opened_video_id == expected_video_id, (
                    f"Video block {index}: opened video "
                    f"{opened_video_id} does not match "
                    f"embed {expected_video_id}"
                )

                WebDriverWait(
                    youtube_tab,
                    Config.EXPLICIT_WAIT,
                ).until(
                    lambda current_driver:
                    current_driver.execute_script(
                        "return document.readyState"
                    )
                    == "complete"
                )

    assert len(driver.window_handles) == 1, (
        "Not all YouTube tabs were closed"
    )

    # Start videos only after all YouTube links were verified.
    for index, card in enumerate(
        video_cards,
        start=1,
    ):
        with allure.step(
            f"Play video block {index}"
        ):
            card.scroll_into_view()
            card.click_play_button()

            WebDriverWait(
                driver,
                Config.EXPLICIT_WAIT,
            ).until(
                lambda _: card.is_video_playing()
            )

            assert card.is_video_playing(), (
                f"Video block {index} "
                "did not start playing inline"
            )

    with allure.step(
        "Resize the browser window to 1024px"
    ):
        driver.set_window_size(
            1024,
            900,
        )

        for index, card in enumerate(
            video_cards,
            start=1,
        ):
            with allure.step(
                f"Verify video block {index} "
                "title is not clipped"
            ):
                card.scroll_title_into_view()

                assert card.is_title_fully_visible(), (
                    f"Video block {index} title is "
                    "cut off or overlapped at 1024px width"
                )
