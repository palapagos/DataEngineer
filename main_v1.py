import requests
import os
import csv
from datetime import datetime
import schedule
import time

# Ваш API-ключ
API_KEY = 'af77d74f80fbe6595693efb6b129d825'

# URL для запиту
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Міста для перевірки погоди
cities = ["Kyiv", "Lviv", "Odessa", "Kharkiv"]

# Функція для отримання даних погоди
def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Щоб отримати дані в градусах Цельсія
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        print(f"Помилка отримання даних для міста {city}: {response.status_code}")
        return None

# Збір даних для всіх міст
weather_data = []
for city in cities:
    weather = get_weather(city)
    if weather:
        weather_data.append(weather)

# Збереження в CSV з перезаписом файлу
#csv_file = "weather_data.csv"
#with open(csv_file, mode="w", newline="", encoding="utf-8") as file:      #перезаписує файл
#    writer = csv.DictWriter(file, fieldnames=["city", "temperature", "humidity", "description", "datetime"])
#    writer.writeheader()
#    writer.writerows(weather_data)


# Збереження в CSV з накопиченням данних
csv_file = "weather_data.csv"
# Перевірка, чи файл вже існує
file_exists = os.path.isfile(csv_file)
with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["city", "temperature", "humidity", "description", "datetime"])
    # Якщо файл новий, пишемо заголовок
    if not file_exists:
        writer.writeheader()
    # Записуємо нові рядки
    writer.writerows(weather_data)

print(f"Дані про погоду збережено у файл {csv_file}.")

