import asyncio
import os
from datetime import datetime
from typing import List, Literal, Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langsmith import traceable
# from .prompts import *
from pydantic import BaseModel, Field
from tavily import AsyncTavilyClient, TavilyClient
from typing_extensions import TypedDict

load_dotenv()

tavily_client = TavilyClient()
tavily_async_client = AsyncTavilyClient()

llm = ChatNVIDIA(
    model="nv-mistralai/mistral-nemo-12b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"),
)

class SearchQuery(BaseModel):
    search_query: str = Field(
        None, description="Query for web search."
    )
    
class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the report.",
    )
    content:str = Field(
        description="The content of the section."
    ) 

class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the report.",
    )

class SectionState(TypedDict):
    number_of_queries: int # Number web search queries to perform per section   
    section: Section # Section to write
    writer_prompt: str 
    search_queries: list[SearchQuery] # List of search queries
    source_str: str # String of formatted source content from web search
    report_sections_from_research: str # String of any completed sections from research to write final sections
    web_sources: list[str] # List of raw sources from web search
    images: list[str] # List of images from web search
    completed_sections: list[Section] # Final key we duplicate in outer state for Send() API

class SectionOutputState(TypedDict):
    images: list[str]
    web_sources: list[str]
    completed_sections: list[Section]

def deduplicate_and_format_sources(search_response, max_tokens_per_source, include_raw_content=False):
    """
    Takes either a single search response or a list of responses from Tavily API and formats them.
    Limits the raw_content to approximately max_tokens_per_source.
    Does not include images or URLs in the formatted output.
    """
    sources_list = []
    
    if isinstance(search_response, dict):
        for result in search_response.get('results', []):
            sources_list.append(result)
    elif isinstance(search_response, list):
        for response in search_response:
            if isinstance(response, dict) and 'results' in response:
                for result in response['results']:
                    sources_list.append(result)
            else:
                sources_list.extend(response)
    else:
        raise ValueError("Input must be either a dict with 'results' or a list of search results")
    
    unique_sources = {}
    for source in sources_list:
        url = source['url']
        if url not in unique_sources:
            unique_sources[url] = source
    
    formatted_text = "Sources:\n\n"
    for source in unique_sources.values():
        formatted_text += f"Source {source['title']}:\n===\n"
        formatted_text += f"Most relevant content from source: {source['content']}\n===\n"
        
        if include_raw_content:
            char_limit = max_tokens_per_source * 4
            raw_content = source.get('raw_content', '')
            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"
            formatted_text += f"Full source content limited to {max_tokens_per_source} tokens: {raw_content}\n\n"
    
    return formatted_text.strip()


@traceable
async def tavily_search_async(search_queries):
    """
    Performs concurrent web searches using the Tavily API.

    Args:
        search_queries (List[SearchQuery]): List of search queries to process
        tavily_topic (str): Type of search to perform ('news' or 'general')
        tavily_days (int): Number of days to look back for news articles (only used when tavily_topic='news')

    Returns:
        List[dict]: List of search results from Tavily API, one per query

    Note:
        For news searches, each result will include articles from the last `tavily_days` days.
        For general searches, the time range is unrestricted.
    """
    
    search_tasks = []
    for query in search_queries:
        search_tasks.append(
            tavily_async_client.search(
                query,
                max_results=2,
                include_raw_content=False,
                include_images=True,
                topic="general",
            )
        )

    # Execute all searches concurrently
    search_docs = await asyncio.gather(*search_tasks)
    #  Add urls and images to state
    # print("DEBUG: Search docs:", search_docs)
    return search_docs


async def search_web(state: SectionState):
    """Search the web for each query and return a formatted source string along with images and web_sources."""
    
    search_queries = state["search_queries"]
    query_list = [query.search_query for query in search_queries]
    search_docs = await tavily_search_async(query_list)
    
    urls = []
    all_images = []
    for doc in search_docs:
        if isinstance(doc, dict):
            images = doc.get('images', [])
            all_images.extend(images)
            for result in doc.get('results', []):
                urls.append(result.get('url'))
        elif isinstance(doc, list):
            for result in doc:
                urls.append(result.get('url'))
                all_images.extend(result.get('images', []))
    
    # Deduplicate the lists and update state
    web_sources = list(set(urls))
    images = list(set(all_images))
    state["web_sources"] = web_sources
    state["images"] = images
    
    source_str = deduplicate_and_format_sources(
        search_docs,
        max_tokens_per_source=2000,
        include_raw_content=False
    )
    
    
    return {"source_str": source_str, "web_sources": web_sources, "images": images}


def write_section(state: SectionState):
    """ Write a section of the report """

    quality_check_prompt = (
        "Vérifications de qualité : "
        "- La structure de la section est respectée. "
        "- Le texte est entièrement en Francais. " 
        "- Assurer clarté et concision. "
        "- Vérifier l'exactitude des données (chiffres et faits). "
        # "- Vous utilisez toujours les informations les plus récentes et les plus pertinentes. Rien qui date de plus de 60 ans."
    )

    section = state["section"]
    source_str = state["source_str"]

    # Format the writer_prompt (which contains the {context} placeholder) with source_str
    formatted_writer_prompt = state["writer_prompt"].format(context=source_str)
    # print(formatted_writer_prompt)
    # Combine all parts into the final system_instructions string
    # system_instructions = f"{formatted_writer_prompt}\n\n{quality_check_prompt}"

    # Generate section  
    section_content = llm.invoke(
        [SystemMessage(content=quality_check_prompt)]+[HumanMessage(content=formatted_writer_prompt)]
    )
    section.content = section_content.content
    results_data = {
        "completed_sections": [section],
        "images": state["images"],
        "web_sources": state["web_sources"],
    }
    return SectionOutputState(**results_data)

    
section_builder = StateGraph(SectionState, output=SectionOutputState)
section_builder.add_node("search_web", search_web)
section_builder.add_node("write_section", write_section)
section_builder.add_edge(START, "search_web")
section_builder.add_edge("search_web", "write_section")
section_builder.add_edge("write_section", END)
section_builder_graph = section_builder.compile()

