"""Page object for the Footer component of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.types import Locator


class FooterComponent(BaseComponent):
    """Component representing the Speak Ukrainian footer."""

    FOOTER_LOGO: Locator = (By.CSS_SELECTOR, "footer .footer-logo")
    DESCRIPTION_TEXT: Locator = (By.CSS_SELECTOR, "footer .description .text")
    COPYRIGHT_TEXT: Locator = (By.CSS_SELECTOR, "footer .qubstudio")

    FACEBOOK_LINK: Locator = (
        By.CSS_SELECTOR,
        "footer a[href*='facebook.com/teach.in.ukrainian']",
    )
    YOUTUBE_LINK: Locator = (
        By.CSS_SELECTOR,
        "footer a[href*='youtube.com/channel']",
    )
    INSTAGRAM_LINK: Locator = (
        By.CSS_SELECTOR,
        "footer a[href*='instagram.com/yedyni.ruh']",
    )

    SOFT_SERVE_LOGO: Locator = (By.CSS_SELECTOR, "footer img[alt='soft_serve']")
    MOVA_OBYEDNUE_LOGO: Locator = (By.CSS_SELECTOR, "footer img[alt='Mova_obyednue']")
    EDERA_LOGO: Locator = (By.CSS_SELECTOR, "footer img[alt='EDERA']")
    EMOVA_LOGO: Locator = (By.CSS_SELECTOR, "footer img[alt='e-mova']")
    KRAINA_FM_LOGO: Locator = (By.CSS_SELECTOR, "footer img[alt='Kraina_FM']")
    UCF_LOGO: Locator = (By.CSS_SELECTOR, "footer img[alt='ucf']")
    PROSTIR_SVOBODI_LOGO: Locator = (By.CSS_SELECTOR, "footer img[alt='prostir_svobodi']")

    DONATE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "footer .donate-button",
    )
    DONATE_DESCRIPTION: Locator = (By.CSS_SELECTOR, "footer .footer-donate .desc")

    def __init__(self, root: WebElement) -> None:
        """Initialize FooterComponent with the root element."""
        super().__init__(root)

    @allure.step("Click footer logo")
    def click_footer_logo(self) -> None:
        """Click the footer logo."""
        self._find_element(self.FOOTER_LOGO).click()

    @allure.step("Click Facebook link in footer")
    def click_facebook_link(self) -> None:
        """Click the Facebook social link."""
        self._find_element(self.FACEBOOK_LINK).click()

    @allure.step("Click YouTube link in footer")
    def click_youtube_link(self) -> None:
        """Click the YouTube social link."""
        self._find_element(self.YOUTUBE_LINK).click()

    @allure.step("Click Instagram link in footer")
    def click_instagram_link(self) -> None:
        """Click the Instagram social link."""
        self._find_element(self.INSTAGRAM_LINK).click()

    @allure.step("Click 'Допомогти проєкту' donate button")
    def click_donate_button(self) -> None:
        """Click the donate button in footer."""
        self._find_element(self.DONATE_BUTTON).click()

    @allure.step("Click SoftServe partner logo")
    def click_softserve_logo(self) -> None:
        """Click SoftServe partner logo."""
        self._find_element(self.SOFT_SERVE_LOGO).click()

    @allure.step("Click EDERA partner logo")
    def click_edera_logo(self) -> None:
        """Click EDERA partner logo."""
        self._find_element(self.EDERA_LOGO).click()

    @allure.step("Click MovaObyednue partner logo")
    def click_mova_obyednue_logo(self) -> None:
        """Click MovaObyednue partner logo."""
        self._find_element(self.MOVA_OBYEDNUE_LOGO).click()

    @allure.step("Click Emova partner logo")
    def click_emova_logo(self) -> None:
        """Click Emova partner logo."""
        self._find_element(self.EMOVA_LOGO).click()

    @allure.step("Click KrainaFM partner logo")
    def click_kraina_fm_logo(self) -> None:
        """Click KrainaFM partner logo."""
        self._find_element(self.KRAINA_FM_LOGO).click()

    @allure.step("Click UCF partner logo")
    def click_ucf_logo(self) -> None:
        """Click UCF partner logo."""
        self._find_element(self.UCF_LOGO).click()

    @allure.step("Click prostirsvobodi partner logo")
    def click_prostir_svobodi_logo(self) -> None:
        """Click Prostirsvobodi partner logo."""
        self._find_element(self.PROSTIR_SVOBODI_LOGO).click()

    @allure.step("Get footer description text")
    def get_description_text(self) -> str:
        """Retrieve main description text from footer."""
        return self._find_element(self.DESCRIPTION_TEXT).text.strip()

    @allure.step("Get copyright text")
    def get_copyright_text(self) -> str:
        """Retrieve copyright and development info text."""
        return self._find_element(self.COPYRIGHT_TEXT).text.strip()

    @allure.step("Get donate block description text")
    def get_donate_description_text(self) -> str:
        """Retrieve description text from donate block."""
        return self._find_element(self.DONATE_DESCRIPTION).text.strip()
