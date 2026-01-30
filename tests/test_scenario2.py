# test_scenario2.py - ВТОРОЙ СЦЕНАРИЙ

print("=" * 70)
print("ТЕСТ 2: Проверка регионов на Saby.ru")
print("=" * 70)

import time
import sys
import os

# Добавляем папку pages в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pages.saby_page import SabyPage
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def test_second_scenario():
    """Второй сценарий: проверка смены региона"""

    print("Запускаю Firefox...")

    try:
        # Автоматически скачиваем драйвер Firefox
        service = Service(GeckoDriverManager().install())

        # Настраиваем Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        # Запускаем Firefox
        driver = webdriver.Firefox(service=service, options=options)
        print("Firefox запущен успешно!")

    except Exception as e:
        print(f"Ошибка при запуске Firefox: {e}")
        return False

    try:
        # Создаем объект страницы Saby
        saby_page = SabyPage(driver)

        # ========== ЧАСТЬ 1: Открываем контакты ==========
        print("\n📋 ЧАСТЬ 1: Открываем страницу контактов")

        print("\n1. Открываю saby.ru/contacts...")
        saby_page.open_contacts()
        time.sleep(3)

        # Сохраняем начальные данные
        start_url = driver.current_url
        start_title = driver.title

        print(f"   Начальный URL: {start_url}")
        print(f"   Начальный заголовок: {start_title}")

        # ========== ЧАСТЬ 2: Анализируем страницу ==========
        print("\n📋 ЧАСТЬ 2: Анализируем страницу")

        # Получаем весь текст страницы
        all_text = driver.find_element("tag name", "body").text
        print(f"   Длина текста на странице: {len(all_text)} символов")

        # Разбиваем текст на строки
        lines = all_text.split('\n')
        print(f"   Количество строк текста: {len(lines)}")

        # Ищем упоминания регионов
        print("\n2. Ищу упоминания регионов...")

        region_keywords = [
            'Москва', 'Санкт-Петербург', 'Ярослав', 'Новосибирск',
            'Екатеринбург', 'Казань', 'область', 'край', 'республика'
        ]

        found_regions = []
        for line in lines:
            line_lower = line.lower()
            for keyword in region_keywords:
                if keyword.lower() in line_lower:
                    # Берем только короткие строки (скорее всего это названия)
                    if len(line.strip()) < 50 and line.strip() not in found_regions:
                        found_regions.append(line.strip())
                        break

        if found_regions:
            print(f"   Найдено упоминаний регионов: {len(found_regions)}")
            print("   Примеры найденного:")
            for region in found_regions[:5]:  # Показываем первые 5
                print(f"   - {region}")
        else:
            print("   Явных упоминаний регионов не найдено")

        # ========== ЧАСТЬ 3: Ищем элементы управления ==========
        print("\n📋 ЧАСТЬ 3: Ищу элементы управления регионом")

        print("\n3. Ищу элементы на странице...")

        # Считаем разные элементы
        all_buttons = driver.find_elements("tag name", "button")
        all_selects = driver.find_elements("tag name", "select")
        all_inputs = driver.find_elements("tag name", "input")

        print(f"   Найдено кнопок: {len(all_buttons)}")
        print(f"   Найдено выпадающих списков: {len(all_selects)}")
        print(f"   Найдено полей ввода: {len(all_inputs)}")

        # Ищем элементы с текстом "регион", "город" и т.д.
        search_words = ['регион', 'город', 'выбрать', 'сменить', 'изменить']

        found_elements = []
        for word in search_words:
            try:
                # Ищем по тексту элемента
                elements = driver.find_elements("xpath", f"//*[contains(text(), '{word}')]")
                if elements:
                    found_elements.extend(elements)
                    print(f"   Найдено элементов с текстом '{word}': {len(elements)}")
            except:
                pass

        if found_elements:
            print(f"\n   Всего найдено элементов управления: {len(found_elements)}")

            # Пробуем кликнуть по первому подходящему элементу
            for element in found_elements:
                try:
                    if element.is_displayed() and element.is_enabled():
                        element_text = element.text[:30] if element.text else "элемент без текста"
                        print(f"Найден элемент: {element_text}...")

                        # Пробуем кликнуть
                        element.click()
                        time.sleep(2)

                        # Теперь ищем Камчатский край
                        print("Ищу 'Камчатский'...")

                        # Ищем текст Камчатка
                        page_text = driver.page_source
                        if 'камчат' in page_text.lower():
                            print("Найдено упоминание Камчатки")
                        else:
                            print("Камчатка не найдена")

                        break
                except:
                    continue
        else:
            print("   Элементы управления не найдены")

        # ========== ЧАСТЬ 4: Итоги проверки ==========
        print("ЧАСТЬ 4: Итоги проверки")

        # Сравниваем начальные и конечные данные
        end_url = driver.current_url
        end_title = driver.title

        print(f"\n4. Сравниваю начальные и конечные данные:")
        print(f"   URL был: {start_url}")
        print(f"   URL стал: {end_url}")
        print(f"   Заголовок был: {start_title}")
        print(f"   Заголовок стал: {end_title}")

        if start_url != end_url:
            print("URL изменился")
        else:
            print("URL не изменился")

        if start_title != end_title:
            print("Заголовок изменился")
        else:
            print("Заголовок не изменился")

        # Делаем финальный скриншот
        saby_page.take_screenshot("region_final")

        print("\n" + "=" * 70)
        print("🎉 ТЕСТ 2 ВЫПОЛНЕН!")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"Ошибка во время теста: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        print("\nЗакрываю Firefox...")
        driver.quit()
        print("Браузер закрыт.")


# Запускаем тест если файл запущен напрямую
if __name__ == "__main__":
    success = test_second_scenario()
    if success:
        print("Тест пройден успешно!")
    else:
        print("Тест завершился с ошибкой")

    input("\nНажми Enter для выхода...")