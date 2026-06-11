import requests

# Список городов
CITIES = {
    "1": {"name": "Москва", "lat": 55.7558, "lon": 37.6173},
    "2": {"name": "Пермь", "lat": 58.0105, "lon": 56.2502},
    "3": {"name": "Екатеринбург", "lat": 56.8389, "lon": 60.6057},
    "4": {"name": "Барселона", "lat": 41.3851, "lon": 2.1734},
    "5": {"name": "Лондон", "lat": 51.5074, "lon": -0.1278},
    "6": {"name": "Пекин", "lat": 39.9042, "lon": 116.4074},
}

def get_weather_description(code):
    codes = {
        0: "Ясно ☀️",
        1: "Преимущественно ясно 🌤️",
        2: "Переменная облачность ⛅",
        3: "Пасмурно ☁️",
        45: "Туман 🌫️",
        48: "Осаждающийся туман 🌫️",
        51: "Легкая морось 🌧️",
        53: "Умеренная морось 🌧️",
        55: "Плотная морось 🌧️",
        61: "Небольшой дождь 💧",
        63: "Умеренный дождь 🌧️",
        65: "Сильный дождь ⛈️",
        71: "Небольшой снегопад 🌨️",
        73: "Умеренный снегопад ❄️",
        75: "Сильный снегопад ☃️",
        77: "Снежная крупа 🌨️",
        80: "Слабый ливень 🌧️",
        81: "Умеренный ливень 🌧️",
        82: "Сильный ливень ⛈️",
        85: "Слабый снегопад с дождем 🌨️",
        86: "Сильный снегопад с дождем 🌨️",
        95: "Гроза ⚡",
    }
    return codes.get(code, "Переменчивая погода 🌤️🌧️")

def get_weather(city_name, lat, lon):
    # Запрашиваем температуру, влажность, ветер, код погоды, количество осадков (precipitation)
    # и вероятность осадков (precipitation_probability) за текущий час из почасового прогноза
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code,precipitation&hourly=precipitation_probability&wind_speed_unit=ms&timezone=auto&forecast_days=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Данные в реальном времени
        current = data["current"]
        temp = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]
        precipitation = current["precipitation"]  # Осадки в мм

        # Вытаскиваем вероятность осадков на текущий час из почасового массива
        # (Просто берем самый первый элемент, так как запросили прогноз всего на 1 день)
        prob_list = data["hourly"]["precipitation_probability"]
        precip_prob = prob_list[0] if prob_list else 0

        weather_code = current["weather_code"]
        weather_desc = get_weather_description(weather_code)

        print("\n" + "=" * 40)
        print(f"🌍 ПОГОДА В ГОРОДЕ: {city_name.upper()}")
        print("=" * 40)
        print(f"📋 На небе:          {weather_desc}")
        print(f"🌡️ Температура:     {temp}°C")
        print(f"🤔 Ощущается как:   {feels_like}°C")
        print(f"💧 Влажность:       {humidity}%")
        print(f"💨 Ветер:           {wind} м/с")
        print(f"🌧️ Осадки сейчас:   {precipitation} мм")
        print(f"🎲 Шанс осадков:    {precip_prob}%")
        print("=" * 40)

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Не удалось получить данные: {e}")

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
            print("\n⚠️ Неверный ввод. Выберите номер из списка.")

if __name__ == "__main__":
    main()