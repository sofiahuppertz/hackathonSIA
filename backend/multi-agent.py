import json
import os
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from tavily.search import TavilySearchResults

# Load the environment variables
load_dotenv()

# Class definitions
class State(TypedDict):
    messages: Annotated[list, add_messages]

#  Instance creations
graph_builder = StateGraph(State)

llm = ChatNVIDIA(
    model="nv-mistralai/mistral-nemo-12b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"),
)

#  Node defintions
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

tool = TavilySearchResults(max_results=2)
tools = [tool]
tool.invoke("What's a 'node' in LangGraph?")

# Graph architecture
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()
print(graph)

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)       
            
while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break



