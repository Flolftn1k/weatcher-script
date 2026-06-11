import requests

# Словарь со списком городов, их координатами и русскими названиями
CITIES = {
    "1": {"name": "Москва", "lat": 55.7558, "lon": 37.6173},
    "2": {"name": "Пермь", "lat": 58.0105, "lon": 56.2502},
    "3": {"name": "Екатеринбург", "lat": 56.8389, "lon": 60.6057},
    "4": {"name": "Барселона", "lat": 41.3851, "lon": 2.1734},
    "5": {"name": "Лондон", "lat": 51.5074, "lon": -0.1278},
    "6": {"name": "Пекин", "lat": 39.9042, "lon": 116.4074},
}

def get_weather(city_name, lat, lon):
    # Добавили параметр timezone=auto, чтобы API учитывало локальное время города
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m&wind_speed_unit=ms&timezone=auto"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        temp = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]

        print("\n" + "=" * 35)
        print(f"🌍 ПОГОДА В ГОРДE: {city_name.upper()}")
        print("=" * 35)
        print(f"🌡️ Температура: {temp}°C")
        print(f"🤔 Ощущается как: {feels_like}°C")
        print(f"💧 Влажность: {humidity}%")
        print(f"💨 Скорость ветра: {wind} м/с")
        print("=" * 35)
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Не удалось получить данные для города {city_name}: {e}")

def main():
    while True:
        print("\n=== ВЫБЕРИТЕ ГОРОД ===")
        for key, city_info in CITIES.items():
            print(f"{key}. {city_info['name']}")
        print("0. Выход из программы")

        choice = input("\nВведите номер города: ").strip()

        if choice == "0":
            print("\nДо встречи! Хорошей погоды! ☀️")
            break
        elif choice in CITIES:
            city = CITIES[choice]
            get_weather(city["name"], city["lat"], city["lon"])
        else:
            print("\n⚠️ Неверный ввод. Пожалуйста, выберите номер из списка.")

if __name__ == "__main__":
    main()