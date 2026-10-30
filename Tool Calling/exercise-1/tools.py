def get_weather(city):
    weather_data = {
        "chennai": "32°C Sunny",
        "bangalore": "25°C Cloudy",
        "mumbai": "30°C Rainy"
    }
    city = city.lower()
    if city in weather_data:
        return weather_data[city]
    else:
        return "Weather not available"
