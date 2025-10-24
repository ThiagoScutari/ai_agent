import os
from dotenv import load_dotenv

# --- Passo 1: Carregar Chaves ---
# Isso agora carrega AMBAS as chaves (GEMINI e SERPER)
load_dotenv()

from crewai import Agent, Task, Crew, Process
from crewai import LLM

# Passo 1: Importar o decorator @tool de crewai_tools
from crewai.tools import tool

# Passo 2: Importar a funcionalidade de busca do DuckDuckGo da langchain_community
from langchain_community.tools import DuckDuckGoSearchRun

# --- Passo 3: Definir o Cérebro (LLM) ---
llm = LLM(
  model="gemini/gemini-2.5-flash-lite", # ou "gemini/gemini-1.5-pro-latest"
  api_key=os.getenv("GEMINI_API_KEY")
)
print("--- [MAIN] Cérebro (LLM) configurado. ---")

# Passo 3: Criar a ferramenta de busca usando o decorator
# O nome que você passa para o @tool ("DuckDuckGo Search") é como o agente irá "ver" a ferramenta.
@tool("DuckDuckGo Search")
def search_tool(query: str) -> str:
    """
    Realiza uma busca na web usando o DuckDuckGo para encontrar informações sobre um determinado tópico.
    Retorna os resultados da busca.
    """
    return DuckDuckGoSearchRun().run(query)

# Configuração do seu ambiente (ex: chaves de API, se necessário)
# os.environ = "SUA_CHAVE_API"

# Criar os Agentes
researcher = Agent(
  role='Analista de Pesquisa Sênior',
  goal='Descobrir desenvolvimentos de ponta sobre Agentes de IA',
  backstory="""Você é um Analista de Pesquisa Sênior em um importante think tank de tecnologia.
  Sua especialidade é identificar tendências e tecnologias emergentes sobre Agentes de IA.
  Você tem um talento para dissecar dados complexos e apresentar insights acionáveis.
  Sua principal função é encontrar soluções que estão em andamento que já estão trazendo retorno, 
  sejam eles: financeiro, tempo, educacional, indutrial, etc.""",
  verbose=True,
  allow_delegation=False,
  llm=llm,
  # Passo 4: Passar a ferramenta que acabamos de criar para o agente
  tools=[search_tool]
)

# Criar as Tarefas
research_task = Task(
  description="""Conduza uma análise abrangente dos últimos avanços sobre agentes de IA em 2025.
  Identifique as principais tendências, tecnologias inovadoras e potenciais impactos na indústria.
  Sua resposta final DEVE ser um relatório de análise completo."""  ,
  expected_output="""Um relatório abrangente, detalhando e factivel, com aplicação do mundo real. Enontre os 5 principais avanços sobre agentes de IA em 2025, com fontes.
  faça um relatorio detalhado com cada tópico (aplicação do mundo real de agentes de ai), explicação
  com auxílio de bullet points em formato markdown""",
  agent=researcher
)

# Montar a Equipe (Crew)
tech_crew = Crew(
  agents=[researcher],
  tasks=[research_task],
  verbose=True,
  llm=llm,
  process=Process.sequential
)

# Iniciar o trabalho
result = tech_crew.kickoff()

print("######################")
print(result)