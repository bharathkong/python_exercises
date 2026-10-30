from ollama import chat
from tools import *

tool_registry ={
"get_capital":"get_capital",
"get_weather":"get_weather"
}
query = input("Enter your query : ")
messages =[
			{
			"role":"system"
			"content": """
			You are a Assistant.
			You should use the below tools to answer any question
			Tools: get_weather, get_capital.
			Do not generate your answer without using the tools
			If you dont have answer, respond stating I am sorry I cannot help you now. 
			"""
			},
			{
			"role":"user",
			"content":query
			}
			]
			
			
response= chat(
			model="qwen2.5:3b",
			messages= messages,
			tools= list(tool_registry.values())
			 )			

tool_call = response.message.tool_calls[0]
tool_name= tool_call.function.name
tool_function= tool_registry.get(tool_name)

tool_Result= tool_function(**tool_call.function.arguments)

messages.append(
    {
        "role": "tool",
        "tool_name": tool_name,
        "content": tool_result
    }
)



response= chat(
			model="qwen2.5:3b",
			messages= messages,
			 )
             

answer = response.message.content
print( answer)
