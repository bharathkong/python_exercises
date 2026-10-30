from langgraph import *
from agents import *

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