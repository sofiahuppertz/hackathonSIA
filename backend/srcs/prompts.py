tableau_recap_prompt = (
    "Vous devez extraire et organiser les informations financières les plus récentes pour la collectivité locale {collectivite} et sa métropole en deux tableaux distincts au format Markdown.\n\n"
    "Pour chacun des tableaux, respectez le format suivant :\n\n"
    "- Colonnes :\n"
    "  1. Vision récapitulative : le libellé de l'indicateur.\n"
    "  2. Client : la valeur observée pour la collectivité locale (ou la métropole), accompagnée de l’année de référence et d’un lien vers la source.\n"
    "  3. Moyenne nationale : la valeur de référence nationale, accompagnée de l’année de référence et d’un lien vers la source.\n\n"
    "- Lignes (indicateurs à présenter) :\n"
    "  1. Encours total budget principal (en euros et en euros par habitant)\n"
    "     - Exemple : 110 M€ soit 679 €/hab\n"
    "  2. Capacité de désendettement (en années)\n"
    "     - Exemple : 3,4 ans\n"
    "  3. Taux d’endettement (en %)\n"
    "     - Exemple : 51 %\n"
    "  4. Durée apparente de la dette (en années)\n"
    "     - Exemple : 10,1 ans\n\n"
    "Instructions supplémentaires :\n\n"
    "- Pour chaque indicateur, indiquez la valeur, l’année de référence et fournissez le lien vers la source.\n"
    "- Utilisez les documents ci-dessous comme sources d’information :\n\n"
    "  ------------------------------------------------------------\n"
    "  {{context}}\n"
    "  ------------------------------------------------------------\n\n"
    "Organisez et structurez les informations de manière claire et cohérente, en respectant scrupuleusement le format demandé."
)

presentation_generale_prompt = (
    "Vous devez structurer et organiser les informations relatives à la collectivité de {collectivite} "
    "Voici le format attendu :\n"
    " 1. Info Générales\n"
    "    - Collectivité : [nom]\n"
    "    - Habitants : [nombre] (année, gentilé)\n"
    "    - Superficie : [km²], densité : [hab./km²]\n"
    "2. Histoire et évolution administrative\n"
    "    - Réformes majeures : \n"
    "    - Dates clés : \n"
    "3. Caractéristiques clés: \n"
    "    - Secteurs économiques dominants :  \n"
    "    - Patrimoine et culture :  \n"
    "Utilisez les sources suivantes pour compléter et étayer votre fiche :\n"
    "------------------------------------------------------------\n"
    "{{context}}\n"
    "------------------------------------------------------------\n"
    "Veuillez intégrer ces informations de manière pertinente dans la rédaction de votre fiche."
)

projets_verts_prompt = (
    "Vous devez transformer les informations relatives aux projets de la collectivité de {collectivite} "
    "en un tableau structuré selon le format suivant :\n"
    " 1. Thème\n"
    "    - Grande catégorie sous laquelle s’inscrit le projet (ex: Énergies renouvelables, Mobilité douce, Gestion de l’eau).\n"
    " 2. Catégorie de projets\n"
    "    - Type de projet spécifique (ex: Énergies solaires, Transport individuel, Service public de l’assainissement).\n"
    " 3. Principaux investissements en montants associés\n"
    "    - Investissements majeurs avec les montants associés lorsqu’ils sont disponibles.\n"
    " 4. Libellé politique publique ou budget\n"
    "    - Cadre budgétaire ou politique publique associée au projet (ex: Plan de Solarisation, Plan pluriannuel de rénovation des écoles).\n"
    "Format de sortie attendu : Markdown\n"
    "Utilisez les sources suivantes pour compléter et structurer le tableau :\n"
    "------------------------------------------------------------\n"
    "{{context}}\n"
    "------------------------------------------------------------\n"
    "Veuillez organiser les informations de manière claire et cohérente en respectant le format demandé."
)

interlocuteurs_prompt = (
    "Vous devez structurer et organiser les informations relatives à un dirigeant de la collectivité de {collectivite}.\n"
    "Veuillez créer une fiche détaillée pour chaque personne identifiée (Maire, Directeur Financier, Directeur Général des Services, etc.).\n"
    "Le format attendu est le suivant :\n"
    "1. Informations Personnelles:\n"
    "   - Nom et Prénom : [Nom et Prénom]\n"
    "   - Date de Naissance : [JJ/MM/AAAA]\n"
    "   - Lieu de Naissance : [Ville, Pays]\n"
    "2. Formation:\n"
    "   - Diplômes et certifications obtenus, en indiquant les établissements et la chronologie des formations\n"
    "3. Carrière Professionnelle:\n"
    "   - Parcours professionnel détaillé en ordre chronologique (postes occupés, dates et responsabilités associées)\n"
    "4. Autres Activités en Cours:\n"
    "   - Engagements, activités ou responsabilités complémentaires\n"
    "------------------------------------------------------------\n"
    "{{context}}\n"
    "------------------------------------------------------------\n"
    "Intégrez ces informations de manière pertinente afin de mettre en lumière le profil complet et la trajectoire du dirigeant."
)
