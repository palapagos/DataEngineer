import schedule
import time
import requests
import os
import csv
from datetime import datetime

API_KEY = 'af77d74f80fbe6595693efb6b129d825'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
cities = ["Kyiv", "Lviv", "Odessa", "Kharkiv"]
csv_file = "weather_data.csv"

def fetch_weather():
    weather_data = []
    for city in cities:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_data.append({
                "city": city,
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    # Збереження в CSV
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["city", "temperature", "humidity", "description", "datetime"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(weather_data)
    print(f"Дані успішно додано в {csv_file}")

# Запланувати виконання функції кожну хвилину
schedule.every(1).minutes.do(fetch_weather)
start_time = time.time()
max_duration = 300  # Максимальна тривалість роботи (в секундах)
# Головний цикл
while True:
    schedule.run_pending()
    time.sleep(1)
    if time.time() - start_time > max_duration:  # Перевірка часу
        print(f"Виконання завершено після {max_duration} секунд.")
        break