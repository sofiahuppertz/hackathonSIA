# H-GenAI 2025: SIA Partners, SFIL, AWS, Nvidia, MistralAI 🚀

## Setup
⚠️ Use env_template to add API keys in .env file inside backend/

pip install -r requirements.txt
cd backend/
uvicorn app:app --reload
cd frontend/
streamlit run main.py

# Bussiness Requirement
## Client Profile

Here are the section titles with guidelines to gather similar info from other local authorities:

1. **General Overview** 🏙️  
   - Demographics: population, area, density.  
   - History of territorial reorganizations (e.g., districts, communities, metropolises).  
   - Key characteristics: role, economic & administrative specifics.

2. **Key Contacts** 📞  
   - Main leaders (Mayor, Metropolitan/Community President, Directors).  
   - Background & education of officials.  
   - Roles & responsibilities.

3. **2024 Budget** 💰  
   - Total approved budget.  
   - Breakdown: operating vs. capital expenses.  
   - Funding priorities.

4. **Financial Status (2023)** 📊  
   - Debt and financial ratios (debt capacity, debt ratio).  
   - Gross savings and self-financing.  
   - Comparisons with national/regional averages.

5. **Green Projects** 🌱  
   - Investments in renewables (solar, wind, biomass).  
   - Sustainable mobility & infrastructure (bike lanes, clean transport).  
   - Urban sustainability & energy efficiency (renovation, public lighting, water management).

6. **Social Projects** 🤝  
   - Educational facilities (schools, colleges, vocational training).  
   - Sports and cultural infrastructure.  
   - Social inclusion and urban renewal policies.

7. **Peer Comparison** 🔍  
   - Compare key financial and budget indicators with similar authorities.  
   - Analyze similar investments in other regions.  
   - Evaluate eco-friendly and social transition initiatives.


# 🚀 Project Technology Stack

## 🧠 Language Models & AI Frameworks
	•	🔗 nv-mistralai/mistral-nemo-12b-instruct (API)
 	•	Nvidia NIM
## 🔄 Workflow & Orchestration
	•	🔗 Langchain
## 🔍 Search & Retrieval
	•	🔗 TavilySearch
# 🌐 Frontend & User Interface
	•	🎨 Streamlit
# 🖥️ Backend & API Development
	•	⚡ FastAPI

# ☁️ Deployment & Infrastructure (TODO)
	•	☁️ AWS (Amazon Web Services)
	•	Services to Consider: AWS Lambda, EC2, ECS
 
# 📋 Project Structure Overview

📁 project-root/
|
backend/
├── app.py
├── schemas.py
└── srcs/
    ├── client_sheet_generator_agent.py
    ├── prompts.py
    └── web_search_agent.py
|
frontend/
├── DejaVuSans.ttf
├── generate_pdf.py
├── main.py
├── schemas.py
└── utils.py


✅ Key Features
	•	Multi-Agent RAG Workflow: Enhanced interactivity and functionality through Langchain’s multi-agent capabilities.
	•	Efficient Data Retrieval: TavilySearch ensures quick and relevant data fetching.
	•	Interactive UI: Streamlit provides a user-friendly interface for seamless interaction.
	•	Scalable Deployment: AWS ensures your application can scale as needed.


