
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


async def interlocuteurs(state: State):
    prompt = ""
        
    collectivite = state["collectivite"]
    queries = [
        {"search_query": f"Liste des dirigeants de {collectivite}"},
        {"search_query": f"Parcours et formation des élus de {collectivite}"},
        {"search_query": f"Fonctions et responsabilités des responsables de {collectivite}"}
    ]
    section_data = {
        "name": "interlocuteurs",
        "description": "Liste détaillée des interlocuteurs de la collectivité",
        "content": ""
    }
    section = Section(**section_data)
    search_query_objs = [SearchQuery(**q) for q in queries]
    initial_state = {
        "number_of_queries": len(queries),
        "writer_prompt": prompt,
        "search_queries": search_query_objs,
        "source_str": "",
        "report_sections_from_research": "",
        "completed_sections": [],
    }
    result = await section_builder_graph.ainvoke(initial_state)
    completed_section = result["completed_sections"][0]
    return {"interlocuteurs": completed_section.content}
