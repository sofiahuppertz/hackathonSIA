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
from prompts import presentation_generale_prompt, projets_verts_prompt, tableau_recap_prompt, interlocuteurs_prompt

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_concurrent_workflow

from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict



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
    current_section: str  # Track active section
    sections: dict  # Store all section states
    images: List[str]
    web_sources: List[str]
    fiche_client: str
    messages: Annotated[list, add_messages]


class SearchQuery(BaseModel):
    search_query: str = Field(
        None, description="Query for web search."
    )
    
async def generate_section(
    state: State,
    queries: List[dict],
    prompt_template: str,
    result_key: str,
) -> dict:
    """
    A generic function that builds a section by:
    1. Formatting a prompt with the collectivite.
    2. Building search queries.
    3. Creating an initial state for the section builder.
    4. Invoking the common section builder graph.
    5. Returning the result under the provided key.
    """
    collectivite = state["collectivite"]
    search_query_objs = [SearchQuery(**q) for q in queries]
    prompt = prompt_template.format(collectivite=collectivite)
    section = Section(content="")

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
    result = await section_builder_graph.ainvoke(
        initial_state,
        config={"configurable": {"thread_id": "web_search_123"}}
    )
    return {result_key: result}
    
async def recapitulative(state: State):
    queries = [
        {"search_query": f"{state['collectivite']} encours total budget principal \"euros par habitant\" dette municipal rapport financier 2025 filetype:pdf"},
        {"search_query": f"{state['collectivite']} \"capacité de désendettement\" dette municipal analyse financière indicateur 2025 filetype:pdf"},
        {"search_query": f"{state['collectivite']} \"taux d'endettement\" finances municipales indicateurs dette analyse 2025"},
        {"search_query": f"{state['collectivite']} \"durée apparente de la dette\" analyse financière municipal rapport 2025 filetype:pdf"},
        {"search_query": f"{state['collectivite']} métropole finances municipales comparaison indicateurs encours budget capacité désendettement taux endettement durée dette 2025 filetype:pdf"}
    ]
    return await generate_section(state, queries, tableau_recap_prompt, "recapitulative")

async def presentation_generale(state: State):
    queries = [
        {"search_query": f"Statistiques officielles de {state['collectivite']} : population de la Métropole, superficie et densité de population en 2024"},
        {"search_query": f"Événements clés et réformes de {state['collectivite']} pendant les 30 dernières années"},
        {"search_query": f"Événements clés et réformes de {state['collectivite']} pendant les 60 dernières années"},
        {"search_query": f"Compétences et missions principales de {state['collectivite']} : responsabilités, attributions et organisation administrative."},
        {"search_query": f"Secteurs économiques dominants de {state['collectivite']}"},
        {"search_query": f"Patrimoine culturel de {state['collectivite']}"},
    ]
    return await generate_section(state, queries, presentation_generale_prompt, "presentation_generale")

async def projets_verts(state: State):
    queries = [
        {"search_query": f"{state['collectivite']} transition écologique site officiel projets environnementaux 2024 budget écologie 2024 filetype:pdf politiques publiques environnement programme développement durable"},
        {"search_query": f"{state['collectivite']} énergies renouvelables projets panneaux solaires installations politique énergétique municipale transition énergétique budget solaire photovoltaïque ville"},
        {"search_query": f"{state['collectivite']} transports propres mobilité durable infrastructures cyclables 2024 pistes cyclables projet filetype:pdf plan mobilité durable véhicules électriques municipaux"},
        {"search_query": f"{state['collectivite']} assainissement projets gestion des eaux pluviales réduction rejets eaux usées bassins d’orages investissement pollution eaux plan d’action"},
        {"search_query": f"{state['collectivite']} rénovation énergétique écoles bâtiments publics plan efficacité énergétique 2024 réduction consommation énergétique transition énergétique bâtiments municipaux budget municipal écologie 2024 filetype:pdf rapport développement durable filetype:pdf plan climat énergie territorial rapport investissement écologique dossier subventions écologiques"}
    ]
    return await generate_section(state, queries, projets_verts_prompt, "projets_verts")

async def interlocuteurs(state: State):
    queries = [
        {"search_query": f"Maire de la métropole de {state['collectivite']} Infos: Nom, Prénom, Date et Lieu de Naissance, Formation, Carrière Chronologique et Activités en cours"},
        {"search_query": f"Directeur Financier de {state['collectivite']} - Profil Complet: Nom, Prénom, Date et Lieu de Naissance, Formation, Parcours Professionnel et Autres Activités"},
        {"search_query": f"Directeur Général des Services de {state['collectivite']} - Détails Biographiques: Nom, Prénom, Date et Lieu de Naissance, Formation, Carrière Chronologique, Activités"},
        {"search_query": f"Biographie détaillée des dirigeants de {state['collectivite']}: Maire, Directeur Financier, Directeur Général des Services - Informations personnelles, formation et parcours professionnel"},
        {"search_query": f"Profil complet des responsables de {state['collectivite']} : Maire, Directeur Financier, Directeur Général des Services - Données sur naissance, formation, carrière et activités actuelles"},
    ]
    return await generate_section(state, queries, interlocuteurs_prompt, "interlocuteurs")

def aggregator(state: State):
    combined = f"# Fiche Client pour {state['collectivite']}:\n\n"
    combined += "## 1. Récapitulative:\n" + state["recapitulative"]["completed_sections"] + "\n\n"
    combined += "## 2. Présentation Générale:\n" + state["presentation_generale"]["completed_sections"] + "\n\n"
    combined += "## 3. Projets Verts:\n" + state["projets_verts"]["completed_sections"] + "\n\n"
    combined += "## 4. Interlocuteurs:\n" + state["interlocuteurs"]["completed_sections"] + "\n\n"
    
    sections = {
        "recapitulative": state["recapitulative"],
        "presentation_generale": state["presentation_generale"],
        "projets_verts": state["projets_verts"],
        "interlocuteurs": state["interlocuteurs"],
    }

    images_by_section = {}
    sources_by_section = {}
    
    for name, section in sections.items():
        images_by_section[name] = section.get("images", [])
        sources_by_section[name] = section.get("web_sources", [])
    

    all_images = list(state.get("images", []))
    all_web_sources = list(state.get("web_sources", []))
    
    for section in [state["recapitulative"], state["presentation_generale"], state["projets_verts"], state["interlocuteurs"]]:
        all_images.extend(section.get("images", []))
        all_web_sources.extend(section.get("web_sources", []))
    
    return {
        "fiche_client": combined,
        "images": all_images,
        "web_sources": all_web_sources,
        "images_by_section": images_by_section,
        "sources_by_section": sources_by_section,
    }
    
# Build workflow
parallel_builder = StateGraph(State)


# Define a list of tuples with node names and their corresponding functions
sections = [
    ("recapitulative", recapitulative),
    ("presentation_generale", presentation_generale),
    ("projets_verts", projets_verts),
    ("interlocuteurs", interlocuteurs),
    # ("call_section_3", budget_primitif_2024),
    # ("call_section_4", situation_financiere),
    # ("call_section_6", projets_sociaux),
    # ("call_section_7", comparatif_collectivites),
]

checkpointer = SqliteSaver.from_conn_string(":memory:")  


parallel_builder = create_concurrent_workflow(
    "parallel_sections",
    sections,
    aggregator,
    checkpointer=checkpointer
)

# Loop to add nodes and connect them from START and to aggregator
for name, func in sections:
    parallel_builder.add_node(name, func)
    parallel_builder.add_edge(START, name)
    parallel_builder.add_edge(name, "aggregator")

# Add the aggregator node and connect it to END
parallel_builder.add_node("aggregator", aggregator)
parallel_builder.add_edge("aggregator", END)

# Add to your workflow compilation
parallel_workflow = parallel_builder.compile(
    checkpointer=checkpointer,
    visualize=True,  # Enable built-in visualization
    visualization_options={
        "format": "png",
        "filename": "workflow_graph"
    }
)

# Invoke
async def run_workflow(collectivite: str ) -> State:
    state = await parallel_workflow.ainvoke(
        {"collectivite": collectivite},
        config={"configurable": {"thread_id": "client_sheet_456"}}
    )
    return state

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_workflow("Nice"))

