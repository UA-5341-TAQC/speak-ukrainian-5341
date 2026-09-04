"""Automated test for TC-29 "Verify homepage carousel navigation".

Maps 1:1 to the test steps of issue UA-5341-TAQC/speak-ukrainian-5341#29:

  Step 1  Locate the carousel section                      -> Carousel is displayed.
  Step 2  Click the button on the first carousel slide     -> Challenge "Єдині" page.
  Step 3  Navigate back to the homepage                    -> Homepage is displayed again.
  Step 4  Click the right carousel navigation arrow        -> Second slide is displayed.
  Step 5  Click the button on the second slide             -> Clubs page.
  Step 6  Navigate back to the homepage                    -> Homepage is displayed again.
  Step 7  Click the right carousel navigation arrow twice  -> Third slide is displayed.
  Step 8  Click the button on the third slide              -> About page.

The hero carousel autoplays (it advances roughly every 4 seconds), so the test
pauses autoplay by hovering the carousel (slick's pause-on-hover) and then
synchronizes the carousel to the expected slide before interacting. This keeps
the "first/second/third slide" assertion deterministic.
"""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.home_page import HomePage


def test_homepage_carousel_navigation(driver: WebDriver) -> None:
    """Verify homepage hero carousel navigation and its slide redirects."""
    home = HomePage(driver)
    driver.get(Config.BASE_UI_URL.rstrip("/") + "/")

    # Step 1: locate the carousel section -> the carousel is displayed.
    assert home.is_carousel_displayed(), "Expected homepage hero carousel to be displayed."

    slide_count = home.get_carousel_slide_count()
    if slide_count < 2:
        pytest.skip(
            f"Carousel on current environment contains {slide_count} slide(s); "
            "navigation arrows are only rendered when multiple slides exist."
        )

    # Step 2: click the button on the first slide -> challenge "Єдині" page.
    first = home.pause_autoplay_and_sync()
    first_url = first.get_active_link_href()
    assert HomePage.CHALLENGE_PAGE in first_url
    first.get_active_item().click_details_button()
    home._wait_for_url(first_url)
    assert HomePage.CHALLENGE_PAGE in driver.current_url

    # Step 3: go back to the homepage -> homepage is displayed again.
    driver.back()
    assert home.wait_loaded().is_carousel_displayed()

    # Step 4: click the right arrow -> the second slide is displayed.
    second = home.pause_autoplay_and_sync()
    first_href = second.get_active_link_href()
    second.click_next_arrow()
    home.wait.until(lambda _: second.get_active_link_href() != first_href)
    second_url = second.get_active_link_href()
    assert HomePage.CLUBS_PAGE in second_url

    # Step 5: click the button on the second slide -> Clubs page.
    second.get_active_item().click_details_button()
    home._wait_for_url(second_url)
    assert HomePage.CLUBS_PAGE in driver.current_url

    # Step 6: go back to the homepage -> homepage is displayed again.
    driver.back()
    assert home.wait_loaded().is_carousel_displayed()

    # Step 7: click the right arrow twice -> the third slide is displayed.
    third = home.pause_autoplay_and_sync()
    previous_url = third.get_active_link_href()
    third.click_next_arrow()
    home.wait.until(lambda _: third.get_active_link_href() != previous_url)
    previous_url = third.get_active_link_href()
    third.click_next_arrow()
    home.wait.until(lambda _: third.get_active_link_href() != previous_url)
    third_url = third.get_active_link_href()
    assert HomePage.ABOUT_PAGE in third_url

    # Step 8: click the button on the third slide -> About page.
    third.get_active_item().click_details_button()
    home._wait_for_url(third_url)
    assert HomePage.ABOUT_PAGE in driver.current_url
