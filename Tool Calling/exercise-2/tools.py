def get_weather(town: str) -> str:
    
    weather_data = {
        "chennai": "32°C Sunny",
        "delhi": "28°C Clear",
        "mumbai": "30°C Rainy"
    }

    return weather_data.get(
        town.lower(),
        "Weather not available"
    )
    
    
def get_capital(state: str) -> str:
    
    capital_data = {
        "tamilnadu": "chennai",
        "andhrapradesh": "Hyderabad",
        "karnataka": "bangalire",
        "uttarpradesh":"lucknow"
    }

    return capital_data.get(
        state.lower(),
        "Capital not available"
    )    