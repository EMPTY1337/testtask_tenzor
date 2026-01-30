
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Ждем элементы до 10 секунд

    def open(self, url):
        """Открыть страницу по URL"""
        print(f"Открываю: {url}")
        self.driver.get(url)
        time.sleep(2)  # Ждем 2 секунды чтобы страница загрузилась

    def find_element(self, locator):
        """Найти один элемент на странице"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Найти все элементы на странице"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Кликнуть по элементу"""
        element = self.find_element(locator)
        element.click()
        print(f"Кликнул по элементу")

    def get_text(self, locator):
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text

    def take_screenshot(self, name):
        """Сделать скриншот"""
        # Создаем папку для скриншотов если ее нет
        import os
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        # Сохраняем скриншот
        filename = f"screenshots/{name}.png"
        self.driver.save_screenshot(filename)
        print(f"Скриншот сохранен: {filename}")
        return filename