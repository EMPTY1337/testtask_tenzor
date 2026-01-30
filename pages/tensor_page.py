# tensor_page.py - страница Tensor.ru

from selenium.webdriver.common.by import By
from .base_page import BasePage
import time


class TensorPage(BasePage):
    """Класс для работы со страницей Tensor.ru"""

    # Элементы на главной странице
    POWER_BLOCK = (By.XPATH, "//*[contains(text(), 'Сила в людях')]")

    # Ссылка "Подробнее"
    DETAILS_LINK = (By.XPATH, "//a[contains(text(), 'Подробнее')]")

    # Изображения в разделе "Работаем"
    WORKING_IMAGES = (By.XPATH, "//img[contains(@class, 'work') or contains(@alt, 'work')]")

    def check_power_in_people(self):
        """Проверить наличие блока 'Сила в людях'"""
        print("Проверяю блок 'Сила в людях'...")
        try:
            element = self.find_element(self.POWER_BLOCK)
            if element:
                print("Блок 'Сила в людях' найден")
                return True
        except:
            print("Блок 'Сила в людях' не найден")
            return False

    def go_to_about_page(self):
        """Перейти на страницу 'О нас'"""
        print("Перехожу на страницу 'О нас'...")
        self.open("https://tensor.ru/about")
        self.take_screenshot("tensor_about")

        if "about" in self.driver.current_url:
            print(" Страница 'О нас' открыта")
            return True
        else:
            print("Не удалось открыть страницу 'О нас'")
            return False

    def check_images_size(self):
        """Проверить размеры изображений"""
        print("Проверяю размеры изображений...")

        # Ищем все изображения
        images = self.find_elements((By.TAG_NAME, "img"))
        print(f"Найдено изображений: {len(images)}")

        if len(images) < 2:
            print("Недостаточно изображений для проверки")
            return False

        # Берем первые 3 изображения
        sizes = []
        for i in range(min(3, len(images))):
            try:
                img = images[i]
                width = img.size['width']
                height = img.size['height']
                sizes.append((width, height))
                print(f"  Изображение {i + 1}: {width}x{height}")
            except:
                print(f"  Не удалось получить размер изображения {i + 1}")

        # Проверяем одинаковы ли размеры
        if len(sizes) >= 2:
            first_size = sizes[0]
            all_same = all(size == first_size for size in sizes[1:])

            if all_same:
                print(f"Все изображения одинакового размера: {first_size[0]}x{first_size[1]}")
                return True
            else:
                print("Изображения разного размера")
                return False
        else:
            print("Недостаточно изображений для сравнения")
            return False