def main2():
    cityname = input("Enter city name: ")
    print("city is ", cityname)
    get_weather(cityname)
    
    
def get_weather(city):
    print("Calling getwesather")
    weather_data ={
        "chennai":"100",
        "delhi":"200",
        "bombay":"300"
    }

    city= city.lower()
    print("city is", city)
    
    if city in weather_data:
        print(weather_data[city])
    else :
        print("data not available")
	


if __name__ == "__main__":
    main1()