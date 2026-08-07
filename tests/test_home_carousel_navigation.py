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

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from data.config import Config
from pages.components.carousel import Carousel
from pages.home_page import HomePage

# Path fragments of the pages each carousel slide must lead to (TC-29 steps 2, 5, 8).
CHALLENGE_PAGE = "/challenges"
CLUBS_PAGE = "/clubs"
ABOUT_PAGE = "/about"


def _active_link_href(carousel: Carousel) -> str:
    """Return the href of the currently active carousel slide's button."""
    active = carousel.get_active_item()
    link = active._find_element(active.LINK)
    return (link.get_attribute("href") or "").rstrip("/")


def _pause_autoplay_and_sync(
    home: HomePage, driver: WebDriver, wait: WebDriverWait[WebDriver]
) -> Carousel:
    """Pause the carousel autoplay and bring it back to the first slide.

    Hovering the carousel pauses slick's autoplay; arrow clicks then shift one
    slide deterministically. The carousel is walked forward (bounded) until the
    challenge ("Єдині") slide - the first one - is focused again.
    """
    first_slide = home._find_element(home.CAROUSEL)
    ActionChains(driver).move_to_element(first_slide).perform()
    carousel: Carousel = home.get_carousel()
    wait.until(lambda _: bool(_active_link_href(carousel)))
    for _ in range(3):
        if CHALLENGE_PAGE in _active_link_href(carousel):
            return carousel
        carousel.click_next_arrow()
        wait.until(lambda _: bool(_active_link_href(carousel)))
    raise AssertionError("The carousel could not be brought back to the first (challenge) slide.")


def test_homepage_carousel_navigation(driver: WebDriver) -> None:
    """Verify homepage hero carousel navigation and its slide redirects."""
    home = HomePage(driver)
    driver.get(Config.BASE_UI_URL.rstrip("/") + "/")
    wait = WebDriverWait(driver, 12)

    # Step 1: locate the carousel section -> the carousel is displayed.
    home._wait_visible(home.CAROUSEL)
    assert home._find_element(home.CAROUSEL).is_displayed()

    # Step 2: click the button on the first slide -> challenge "Єдині" page.
    first = _pause_autoplay_and_sync(home, driver, wait)
    first_url = _active_link_href(first)
    assert CHALLENGE_PAGE in first_url
    first.get_active_item().click_details_button()
    wait.until(lambda d: d.current_url.rstrip("/") == first_url)
    assert CHALLENGE_PAGE in driver.current_url

    # Step 3: go back to the homepage -> homepage is displayed again.
    driver.back()
    wait.until(lambda _: home._find_element(home.CAROUSEL).is_displayed())

    # Step 4: click the right arrow -> the second slide is displayed.
    second = _pause_autoplay_and_sync(home, driver, wait)
    first_href = _active_link_href(second)
    second.click_next_arrow()
    wait.until(lambda _: _active_link_href(second) != first_href)
    second_url = _active_link_href(second)
    assert CLUBS_PAGE in second_url

    # Step 5: click the button on the second slide -> Clubs page.
    second.get_active_item().click_details_button()
    wait.until(lambda d: d.current_url.rstrip("/") == second_url)
    assert CLUBS_PAGE in driver.current_url

    # Step 6: go back to the homepage -> homepage is displayed again.
    driver.back()
    wait.until(lambda _: home._find_element(home.CAROUSEL).is_displayed())

    # Step 7: click the right arrow twice -> the third slide is displayed.
    third = _pause_autoplay_and_sync(home, driver, wait)
    previous_url = _active_link_href(third)
    third.click_next_arrow()
    wait.until(lambda _: _active_link_href(third) != previous_url)
    previous_url = _active_link_href(third)
    third.click_next_arrow()
    wait.until(lambda _: _active_link_href(third) != previous_url)
    third_url = _active_link_href(third)
    assert ABOUT_PAGE in third_url

    # Step 8: click the button on the third slide -> About page.
    third.get_active_item().click_details_button()
    wait.until(lambda d: d.current_url.rstrip("/") == third_url)
    assert ABOUT_PAGE in driver.current_url
