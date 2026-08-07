"""Comment card component (single comment) on the club details page."""

from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class CommentCardComponent(BaseComponent):
    """Component for a single comment."""

    # Comment header
    AUTHOR_NAME: Locator = (By.CSS_SELECTOR, "div.author span.name")
    AVATAR_ICON: Locator = (By.CSS_SELECTOR, "div.author img.avatar")
    DATE_AND_TIME: Locator = (By.CSS_SELECTOR, "div.author span.datetime")
    RATING_WIDGET: Locator = (By.CSS_SELECTOR, "ul.ant-rate.rating")
    FILLED_STARS: Locator = (By.CSS_SELECTOR, "li.ant-rate-star-full")

    # Comment text and reply link
    COMMENT_TEXT: Locator = (By.CSS_SELECTOR, "div.ant-comment-content-detail p")
    REPLY_BUTTON: Locator = (By.CSS_SELECTOR, "button.answer-comment")

    def get_rating(self) -> int:
        """Return the number of filled stars in the comment's rating."""
        return len(self._find_elements(self.FILLED_STARS))

    def is_rating_displayed(self) -> bool:
        """Check if the rating widget is visible."""
        return self._find_element(self.RATING_WIDGET).is_displayed()

    def get_author_name(self) -> str:
        """Return the comment author's name."""
        return self._find_element(self.AUTHOR_NAME).text

    def get_avatar_icon(self) -> str | None:
        """Return the avatar image's src attribute."""
        return self._find_element(self.AVATAR_ICON).get_attribute("src")

    def get_date_and_time(self) -> str:
        """Return the comment's posted date/time."""
        return self._find_element(self.DATE_AND_TIME).text

    def get_comment_text(self) -> str:
        """Return the comment's text."""
        return self._find_element(self.COMMENT_TEXT).text

    def click_reply(self) -> None:
        """Click the "Відповісти" button."""
        self._wait_clickable(self.REPLY_BUTTON).click()
