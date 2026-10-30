from langgraph import *
from langgraph.graph import END
from typing import TypedDict
from ollama import chat
from langgraph.graph import StateGraph
from openai import OpenAI

class SDLCState(TypedDict):
    requirements:str
    analysis:str
    design:str
    code:str
    testcases:str

def llm_call(prompt):
    #print(" LLM Call Started ")
    llm_output = chat(
        model="qwen2.5:3b",
                 messages = [
                     {
                        "role":"user",
                        "content":prompt
                     }
                 ]
    )
    #print(" LLM Call Ended")
    
    return llm_output.message.content



client = OpenAI(
    api_key="your-api-key"
)

def llm_call_openai(prompt):


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
    
def analysis_agent(state):
    prompt = f"""
    Requirements {state['requirements']}
    You are a analysis agent. You will read the requirements and generated analysis documentation not more than 10 lines.
    Generate only content relevant to the requirements.
    """
    #print(" calling analysis agent ", prompt)
    output = llm_call(prompt)
    print(" Analysis Done ")
    return {
        "analysis":output
    }
        
def design_agent(state):
    prompt = f"""
    Requirements details are provided below:
    {state['requirements']}
    Analysis details are provided below:
    {state['analysis']}
    You are a design agent. You will read the requirements and analysis documentation and generat high level designdocumentation not more than 10 lines.
    Generate only content relevant to the design.
    """
    #print(" calling design agent ", prompt)
    output = llm_call(prompt)
    print(" DESIGN Done ")
    return {
        "design":output
    }
    
# user_input = input("Enter the requirements:-->  ")
user_input ="generate application that accepts a paragraph and returns  only first 10 words "

graph = StateGraph(SDLCState)

graph.add_node("analysis",analysis_agent)
graph.add_node("design",design_agent)

graph.add_edge("analysis", "design")
graph.add_edge("design", END)
graph.set_entry_point("analysis")
app= graph.compile()

#print(" Starting GGenereration ", user_input)
print(" Process Started ")
final_output = app.invoke(
    {
        "requirements":user_input
    }
)

print("* *************** Final ouput  ****************")
print ("Analysis ", final_output['analysis'])
print ("Design ", final_output['design'])
    


