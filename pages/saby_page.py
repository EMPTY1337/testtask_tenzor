# saby_page.py - страница Saby.ru

from selenium.webdriver.common.by import By
from .base_page import BasePage
import time


class SabyPage(BasePage):
    """Класс для работы со страницей Saby.ru"""

    # Кнопка "Контакты" в меню
    CONTACTS_LINK = (By.XPATH, "//a[contains(@href, 'contacts')]")

    # Текст на странице контактов
    PAGE_TITLE = (By.TAG_NAME, "h1")

    # Все изображения на странице
    ALL_IMAGES = (By.TAG_NAME, "img")

    # Все ссылки на странице
    ALL_LINKS = (By.TAG_NAME, "a")

    def open_contacts(self):
        """Открыть страницу контактов"""
        self.open("https://saby.ru/contacts")
        self.take_screenshot("saby_contacts")

    def search_tensor_banner(self):
        """Найти баннер Тензор"""
        print("Ищу баннер Тензор...")

        # Ищем все ссылки на странице
        links = self.find_elements(self.ALL_LINKS)
        print(f"Найдено ссылок: {len(links)}")

        # Ищем ссылку на tensor.ru
        for link in links:
            href = link.get_attribute("href")
            if href and "tensor.ru" in href:
                print(f"Найдена ссылка на Tensor: {href}")
                return link

        print("Ссылка на Tensor не найдена")
        return None

    def get_page_info(self):
        """Получить информацию о странице"""
        info = {
            "url": self.driver.current_url,
            "title": self.driver.title,
            "text_length": len(self.driver.page_source)
        }
        return info