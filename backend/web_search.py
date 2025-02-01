import asyncio
import os
from typing import List, Literal, Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langsmith import traceable
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
    

class SectionState(TypedDict):
    number_of_queries: int # Number web search queries to perform per section 
    section: Section # Report section   
    search_queries: list[SearchQuery] # List of search queries
    source_str: str # String of formatted source content from web search
    report_sections_from_research: str # String of any completed sections from research to write final sections
    completed_sections: list[Section] # Final key we duplicate in outer state for Send() API

class SectionOutputState(TypedDict):
    completed_sections: list[Section]

def deduplicate_and_format_sources(search_response, max_tokens_per_source, include_raw_content=True):
    """
    Takes either a single search response or a list of responses from Tavily API and formats them.
    Limits the raw_content to approximately max_tokens_per_source.
    Now includes images associated with each search result.
    
    Args:
        search_response: Either:
            - A dict with a 'results' key (and optionally an 'images' key) 
            - A list of dicts, each containing search results and optionally an 'images' key.
            
    Returns:
        str: Formatted string with deduplicated sources, including images.
    """
    # print("DEBUG: search_response:", search_response)
    sources_list = []
    
    if isinstance(search_response, dict):
        images = search_response.get('images', [])
        for result in search_response.get('results', []):
            result['images'] = images  # Associate top-level images with each result
            sources_list.append(result)
    elif isinstance(search_response, list):
        for response in search_response:
            if isinstance(response, dict) and 'results' in response:
                images = response.get('images', [])
                for result in response['results']:
                    result['images'] = images  # Associate images with the corresponding result
                    sources_list.append(result)
            else:
                sources_list.extend(response)
    else:
        raise ValueError("Input must be either a dict with 'results' or a list of search results")
    
    # Deduplicate by URL, merging images from duplicates if necessary
    unique_sources = {}
    for source in sources_list:
        url = source['url']
        if url not in unique_sources:
            unique_sources[url] = source
        else:
            existing_images = set(unique_sources[url].get('images', []))
            new_images = set(source.get('images', []))
            unique_sources[url]['images'] = list(existing_images.union(new_images))
    
    # Format output with images included
    formatted_text = "Sources:\n\n"
    for source in unique_sources.values():
        formatted_text += f"Source {source['title']}:\n===\n"
        formatted_text += f"URL: {source['url']}\n===\n"
        formatted_text += f"Most relevant content from source: {source['content']}\n===\n"
        
        images = source.get('images', [])
        if images:
            images_text = ", ".join(images)
            formatted_text += f"Images: {images_text}\n===\n"
        
        if include_raw_content:
            char_limit = max_tokens_per_source * 4  # Approximate conversion
            raw_content = source.get('raw_content') or ''
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
                max_results=5,
                include_raw_content=True,
                include_images=True,
                topic="general",
            )
        )

    # Execute all searches concurrently
    search_docs = await asyncio.gather(*search_tasks)
    # print("DEBUG: Search docs:", search_docs)
    return search_docs

section_writer_instructions = """You are an expert technical writer crafting one section of a technical report.

Topic for this section:
{section_topic}

Guidelines for writing:

1. Technical Accuracy:
- Include specific version numbers
- Reference concrete metrics/benchmarks
- Cite official documentation
- Use technical terminology precisely

2. Length and Style:
- Strict 150-200 word limit
- No marketing language
- Technical focus
- Write in simple, clear language
- Start with your most important insight in **bold**
- Use short paragraphs (2-3 sentences max)

3. Structure:
- Use ## for section title (Markdown format)
- Only use ONE structural element IF it helps clarify your point:
  * Either a focused table comparing 2-3 key items (using Markdown table syntax)
  * Or a short list (3-5 items) using proper Markdown list syntax:
    - Use `*` or `-` for unordered lists
    - Use `1.` for ordered lists
    - Ensure proper indentation and spacing
- End with ### Sources that references the below source material formatted as:
  * List each source with title, date, and URL
  * Format: `- Title : URL`

3. Writing Approach:
- Include at least one specific example or case study
- Use concrete details over general statements
- Make every word count
- No preamble prior to creating the section content
- Focus on your single most important point

4. Use this source material to help write the section:
{context}

5. Quality Checks:
- Exactly 150-200 words (excluding title and sources)
- Careful use of only ONE structural element (table or list) and only if it helps clarify your point
- One specific example / case study
- Starts with bold insight
- No preamble prior to creating the section content
- Sources cited at end"""

async def search_web(state: SectionState):
    """ Search the web for each query, then return a list of raw sources and a formatted string of sources."""
    
    # Get state 
    search_queries = state["search_queries"]

    # Web search
    query_list = [query.search_query for query in search_queries]
    search_docs = await tavily_search_async(query_list)

    # Deduplicate and format sources
    source_str = deduplicate_and_format_sources(search_docs, max_tokens_per_source=5000, include_raw_content=True)
    return {"source_str": source_str}

def write_section(state: SectionState):
    """ Write a section of the report """

    # Get state 
    section = state["section"]
    source_str = state["source_str"]

    # Format system instructions
    system_instructions = section_writer_instructions.format(section_title=section.name, section_topic=section.description, context=source_str)

    # Generate section  
    section_content = llm.invoke([SystemMessage(content=system_instructions)]+[HumanMessage(content="Generate a report section based on the provided sources.")])
    
    # Write content to the section object  
    section.content = section_content.content

    # Write the updated section to completed sections
    return {"completed_sections": [section]}

    
section_builder = StateGraph(SectionState, output=SectionOutputState)
section_builder.add_node("search_web", search_web)
section_builder.add_node("write_section", write_section)
section_builder.add_edge(START, "search_web")
section_builder.add_edge("search_web", "write_section")
section_builder.add_edge("write_section", END)
section_builder_graph = section_builder.compile()

