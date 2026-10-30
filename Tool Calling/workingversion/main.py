from ollama import chat


def get_weather(town: str) :
    
    weather_data = {
        "chennai": "32°C Sunny",
        "delhi": "28°C Clear",
        "mumbai": "30°C Rainy"
    }


    return weather_data.get(
        town.lower(),
        "Weather not available"
    )
    
    
def get_capital(state: str) :
    print("input to get capital ", state)
    capital_data = {
        "tamilnadu": "chennai",
        "andhrapradesh": "Hyderabad",
        "karnataka": "bangalire",
        "uttarpradesh":"lucknow"
    }

    
    if state in capital_data :
        return capital_data[state]
    else  : 
        return "Capital not available"
  
def get_capital1(state: str) :
    print("input to get capital ", state)
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
      
tool_registry1 = {
    "get_weather": get_weather,
    "get_capital": get_capital
}

question = input("Ask: ")

messages = [
            {
               "role": "system",
               "content": """
            You are a helpful assistant.

            Use the provided tools when required.

            Answer ONLY based on the tool result.

            Do not mention other tools.
            Do not explain which tool was used.
            Do not mention weather questions unless the user asks about weather.
            Keep answers concise.
            """
        },
        {
            "role": "user",
            "content": question
        }
    ]

response = chat(
    model="qwen2.5:3b",
    messages=messages,
    tools=list(tool_registry1.values())
)

print("1. LLM Response" , response)


messages.append(response.message)
print("1. Tool calls " , response.message.tool_calls)

tool_call = response.message.tool_calls[0]
tool_name = tool_call.function.name
print("tool name is ", tool_name)
tool_function = tool_registry1[tool_name]
print("tool tool_function is ", tool_function)
tool_result = tool_function(**tool_call.function.arguments)



messages.append(
    {
        "role": "tool",
        "tool_name": tool_name,
        "content": tool_result
    }
)

final_response = chat(
    model="qwen2.5:3b",
    messages=messages
)

print(final_response.message.content)