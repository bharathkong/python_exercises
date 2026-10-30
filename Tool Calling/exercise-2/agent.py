from ollama import chat
#from tools import get_weather
#from tools import get_capital
from tools import *

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