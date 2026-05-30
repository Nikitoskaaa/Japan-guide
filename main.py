import requests
import re
import random
import time
import json
from bs4 import BeautifulSoup

abzaces = {}
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Nikitoskaaa/Japan-facts/refs/heads/main/japan_facts.txt"

def get_random_fact_from_github():
    try:
        response = requests.get(GITHUB_RAW_URL,timeout=10)
        response.raise_for_status()
        facts = response.text.strip().split("\n")
        facts = [fact.strip() for fact in facts if fact.strip()]
        fact = random.choice(facts)
        print(f"\n🌸 Случайный факт о Японии: {fact}\n")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}. Проверьте интернет или ссылку.")


def download_wiki_page(city):
    url = f"https://ru.wikipedia.org/wiki/{city}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        filename = f"{city}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Страница сохранена в {filename}, ссылка на википедию -'https://ru.wikipedia.org/wiki/{city}'-")
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Ошибка загрузки {city}: {e}")
        return False


def extract_first_paragraph(city):
    global abzaces
    filename = f"{city}.html"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        all_p = soup.find_all('p')
        for p in all_p:
            text = p.get_text().strip()
            if len(text) > 100 and not text.startswith('Для улучшения'):
                text = re.sub(r'\[\d+\]', '', text)
                text = re.sub(r'\s+', ' ', text)
                abzaces[city] = text
                # Сохраняем в JSON
                with open("абзацы.json", "w", encoding="utf-8") as f:
                    json.dump(abzaces, f, ensure_ascii=False, indent=2)
                print(f"\n Первый абзац про {city}:\n{text}\n Ссылка на википедию -'https://ru.wikipedia.org/wiki/{city}'-")
                return
        print(f" Не найден подходящий абзац для {city}")
    except FileNotFoundError:
        print(f" Файл {filename} не найден. Сначала скачай страницу.")
    except Exception as e:
        print(f" Ошибка парсинга: {e}")


def searchinjsonabzac(city):
    global abzaces
    file = "абзацы.json"
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                abzaces = json.loads(content)
            else:
                abzaces = {}
    except (FileNotFoundError, json.JSONDecodeError):
        abzaces = {}

    if city in abzaces:
        print(f"🌸 {abzaces[city]} ссылка на википедию -'https://ru.wikipedia.org/wiki/{city}'-")
    else:
        print("Город не найден в сохранённых, приступаю к скачиванию...")
        if download_wiki_page(city):
            extract_first_paragraph(city)
        else:
            print(f"Не удалось скачать страницу. Ссылка на википедию -'https://ru.wikipedia.org/wiki/{city}'-")


def get_temperature(city):
    try:
        print("парсим...")
        link = f"https://wttr.in/{city}?format=%t&lang=ru"
        x = requests.get(link).text
        if "location not found" in x.lower() or not x:
            print(f"Ненашлось города |-> {city} <-| попробуйте скопировать название города и вставить")
            return
        x = x.replace("°C", "")
        x = x.replace("Â", "")
        print(f"В городе {city} {x} градусов 🌡️")
    except(requests.exceptions.RequestException) as e:
        print(f"Не удалось узнать погоду в {city} ошибка: '{e}'")


def get_daily_quote():
    print("парсим...")
    try:
        url = "https://meowfacts.herokuapp.com/?lang=rus"
        response = requests.get(url)
        data = response.json()
        fact = data["data"][0]
        print(f"Факт про кошек: {fact}")
    except Exception as e:
        print(f"Не удалось получить факт о кошках: {e}")


def exit_program():
    print("До свидания! Спасибо, что пользуешься гидом.")
    exit(0)


menu = {
    "1": get_random_fact_from_github,
    "2": lambda: searchinjsonabzac(input("Введите название города или места (например, Токио, Осака, Киото, Гора Фудзи): ")),
    "3": get_daily_quote,
    "4": lambda: get_temperature(input("Введите название города (например, Токио, Осака, Киото): ")),
    "0": exit_program
}

def main():
    while True:
        print("\n" + "🌸"*10)
        print("    ГИД ПО ЯПОНИИ ")
        print("🌸"*10)
        print("""
1 - Случайный факт о Японии⛩️
2 - Узнать о городе/месте (скачать + показать абзац)🔍
3 - Случайный факт про кошек🐱
4 - Погода в городе🌦️
0 - Выход💔""")
        choice = input("Твой выбор: ")
        if choice in menu:
            menu[choice]()   # вызываем выбранную функцию
        else:
            print("Некорректный ввод, попробуй ещё раз.")

if __name__ == "__main__":
    main()