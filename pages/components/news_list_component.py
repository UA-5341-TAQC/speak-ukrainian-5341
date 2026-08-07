"""Component Object for the collection of news cards."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.components.news_card_component import NewsCardComponent
from pages.types import Locator


class NewsListComponent(BaseComponent):
    """Represents the list containing all news cards on the current page."""

    NEWS_CARD: Locator = (By.CSS_SELECTOR, "#newsContainer")

    def __init__(self, root: WebElement):
        """Initialize the news list component."""
        super().__init__(root)

    def get_cards(self) -> list[NewsCardComponent]:
        """Return all news cards displayed on the current page."""
        self._wait_present(self.NEWS_CARD)

        cards_web_elements = self._find_elements(self.NEWS_CARD)

        cards = []

        for card_element in cards_web_elements:
            card = NewsCardComponent(card_element)
            cards.append(card)

        return cards

    def get_card(self, index: int) -> NewsCardComponent:
        """Return a news card by zero-based index."""
        cards = self.get_cards()
        if not 0 <= index < len(cards):
            raise IndexError(
                f"News card index {index} is out of range. Available cards: {len(cards)}."
            )
        return cards[index]

    def get_first_card(self) -> NewsCardComponent:
        """Return the first news card."""
        return self.get_card(0)

    def get_cards_count(self) -> int:
        """Return the number of news cards displayed on the current page."""
        return len(self.get_cards())

    def is_empty(self) -> bool:
        """Return True when no news cards are currently rendered."""
        return len(self._find_elements(self.NEWS_CARD)) == 0
