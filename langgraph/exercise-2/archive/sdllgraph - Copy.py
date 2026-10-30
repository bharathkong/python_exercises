from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from ollama import chat


MODEL = "qwen2.5:3b"

print("Start")

class SDLCState(TypedDict):
    requirement: str
    analysis: str
    design: str
    code: str
    tests: str


def call_llm(prompt):

    print("Calling LLM ", prompt)
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print("LLM Call Success ", response.message.content)
    return response.message.content


# --------------------
# Analysis Agent
# --------------------

def analysis_agent(state):
    print("Calling LLM ", state)
    prompt = f"""
Requirement:

{state['requirement']}

Create only 10 lines of analysis.
"""

    result = call_llm(prompt)

    print("\n=== ANALYSIS ===")
    print(result)

    return {
        "analysis": result
    }


# --------------------
# Design Agent
# --------------------

def design_agent(state):
    print("Calling LLM ", state)
    prompt = f"""
Requirement:
{state['requirement']}

Analysis:
{state['analysis']}

Create only 10 lines of design.
"""

    result = call_llm(prompt)

    print("\n=== DESIGN ===")
    print(result)

    return {
        "design": result
    }


# --------------------
# Code Agent
# --------------------

def code_agent(state):
    print("Calling LLM ", state)
    prompt = f"""
    Requirement:
    {state['requirement']}

    Design:
    {state['design']}

    Generate only 10 lines of sample code.
    """
    result = call_llm(prompt)
    print("\n=== CODE ===")
    print(result)

    return {
           "code": result
    }


# --------------------
# Test Agent
# --------------------

def test_agent(state):
    print("Calling LLM ", state)
    prompt = f"""
    Requirement:
    {state['requirement']}

    Code:
    {state['code']}

    Generate only 10 lines of test cases.
    """

    result = call_llm(prompt)
    print("\n=== TESTS ===")
    print(result)

    return {
          "tests": result
    }


graph = StateGraph(SDLCState)

graph.add_node("analysis", analysis_agent)
graph.add_node("design", design_agent)
graph.add_node("code", code_agent)
graph.add_node("tests", test_agent)

graph.set_entry_point("analysis")

graph.add_edge("analysis", "design")
graph.add_edge("design", "code")
graph.add_edge("code", "tests")
graph.add_edge("tests", END)

app = graph.compile()


requirement = input(
    "Enter requirement: "
)

result = app.invoke(
    {
        "requirement": requirement
    }
)

print("\n\nWORKFLOW COMPLETED")
