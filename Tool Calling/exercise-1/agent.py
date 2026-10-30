from ollama import chat
from kbk import get_weather

question = input("Enter the city to know the weather : ")

prompt = f"""
You are an AI agent.

Available Tool:
get_weather(city)

If the user asks about weather,
respond EXACTLY as:

TOOL:get_weather:<city>

Otherwise answer normally.

User Question:
{question}
"""

response = chat(
    model='qwen2.5:3b',
    messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ]
)

answer = response['message']['content']

print("pringitn full answer")
print(response)
print("\nLLM Response:")
print(answer)

if answer.startswith("TOOL:get_weather:"):

    city = answer.replace(
        "TOOL:get_weather:",
        ""
    ).strip()

    result = get_weather(city)

    print("\nTool Result:")
    print(result)

    final_response = f"""
Weather in {city} is {result}
"""

    print("\nFinal Agent Response:")
    print(final_response)