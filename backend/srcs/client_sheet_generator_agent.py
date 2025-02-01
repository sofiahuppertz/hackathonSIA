import os
import asyncio
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import ToolMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing import List
from typing_extensions import TypedDict
from .web_search import section_builder_graph
from .prompts import presentation_generale_prompt, projets_verts_prompt

load_dotenv()

llm = ChatNVIDIA(
    model="nv-mistralai/mistral-nemo-12b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"),
)


class Section(BaseModel):
    content:str = Field(
        description="The content of the section."
    )
    
class SectionOutputState(TypedDict):
    images: list[str]
    web_sources: list[str]
    completed_section: str

# Graph state
class State(TypedDict):
    collectivite: str
    presentation_generale: SectionOutputState
    projets_verts: SectionOutputState
    images: List[str]
    web_sources: List[str]
    fiche_client: str

class SearchQuery(BaseModel):
    search_query: str = Field(
        None, description="Query for web search."
    )
    
async def presentation_generale(state: State): 
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Statistiques officielles de {collectivite} : population de la Métropole, superficie et densité de population en 2024"},
        {"search_query": f"Événements clés et réformes de {collectivite} pendant les 30 dernières années"},
        {"search_query": f"Événements clés et réformes de {collectivite} pendant les 60 dernières années"},
        {"search_query": f"Compétences et missions principales de {collectivite} : responsabilités, attributions et organisation administrative."},
        {"search_query": f"Secteurs économiques dominants de {collectivite}"},
        {"search_query": f"Patrimoine culturel de {collectivite}"},
    ]
    section_data = {
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    prompt = presentation_generale_prompt.format(collectivite=collectivite)
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "writer_prompt": prompt,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "images": [],
        "web_sources": [],
        "completed_sections": [],
    }
    result = await section_builder_graph.ainvoke(initial_state)
    # print(f"DEBUG: presentation_generale result: {result}")
    return { "presentation_generale": result }

async def projets_verts(state: State):
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"{collectivite} transition écologique site officiel projets environnementaux 2024 budget écologie 2024 filetype:pdf politiques publiques environnement programme développement durable"},
        {"search_query": f"{collectivite} énergies renouvelables projets panneaux solaires installations politique énergétique municipale transition énergétique budget solaire photovoltaïque ville"},
        {"search_query": f"{collectivite} transports propres mobilité durable infrastructures cyclables 2024 pistes cyclables projet filetype:pdf plan mobilité durable véhicules électriques municipaux"},
        {"search_query": f"{collectivite} assainissement projets gestion des eaux pluviales réduction rejets eaux usées bassins d’orages investissement pollution eaux plan d’action"},
        {"search_query": f"{collectivite} rénovation énergétique écoles bâtiments publics plan efficacité énergétique 2024 réduction consommation énergétique transition énergétique bâtiments municipaux budget municipal écologie 2024 filetype:pdf rapport développement durable filetype:pdf plan climat énergie territorial rapport investissement écologique dossier subventions écologiques"}
    ]

    section_data = {
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    prompt = projets_verts_prompt.format(collectivite=collectivite)
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "writer_prompt": prompt,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "images": [],
        "web_sources": [],
        "completed_sections": [],
    }
    result = await section_builder_graph.ainvoke(initial_state)
    return { "projets_verts": result }

def aggregator(state: State):
    combined = f"Fiche Client pour {state['collectivite']}:\n\n"
    combined += "1. Présentation Générale:\n" + state["presentation_generale"]["completed_sections"] + "\n\n"
    combined += "5. Projets Verts:\n" + state["projets_verts"]["completed_sections"] + "\n\n"
    
    all_images = list(state.get("images", []))
    all_web_sources = list(state.get("web_sources", []))
    
    for section in [state["presentation_generale"], state["projets_verts"]]:
        all_images.extend(section.get("images", []))
        all_web_sources.extend(section.get("web_sources", []))
    
    return {
        "fiche_client": combined,
        "images": all_images,
        "web_sources": all_web_sources,
    }
    
# Build workflow
parallel_builder = StateGraph(State)

# Define a list of tuples with node names and their corresponding functions
sections = [
    ("call_section_1", presentation_generale),
    # ("call_section_2", interlocuteurs),
    # ("call_section_3", budget_primitif_2024),
    # ("call_section_4", situation_financiere),
    ("call_section_5", projets_verts),
    # ("call_section_6", projets_sociaux),
    # ("call_section_7", comparatif_collectivites),
]

# Loop to add nodes and connect them from START and to aggregator
for name, func in sections:
    parallel_builder.add_node(name, func)
    parallel_builder.add_edge(START, name)
    parallel_builder.add_edge(name, "aggregator")

# Add the aggregator node and connect it to END
parallel_builder.add_node("aggregator", aggregator)
parallel_builder.add_edge("aggregator", END)

# Compile the workflow
parallel_workflow = parallel_builder.compile()

# Invoke
async def run_workflow(collectivite: str ) -> State:
    state = await parallel_workflow.ainvoke({"collectivite": collectivite})
    return state

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_workflow("Nice"))

