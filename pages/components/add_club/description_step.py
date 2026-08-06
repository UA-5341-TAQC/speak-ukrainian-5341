from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.modals.add_club_modal import AddClubModal
from pages.types import Locator


class DescriptionStep(AddClubModal):
    """Page object for the Description step (Опис) of the Add Club modal."""

    LOGO_UPLOAD_INPUT: Locator = (By.ID, "basic_urlLogo")
    COVER_UPLOAD_INPUT: Locator = (By.ID, "basic_urlBackground")
    GALLERY_UPLOAD_INPUT: Locator = (
        By.CSS_SELECTOR,
        ".ant-upload-picture-card-wrapper input[type='file']",
    )
    VIEW_UPLOAD_IMG_BUTTON: Locator = (
        By.CSS_SELECTOR,
       "span[aria-label='eye']"
    )
    DELETE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "span[aria-label='delete']"
    )

    DESCRIPTION_TEXTAREA: Locator = (By.ID, "basic_description")

    TOAST_CONTAINER: Locator = (By.CSS_SELECTOR, "div.ant-message")
    TOAST_TEXT: Locator = (By.CSS_SELECTOR, "div.ant-message-custom-content span:last-child")

    FAILED_TO_POST: Locator = (By.CSS_SELECTOR, "div.ant-tooltip-inner")

    @allure.step("Upload logo: '{file_path}'")
    def upload_logo(self, file_path: str) -> DescriptionStep:
        """Upload a club logo (png, jpeg, jpg, svg)."""
        self._find_element(self.LOGO_UPLOAD_INPUT).send_keys(file_path)
        return self

    @allure.step("Upload cover: '{file_path}'")
    def upload_cover(self, file_path: str) -> DescriptionStep:
        """Upload a club cover / background image."""
        self._find_element(self.COVER_UPLOAD_INPUT).send_keys(file_path)
        return self

    @allure.step("Upload gallery photo: '{file_path}'")
    def upload_gallery_photo(self, file_path: str) -> DescriptionStep:
        """Add a photo to the gallery (picture-card upload)."""
        self._find_element(self.GALLERY_UPLOAD_INPUT).send_keys(file_path)
        return self

    @allure.step("Get uploaded images count")
    def get_uploaded_images_count(self) -> int:
        """Return the number of uploaded images."""
        return len(self.driver.find_elements(*self.VIEW_UPLOAD_IMG_BUTTON))

    @allure.step("Click first image preview button")
    def click_first_view_upload_image(self) -> None:
        """Click the first image preview button."""
        self._wait_clickable(self.VIEW_UPLOAD_IMG_BUTTON).click()

    @allure.step("Enter description: '{text}'")
    def enter_description(self, text: str) -> DescriptionStep:
        """Type the club description into the textarea."""
        el = self._find_element(self.DESCRIPTION_TEXTAREA)
        self._clear(el)
        el.send_keys(text)
        return self

    @allure.step("Clear description")
    def clear_description(self) -> DescriptionStep:
        """Clear the description textarea."""
        self._clear(self._find_element(self.DESCRIPTION_TEXTAREA))
        return self

    @allure.step("Check if toast message is displayed")
    def is_toast_displayed(self) -> bool:
        """Check whether the ant-message toast is visible."""
        try:
            return self._find_element(self.TOAST_CONTAINER).is_displayed()
        except Exception:
            return False

    @allure.step("Get toast message text")
    def get_toast_text(self) -> str:
        """Retrieve the text of the displayed toast notification."""
        return self._find_element(self.TOAST_TEXT).text.strip()

    @allure.step("Fill Step 3 — Опис")
    def fill(
        self,
        description: str | None = None,
        logo: str | None = None,
        cover: str | None = None,
        gallery: str | None = None,
    ) -> DescriptionStep:
        """Fill the description step. Only provided fields are touched."""
        if logo:
            self.upload_logo(logo)
        if cover:
            self.upload_cover(cover)
        if gallery:
            self.upload_gallery_photo(gallery)
        if description:
            self.enter_description(description)
        return self
