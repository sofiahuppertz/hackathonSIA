# In visualization.py
from langgraph.graph import get_graph_dict
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from client_sheet_generator_agent import parallel_workflow
from web_search import section_builder_graph

router = APIRouter()



@router.get("/visualize/{graph_name}", response_class=HTMLResponse)
async def visualize_graph(graph_name: str):
    if graph_name == "client_sheet":
        graph = parallel_workflow
    elif graph_name == "web_search":
        graph = section_builder_graph
    else:
        return "Graph not found"
    
    graph_dict = get_graph_dict(graph)
    return f"""
    <html>
        <body>
            <pre>{graph_dict}</pre>
            <img src="/visualize/{graph_name}/graph.png">
        </body>
    </html>
    """
