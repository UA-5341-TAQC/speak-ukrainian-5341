"""Club details page /club/{id}."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.types import Locator


class ClubDetailsPage(BasePage):
    """Page object for a single club details page (/club/{id})."""

    # Header: banner, name, category
    TITLE: Locator = (By.CSS_SELECTOR, ".club-name")
    CATEGORY_ICON: Locator = (By.CSS_SELECTOR, ".name-box .icon-box")
    CATEGORY_TAG: Locator = (By.CSS_SELECTOR, ".tags .tag .name")
    HEADER_BANNER: Locator = (By.CSS_SELECTOR, "header.page-header")
    BLUR_OVERLAY: Locator = (By.CSS_SELECTOR, "header.page-header .blur")

    # Action buttons
    WRITE_TO_MANAGER_BUTTON: Locator = (By.CSS_SELECTOR, ".apply-box button.apply-button")
    ENROLL_BUTTON: Locator = (By.CSS_SELECTOR, ".button-box button.apply-button")
    DOWNLOAD_BUTTON: Locator = (By.CSS_SELECTOR, "button.details-button")

    # Rating
    RATING_STARS: Locator = (By.CSS_SELECTOR, ".page-rating .ant-rate")
    REVIEWS_COUNT_TEXT: Locator = (By.CSS_SELECTOR, ".page-rating .feedback")

    # Club description
    DESCRIPTION_TEXT: Locator = (By.CSS_SELECTOR, ".page-content .content")

    # Sidebar -> Address and Google Maps
    ADDRESS_TEXT: Locator = (By.CSS_SELECTOR, ".address .text")
    MAP_WIDGET: Locator = (By.CSS_SELECTOR, ".map")

    # Sidebar -> Audience age
    AGE_RANGE_LABEL: Locator = (By.CSS_SELECTOR, ".age .sider-label")
    AGE_RANGE_VALUE: Locator = (By.CSS_SELECTOR, ".age .years")

    # Sidebar -> Club's contacts
    CONTACT_WEBSITE_LINK: Locator = (By.CSS_SELECTOR, ".links .contact .contact-name a")
    CONTACT_ITEMS: Locator = (By.CSS_SELECTOR, ".links .contact .contact-name")

    # Similar clubs (поки що ця секція пуста -> тут тільки заголовок)
    SIMILAR_CLUBS_TITLE: Locator = (By.CSS_SELECTOR, ".similar-clubs .label")

    # Comments
    LEAVE_COMMENT_BUTTON: Locator = (By.CSS_SELECTOR, "button.comment-button")
    COMMENTS_LABEL: Locator = (By.CSS_SELECTOR, ".comment-label")

    def open_page(self, club_id: int) -> None:
        """Navigate to the club details page for the given club id."""
        self.driver.get(f"{self.get_base_url()}/club/{club_id}")

    def get_title(self) -> str:
        """Return the club title."""
        return self._find_element(self.TITLE).text

    def get_category(self) -> str:
        """Return the category tag text, e.g. -> 'Спортивні секції'."""
        return self._find_element(self.CATEGORY_TAG).text

    def click_enroll_button(self) -> None:
        """Click the 'Записатись на гурток' button."""
        self._wait_clickable(self.ENROLL_BUTTON).click()

    def click_write_to_manager_button(self) -> None:
        """Click the 'Написати менеджеру' button."""
        self._wait_clickable(self.WRITE_TO_MANAGER_BUTTON).click()

    def click_download_button(self) -> None:
        """Click the 'Завантажити' button."""
        self._wait_clickable(self.DOWNLOAD_BUTTON).click()

    def get_reviews_count(self) -> str:
        """Return the reviews(comments) count."""
        return self._find_element(self.REVIEWS_COUNT_TEXT).text

    def get_description(self) -> str:
        """Return the club description text."""
        return self._find_element(self.DESCRIPTION_TEXT).text

    def get_address(self) -> str:
        """Return the club address."""
        return self._find_element(self.ADDRESS_TEXT).text

    def get_age_range_value(self) -> str:
        """Return the age range value."""
        return self._find_element(self.AGE_RANGE_VALUE).text

    def get_website_url(self) -> str | None:
        """Return the club website URL (href attribute)."""
        return self._find_element(self.CONTACT_WEBSITE_LINK).get_attribute("href")

    def get_phone(self) -> str:
        """Return the club phone number."""
        # знаходимо всі елементи .contact-name (сайт і телефон)
        contacts = self.driver.find_elements(*self.CONTACT_ITEMS)

        for contact in contacts:
            if not contact.find_elements(By.TAG_NAME, "a"):
                return contact.text.strip()

        raise ValueError("Phone contact not found")

    def get_similar_clubs_title(self) -> str:
        """Return the 'Схожі гуртки' title."""
        return self._find_element(self.SIMILAR_CLUBS_TITLE).text

    def is_map_displayed(self) -> bool:
        """Check if the map widget is visible on the page."""
        return self._find_element(self.MAP_WIDGET).is_displayed()

    def is_category_icon_displayed(self) -> bool:
        """Check if the category icon is visible on the page."""
        return self._find_element(self.CATEGORY_ICON).is_displayed()

    # Перевірити потім у тестах чи повертається 200 статус
    def get_header_banner_image_url(self) -> str:
        """Return the header background image URL from its CSS style."""
        element = self._find_element(self.HEADER_BANNER)
        bg_style = element.value_of_css_property("background-image")
        return bg_style.removeprefix('url("').removesuffix('")')

    def get_blur_filter_value(self) -> str:
        """Return the CSS filter of the blur overlay."""
        element = self._find_element(self.BLUR_OVERLAY)
        return element.value_of_css_property("filter")

    def is_rating_stars_displayed(self) -> bool:
        """Check if the star rating widget is visible on the page."""
        return self._find_element(self.RATING_STARS).is_displayed()

    def get_age_range_label(self) -> str:
        """Return the age range label text -> 'Вік аудиторії:'."""
        return self._find_element(self.AGE_RANGE_LABEL).text

    def click_leave_comment_button(self) -> None:
        """Click the 'Залишити коментар' button, which opens the leave comment modal."""
        self._wait_clickable(self.LEAVE_COMMENT_BUTTON).click()

    def is_comments_label_displayed(self) -> bool:
        """Check if the 'Коментарі' section title is displayed."""
        return self._find_element(self.COMMENTS_LABEL).is_displayed()
