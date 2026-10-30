def get_weather(city):
    weather_data ={
        "chennai":"100",
        "delhi":"200",
        "bombay":"300"
    }

    city= city.lower()
    if city in weather_data:
        return weather_data[city]
    else :
        return "data not available. Pls try later"
	