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
from web_search import section_builder_graph

load_dotenv()

llm = ChatNVIDIA(
    model="nv-mistralai/mistral-nemo-12b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"),
)

# Graph state
class State(TypedDict):
    collectivite: str
    presentation_generale: str
    interlocuteurs: str
    budget_primitif_2024: str
    situation_financiere: str
    projets_verts: str
    projets_sociaux: str
    comparatif_collectivites: str
    fiche_client: str
    
class SearchQuery(BaseModel):
    search_query: str = Field(
        None, description="Query for web search."
    )
    
class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the report.",
    )
    description: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )
    queries: List[SearchQuery] = Field(
        description="list of search queries for this section.",
    )
    content:str = Field(
        description="The content of the section."
    ) 

class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the report.",
    )
    

async def presentation_generale(state: State):
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Informations démographiques de {collectivite}"},
        {"search_query": f"Historique des réorganisations de {collectivite} des 30 dernières années"},
        {"search_query": f"Caractéristiques économiques et administratives de {collectivite}"}
    ]
    section_data = {
        "name": "presentation generale",
        "description": "Analyse de la présentation générale de la collectivité",
        "queries": queries,
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "completed_sections": []
    }
    result = await section_builder_graph.ainvoke(initial_state)
    completed_section = result["completed_sections"][0]
    return {"presentation_generale": completed_section.content}

async def interlocuteurs(state: State):
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Liste des dirigeants de {collectivite}"},
        {"search_query": f"Parcours et formation des élus de {collectivite}"},
        {"search_query": f"Fonctions et responsabilités des responsables de {collectivite}"}
    ]
    section_data = {
        "name": "interlocuteurs",
        "description": "Liste détaillée des interlocuteurs de la collectivité",
        "queries": queries,
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "completed_sections": []
    }
    result = await section_builder_graph.ainvoke(initial_state)
    completed_section = result["completed_sections"][0]
    return {"interlocuteurs": completed_section.content}


async def budget_primitif_2024(state: State):
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Montant total du budget adopté pour {collectivite}"},
        {"search_query": f"Répartition entre dépenses de fonctionnement et d’investissement pour {collectivite}"},
        {"search_query": f"Axes de financement et priorités budgétaires de {collectivite}"}
    ]
    section_data = {
        "name": "budget primitif 2024",
        "description": "Rapport sur le budget primitif 2024 de la collectivité",
        "queries": queries,
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "completed_sections": []
    }
    result = await section_builder_graph.ainvoke(initial_state)
    completed_section = result["completed_sections"][0]
    return {"budget_primitif_2024": completed_section.content}


async def situation_financiere(state: State):
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Niveaux d'endettement de {collectivite}"},
        {"search_query": f"Ratios financiers et épargne brute de {collectivite}"},
        {"search_query": f"Comparaison de la situation financière de {collectivite} avec la moyenne nationale ou régionale"}
    ]
    section_data = {
        "name": "situation financiere",
        "description": "Analyse de la situation financière (Exercice 2023) de la collectivité",
        "queries": queries,
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "completed_sections": []
    }
    result = await section_builder_graph.ainvoke(initial_state)
    completed_section = result["completed_sections"][0]
    return {"situation_financiere": completed_section.content}


async def projets_verts(state: State):
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Investissements en énergies renouvelables à {collectivite}"},
        {"search_query": f"Initiatives de mobilité durable et infrastructures de {collectivite}"},
        {"search_query": f"Actions en urbanisme durable et efficacité énergétique à {collectivite}"}
    ]
    section_data = {
        "name": "projets verts",
        "description": "Rapport sur les projets verts de la collectivité",
        "queries": queries,
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "completed_sections": []
    }
    result = await section_builder_graph.ainvoke(initial_state)
    completed_section = result["completed_sections"][0]
    return {"projets_verts": completed_section.content}


async def projets_sociaux(state: State):
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Équipements éducatifs à {collectivite}"},
        {"search_query": f"Infrastructures sportives et culturelles de {collectivite}"},
        {"search_query": f"Politiques d’inclusion sociale et renouvellement urbain à {collectivite}"}
    ]
    section_data = {
        "name": "projets sociaux",
        "description": "Rapport sur les projets sociaux de la collectivité",
        "queries": queries,
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "completed_sections": []
    }
    result = await section_builder_graph.ainvoke(initial_state)
    completed_section = result["completed_sections"][0]
    return {"projets_sociaux": completed_section.content}


async def comparatif_collectivites(state: State):
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Indicateurs financiers de {collectivite}"},
        {"search_query": f"Comparaison budgétaire de {collectivite} avec d'autres collectivités"},
        {"search_query": f"Initiatives de transition écologique et sociale à {collectivite}"}
    ]
    section_data = {
        "name": "comparatif collectivites",
        "description": "Comparaison du client avec des collectivités comparables",
        "queries": queries,
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    initial_state = {
        "number_of_queries": len(queries),
        "section": section,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "completed_sections": []
    }
    result = await section_builder_graph.ainvoke(initial_state)
    completed_section = result["completed_sections"][0]
    return {"comparatif_collectivites": completed_section.content}


def aggregator(state: State):
    """Combine all sections into a single client file output"""
    combined = f"Fiche Client pour {state['collectivite']}:\n\n"
    combined += "1. Présentation Générale:\n" + state['presentation_generale'] + "\n\n"
    combined += "2. Interlocuteurs:\n" + state['interlocuteurs'] + "\n\n"
    combined += "3. Budget Primitif 2024:\n" + state['budget_primitif_2024'] + "\n\n"
    combined += "4. Situation Financière (Exercice 2023):\n" + state['situation_financiere'] + "\n\n"
    combined += "5. Projets Verts:\n" + state['projets_verts'] + "\n\n"
    combined += "6. Projets Sociaux:\n" + state['projets_sociaux'] + "\n\n"
    combined += "7. Comparatif avec des Collectivités Comparables:\n" + state['comparatif_collectivites']
    return {"fiche_client": combined}


# Build workflow
parallel_builder = StateGraph(State)


# Define a list of tuples with node names and their corresponding functions
sections = [
    ("call_section_1", presentation_generale),
    ("call_section_2", interlocuteurs),
    ("call_section_3", budget_primitif_2024),
    ("call_section_4", situation_financiere),
    ("call_section_5", projets_verts),
    ("call_section_6", projets_sociaux),
    ("call_section_7", comparatif_collectivites),
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
async def run_workflow():
    state = await parallel_workflow.ainvoke({"collectivite": "Nice"})
    print(state["fiche_client"])

asyncio.run(run_workflow())

