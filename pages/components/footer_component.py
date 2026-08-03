"""Page object for the Footer component of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from pages.components.base_component import BaseComponent

DEFAULT_TIMEOUT: int = 10


class FooterComponent(BaseComponent):
    """Component representing the Speak Ukrainian footer."""

    FOOTER_LOGO: tuple[str, str] = (By.CSS_SELECTOR, "footer .footer-logo")
    DESCRIPTION_TEXT: tuple[str, str] = (By.CSS_SELECTOR, "footer .description .text")
    COPYRIGHT_TEXT: tuple[str, str] = (By.CSS_SELECTOR, "footer .qubstudio")

    FACEBOOK_LINK: tuple[str, str] = (
        By.CSS_SELECTOR,
        "footer a[href*='facebook.com/teach.in.ukrainian']",
    )
    YOUTUBE_LINK: tuple[str, str] = (
        By.CSS_SELECTOR,
        "footer a[href*='youtube.com/channel']",
    )
    INSTAGRAM_LINK: tuple[str, str] = (
        By.CSS_SELECTOR,
        "footer a[href*='instagram.com/yedyni.ruh']",
    )

    SOFT_SERVE_LOGO: tuple[str, str] = (By.CSS_SELECTOR, "footer img[alt='soft_serve']")
    MOVA_OBYEDNUE_LOGO: tuple[str, str] = (By.CSS_SELECTOR, "footer img[alt='Mova_obyednue']")
    EDERA_LOGO: tuple[str, str] = (By.CSS_SELECTOR, "footer img[alt='EDERA']")
    EMOVA_LOGO: tuple[str, str] = (By.CSS_SELECTOR, "footer img[alt='e-mova']")
    KRAINA_FM_LOGO: tuple[str, str] = (By.CSS_SELECTOR, "footer img[alt='Kraina_FM']")
    UCF_LOGO: tuple[str, str] = (By.CSS_SELECTOR, "footer img[alt='ucf']")
    PROSTIR_SVOBODI_LOGO: tuple[str, str] = (By.CSS_SELECTOR, "footer img[alt='prostir_svobodi']")

    DONATE_BUTTON: tuple[str, str] = (
        By.CSS_SELECTOR,
        "footer .donate-button",
    )
    DONATE_DESCRIPTION: tuple[str, str] = (By.CSS_SELECTOR, "footer .footer-donate .desc")

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Initialize the footer component.

        Args:
            driver: Selenium WebDriver instance.
            timeout: Maximum time in seconds to wait for elements.
        """
        super().__init__(driver)
        self.wait = WebDriverWait(driver, timeout)


    @allure.step("Click footer logo")
    def click_footer_logo(self) -> None:
        """Click the footer logo."""
        self._click_clickable(self.FOOTER_LOGO)

    @allure.step("Click Facebook link in footer")
    def click_facebook_link(self) -> None:
        """Click the Facebook social link."""
        self._click_clickable(self.FACEBOOK_LINK)

    @allure.step("Click YouTube link in footer")
    def click_youtube_link(self) -> None:
        """Click the YouTube social link."""
        self._click_clickable(self.YOUTUBE_LINK)

    @allure.step("Click Instagram link in footer")
    def click_instagram_link(self) -> None:
        """Click the Instagram social link."""
        self._click_clickable(self.INSTAGRAM_LINK)

    @allure.step("Click 'Допомогти проєкту' donate button")
    def click_donate_button(self) -> None:
        """Click the donate button in footer."""
        self._click_clickable(self.DONATE_BUTTON)


    @allure.step("Click SoftServe partner logo")
    def click_softserve_logo(self) -> None:
        """Click SoftServe partner logo."""
        self._click_clickable(self.SOFT_SERVE_LOGO)

    @allure.step("Click EDERA partner logo")
    def click_edera_logo(self) -> None:
        """Click EDERA partner logo."""
        self._click_clickable(self.EDERA_LOGO)

    @allure.step("Click MovaObyednue partner logo")
    def click_mova_obyednue_logo(self) -> None:
        """Click MovaObyednue partner logo."""
        self._click_clickable(self.MOVA_OBYEDNUE_LOGO)

    @allure.step("Click Emova partner logo")
    def click_emova_logo(self) -> None:
        """Click Emova partner logo."""
        self._click_clickable(self.EMOVA_LOGO)

    @allure.step("Click KrainaFM partner logo")
    def click_kraina_fm_logo(self) -> None:
        """Click KrainaFM partner logo."""
        self._click_clickable(self.KRAINA_FM_LOGO)

    @allure.step("Click UCF partner logo")
    def click_ucf_logo(self) -> None:
        """Click UCF partner logo."""
        self._click_clickable(self.UCF_LOGO)

    @allure.step("Click prostirsvobodi partner logo")
    def click_prostir_svobodi_logo(self) -> None:
        """Click Prostirsvobodi partner logo."""
        self._click_clickable(self.PROSTIR_SVOBODI_LOGO)


    @allure.step("Get footer description text")
    def get_description_text(self) -> str:
        """Retrieve main description text from footer."""
        return self._wait_visible(self.DESCRIPTION_TEXT).text.strip()

    @allure.step("Get copyright text")
    def get_copyright_text(self) -> str:
        """Retrieve copyright and development info text."""
        return self._wait_visible(self.COPYRIGHT_TEXT).text.strip()

    @allure.step("Get donate block description text")
    def get_donate_description_text(self) -> str:
        """Retrieve description text from donate block."""
        return self._wait_visible(self.DONATE_DESCRIPTION).text.strip()


    def _wait_clickable(self, locator: tuple[str, str]) -> WebElement:
        """Wait until an element matching the locator is clickable.

        Args:
            locator: Selenium locator of the element.

        Returns:
            The clickable WebElement.
        """
        return self.wait.until(ec.element_to_be_clickable(locator))

    def _wait_visible(self, locator: tuple[str, str]) -> WebElement:
        """Wait until an element matching the locator is visible.

        Args:
            locator: Selenium locator of the element.

        Returns:
            The visible WebElement.
        """
        return self.wait.until(ec.visibility_of_element_located(locator))

    def _click_clickable(self, locator: tuple[str, str]) -> None:
        """Wait for an element to become clickable and click it.

        Args:
            locator: Selenium locator of the element.
        """
        element = self._wait_clickable(locator)
        element.click()