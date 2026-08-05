"""Page object for the About Us page on the Speak Ukrainian website."""

import allure
from components.social_buttons import SocialButtons
from pages.base_page import BasePage
from pages.types import Locator
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class AboutUsPage(BasePage):
    """Page object representing the 'About Us / About the Initiative' page."""

    HEADER_TITLE: Locator = (By.CSS_SELECTOR, ".about-header .city-name")
    SEARCH_INPUT: Locator = (By.CSS_SELECTOR, ".search input.ant-select-selection-search-input")
    SEARCH_ICON: Locator = (By.CSS_SELECTOR, ".search-icon-group .anticon-search")
    ADVANCED_SEARCH_ICON: Locator = (By.CSS_SELECTOR, ".search-icon-group .anticon-control")

    BANNER_TITLE: Locator = (By.CSS_SELECTOR, ".title .text")
    BANNER_SUBTITLE: Locator = (By.CSS_SELECTOR, ".title .content")

    SECTION_TITLES: Locator = (By.CSS_SELECTOR, "div.title-content")
    ALL_PARAGRAPHS: Locator = (By.CSS_SELECTOR, ".content-text p")

    MEMBER_NAMES: Locator = (By.CSS_SELECTOR, "span.chapter")
    MEMBER_ROLES: Locator = (By.CSS_SELECTOR, "span.highlight")

    PROMO_VIDEO_IFRAME: Locator = (By.CSS_SELECTOR, ".video iframe")
    CONTENT_IMAGES: Locator = (By.CSS_SELECTOR, "img.image")

    def __init__(self, driver: WebDriver) -> None:
        """Initialize AboutUsPage with sub-components."""
        super().__init__(driver)

    @property
    @allure.step("Access Social Buttons component")
    def social_buttons(self) -> SocialButtons:
        """Get the SocialButtons sub-component instance."""
        return SocialButtons(self.driver)

    @allure.step("Get main header page title text")
    def get_header_title_text(self) -> str:
        """Get main header title text."""
        return self._find_element(self.HEADER_TITLE).text.strip()

    @allure.step("Enter text into search input: {query}")
    def enter_search_query(self, query: str) -> "AboutUsPage":
        """Clear search field using React-friendly clear and enter search query."""
        search_input = self._find_element(self.SEARCH_INPUT)
        self.clear(search_input)
        search_input.send_keys(query)
        return self

    @allure.step("Click search icon")
    def click_search_icon(self) -> None:
        """Click search icon to submit search query."""
        self._find_element(self.SEARCH_ICON).click()

    @allure.step("Click advanced search icon")
    def click_advanced_search_icon(self) -> None:
        """Click advanced search icon to open filter options."""
        self._find_element(self.ADVANCED_SEARCH_ICON).click()

    @allure.step("Get banner title text")
    def get_banner_title_text(self) -> str:
        """Get title text from the main banner."""
        return self._find_element(self.BANNER_TITLE).text.strip()

    @allure.step("Get banner subtitle text")
    def get_banner_subtitle_text(self) -> str:
        """Get subtitle text from the main banner."""
        return self._find_element(self.BANNER_SUBTITLE).text.strip()

    @allure.step("Get list of section titles on the page")
    def get_section_titles(self) -> list[str]:
        """Get list of all section title texts present on the page."""
        elements = self._find_elements(self.SECTION_TITLES)
        return [el.text.strip() for el in elements if el.text.strip()]

    @allure.step("Get team members info (name -> role)")
    def get_team_members_info(self) -> dict[str, str]:
        """Get a dictionary mapping member names to their roles."""
        names = self._find_elements(self.MEMBER_NAMES)
        roles = self._find_elements(self.MEMBER_ROLES)

        return {
            name_el.text.strip(): role_el.text.strip()
            for name_el, role_el in zip(names, roles)
            if name_el.text.strip()
        }

    @allure.step("Get promo video embed URL")
    def get_promo_video_url(self) -> str:
        """Get source URL of the embedded promo video."""
        iframe = self._find_element(self.PROMO_VIDEO_IFRAME)
        return iframe.get_attribute("src") or ""

    @allure.step("Get total count of content images")
    def get_content_images_count(self) -> int:
        """Get total number of content images on the page."""
        return len(self._find_elements(self.CONTENT_IMAGES))

    @allure.step("Get all text paragraphs on the page")
    def get_all_paragraphs_text(self) -> list[str]:
        """Get list of text from all content paragraphs."""
        paragraphs = self._find_elements(self.ALL_PARAGRAPHS)
        return [p.text.strip() for p in paragraphs if p.text.strip()]
