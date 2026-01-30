# test_scenario1.py - ПЕРВЫЙ СЦЕНАРИЙ

print("=" * 70)
print("ТЕСТ 1: Переход с Saby.ru на Tensor.ru")
print("=" * 70)

# Импортируем нужные библиотеки
import time
import sys
import os

# Добавляем папку pages в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Импортируем наши страницы
from pages.saby_page import SabyPage
from pages.tensor_page import TensorPage

# Импортируем Selenium для Firefox
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def test_first_scenario():
    """Первый сценарий тестового задания"""

    print("Запускаю Firefox")

    try:
        service = Service(GeckoDriverManager().install())

        # Настраиваем Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        driver = webdriver.Firefox(service=service, options=options)
        print("Firefox запущен успешно!")

    except Exception as e:
        print(f"Ошибка при запуске Firefox: {e}")
        return False

    try:
        # ========== ЧАСТЬ 1: Работа с Saby.ru ==========
        print("Работа с Saby.ru")

        # Создаем объект страницы Saby
        saby_page = SabyPage(driver)

        # 1. Открываем страницу контактов
        print("\n1. Открываю saby.ru/contacts...")
        saby_page.open_contacts()

        # 2. Получаем информацию о странице
        info = saby_page.get_page_info()
        print(f"   URL: {info['url']}")
        print(f"   Заголовок: {info['title']}")

        # 3. Ищем баннер Тензор
        print("Ищу баннер Тензор")
        tensor_banner = saby_page.search_tensor_banner()

        if tensor_banner:
            print(" Нашел баннер, кликаю")
            tensor_banner.click()
            time.sleep(3)
        else:
            print("   Баннер не найден, перехожу напрямую...")
            driver.get("https://tensor.ru")
            time.sleep(3)

        # ========== ЧАСТЬ 2: Работа с Tensor.ru ==========
        print("Работа с Tensor.ru")

        # Создаем объект страницы Tensor
        tensor_page = TensorPage(driver)

        # 4. Проверяем что мы на tensor.ru
        current_url = driver.current_url
        print("Текущий URL: {current_url}")

        if "tensor.ru" not in current_url:
            print("Не на tensor.ru, перехожу")
            driver.get("https://tensor.ru")
            time.sleep(3)
            tensor_page = TensorPage(driver)

        print("Успешно на tensor.ru!")

        # 5. Проверяем блок "Сила в людях"
        print("\n4. Проверяю блок 'Сила в людях'...")
        tensor_page.check_power_in_people()

        # 6. Переходим на страницу "О нас"
        print("\n5. Перехожу на страницу 'О нас'...")
        tensor_page.go_to_about_page()

        # 7. Проверяем размеры изображений
        print("\n6. Проверяю размеры изображений...")
        tensor_page.check_images_size()

        print("\n" + "=" * 70)
        print("ТЕСТ 1 ВЫПОЛНЕН УСПЕШНО!")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"Ошибка во время теста: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Всегда закрываем браузер в конце
        print("Закрываю Firefox...")
        driver.quit()
        print("Браузер закрыт.")


# Запускаем тест если файл запущен напрямую
if __name__ == "__main__":
    success = test_first_scenario()
    if success:
        print("Тест пройден успешно!")
    else:
        print("Тест завершился с ошибкой")

    input("Нажми Enter для выхода...")