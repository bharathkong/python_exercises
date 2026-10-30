def get_weather(city:str)->str:
    print("calling")
    """



    """
    weather_data={
    "chennai":"10",
    "hyderabad":"20",
    "bngl":"30",
    "kerala":"40"

    }
    city=city.lower().strip()
    print("city is ",city)
    if city in weather_data:
        weather =weather_data[city]
        print(f"Weather for {city} is {weather}")
    else:
        print(f"Weather not available for the city {city}")

citystring = "chennai"
get_weather(citystring)
