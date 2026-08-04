import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from components.base_component import BaseComponent


class SocialButtons(BaseComponent):
    """Encapsulates the social media buttons and donation block component."""

    SOCIAL_SECTION_TITLE = (By.CSS_SELECTOR, ".social-info .text, .social-media .text")
    FACEBOOK_BUTTON = (By.CSS_SELECTOR, ".social-info a[href*='facebook.com']")
    YOUTUBE_BUTTON = (By.CSS_SELECTOR, ".social-info a[href*='youtube.com']")
    INSTAGRAM_BUTTON = (By.CSS_SELECTOR, ".social-info a[href*='instagram.com']")
    MAIL_BUTTON = (By.CSS_SELECTOR, ".social-info a[href^='mailto:']")
    DONATE_BUTTON = (By.CSS_SELECTOR, ".help-button .donate-button")

    def __init__(self, driver, root_element: WebElement):
        super().__init__(driver, root_element)

    @allure.step("Get social media section title text")
    def get_social_section_title_text(self) -> str:
        return self.root.find_element(*self.SOCIAL_SECTION_TITLE).text

    @allure.step("Get Facebook link URL")
    def get_facebook_url(self) -> str:
        return self.root.find_element(*self.FACEBOOK_BUTTON).get_attribute("href")

    @allure.step("Click Facebook button")
    def click_facebook_button(self) -> None:
        self.root.find_element(*self.FACEBOOK_BUTTON).click()

    @allure.step("Get YouTube link URL")
    def get_youtube_url(self) -> str:
        return self.root.find_element(*self.YOUTUBE_BUTTON).get_attribute("href")

    @allure.step("Click YouTube button")
    def click_youtube_button(self) -> None:
        self.root.find_element(*self.YOUTUBE_BUTTON).click()

    @allure.step("Get Instagram link URL")
    def get_instagram_url(self) -> str:
        return self.root.find_element(*self.INSTAGRAM_BUTTON).get_attribute("href")

    @allure.step("Click Instagram button")
    def click_instagram_button(self) -> None:
        self.root.find_element(*self.INSTAGRAM_BUTTON).click()

    @allure.step("Get email address from mailto link")
    def get_email_address(self) -> str:
        href = self.root.find_element(*self.MAIL_BUTTON).get_attribute("href")
        return href.replace("mailto:", "")

    @allure.step("Get Donate button text")
    def get_donate_button_text(self) -> str:
        return self.root.find_element(*self.DONATE_BUTTON).text

    @allure.step("Get Donate payment link URL")
    def get_donate_url(self) -> str:
        return self.root.find_element(*self.DONATE_BUTTON).get_attribute("href")

    @allure.step("Click 'Donate' button")
    def click_donate_button(self) -> None:
        self.root.find_element(*self.DONATE_BUTTON).click()