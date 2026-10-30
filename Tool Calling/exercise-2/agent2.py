from tools import * 
from ollama import chat

prompt= input("Enter the question ")
modelname="qwen2.5:3b"
tool_registry={
    "get_weather":get_weather,
    "get_capital":get_capital
}

system_prompt ="""
 You are a helpful assistant.

            Use the provided tools when required.

            Answer ONLY based on the tool result.

            Do not mention other tools.
            Do not explain which tool was used.
            Do not mention weather questions unless the user asks about weather.
            Keep answers concise.
"""
messages=[
    {
        "role":"system",
        "content":system_prompt
    },{
        "role":"user",
        "content":prompt
    }
]


response = chat(
            model=modelname,
            messages=messages,
            tools=list(tool_registry.values())

)

print(response)

tool_call = response.message.tool_calls[0]
print("tool_call " , tool_call)
tool_name= tool_call.function.name
print("tool_name " , tool_name)
tool_function= tool_registry[tool_name]
print("tool_function ", tool_function)

tool_output = tool_function(**tool_call.function.arguments)
print(tool_output)

messages.append(
    {
    "role": "tool",
        "content" : tool_output,
        "tool_name": tool_name    
    }
)

final_answer = chat(
    model=modelname,
    messages=messages
)

print (" *******************")
print (" Final Answer below")
print(final_answer.message.content)