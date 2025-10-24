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
destination_specialist = Agent(
  role='Especialista em Destinos de Viagem',
  goal='Pesquisar e analisar destinos de viagem com base nos interesses do cliente.',
  backstory=(
    "Como um viajante experiente e analista de pesquisa, você é mestre em "
    "encontrar joias escondidas e planejar viagens inesquecíveis. Você "
    "entende de cultura, custos, logística e atividades locais."
    "### Não responda nada que não esteja de acordo com suas atribuições."
    "### Caso seja perguntado sobre algo diferente do que está no escopo,"
    "### seja cortês e encerre a conversa imediatamente."
  ),
  verbose=True,
  allow_delegation=False,
  llm=llm,
  # Passo 4: Passar a ferramenta que acabamos de criar para o agente
  tools=[search_tool]
)

# Agente 2 (Localização)
location_specialist = Agent(
  role='Especialista em Localização Geográfica',
  goal='Encontrar links compartilháveis do Google Maps para locais específicos.',
  backstory=(
    "Você é um especialista em GIS, mestre em usar ferramentas de busca na web "
    "para encontrar as URLs compartilháveis exatas para qualquer local na Terra."
    "### Não responda nada que não esteja de acordo com suas atribuições."
    "### Caso seja perguntado sobre algo diferente do que está no escopo,"
    "### seja cortês e encerre a conversa imediatamente."
  ),
  verbose=True,
  allow_delegation=False,
  # --- MUDANÇA 3: Passar o objeto LLM do LangChain ---
  llm=llm,
  # --- Usando a ferramenta DuckDuckGo ---
tools=[search_tool] # Pass the crewai_tools instance here
)

# Tarefa 1 (Pesquisa de Destino)
task_research_destination = Task(
  description='Pesquise sobre as melhores praias e atividades culturais em {destino_desejado}.',
  expected_output=(
    "Um parágrafo de resumo sobre o {destino_desejado}, seguido por uma lista (bullet points) "
    "com 3 praias recomendadas e 3 atividades culturais imperdíveis."
  ),
  agent=destination_specialist
)

# Tarefa 2 (Busca de Links)
task_find_links = Task(
  description=(
    "Para cada uma das 3 praias e 3 atividades culturais mencionadas no texto anterior (resultado da Tarefa 1), "
    "use sua ferramenta de busca para encontrar o link compartilhável REAL do Google Maps. "
    "Seja preciso na busca (ex: 'Google Maps South Beach Miami'). Extraia apenas a URL do Google Maps dos resultados."
  ),
  expected_output=(
    "Uma lista em bullet points (markdown) com o nome do local e o link REAL do Google Maps encontrado. "
    "Exemplo:\n"
    "- South Beach: [https://www.google.com/maps/place/South+Beach,+Miami+Beach,+Fl%C3%B3rida+33139,+EUA/@25.7818486,-80.1558493,14z/data=!3m1!4b1!4m6!3m5!1s0x88d9b48e8bc080f1:0x7afeece4a9efe6bd!8m2!3d25.7826123!4d-80.1340772!16zL20vMDJxeXNs?entry=ttu&g_ep=EgoyMDI1MTAyMC4wIKXMDSoASAFQAw%3D%3D]\n"
    "- Wynwood Walls: [https://www.google.com/maps/place/Wynwood+Walls/@25.8010178,-80.1993841,17z/data=!3m1!4b1!4m6!3m5!1s0x88d9b6b27c5fc0f7:0xd08ca0f3229d29b3!8m2!3d25.8010178!4d-80.1993841!16s%2Fg%2F11b6d4cjb9?entry=ttu&g_ep=EgoyMDI1MTAyMC4wIKXMDSoASAFQAw%3D%3D]\n"
    "Se um link específico não puder ser encontrado de forma confiável após a busca, escreva 'Link não encontrado'."
  ),
  agent=location_specialist,
  context=[task_research_destination] # Garante que a Tarefa 2 receba a saída da Tarefa 1
)

def run_crew():
    print("--- [MAIN] Montando o Crew... ---")
    travel_crew = Crew(
      agents=[destination_specialist, location_specialist],
      tasks=[task_research_destination, task_find_links],
      process=Process.sequential, # Tarefas rodam em sequência
      verbose=True 
    )
    print("--- [MAIN] Crew montado. ---")

    # 1. Perguntamos ao usuário
    print("\n\n--- [ Bem-vindo à Agência de Viagens CrewAI (vLangChain) ] ---")
    destino = input("Para onde você gostaria de viajar? ")

    # 2. Criamos o dicionário de inputs
    inputs_do_usuario = {
        'destino_desejado': destino
    }

    print("\n--- [ Iniciando a Execução do Crew ] ---\n")

    # 3. Passamos os inputs para o kickoff()
    try:
        result = travel_crew.kickoff(inputs=inputs_do_usuario)

        print("\n\n--- [ Execução Concluída ] ---")
        print("Resultado Final:")
        print(result)
    except Exception as e:
        print(f"\n--- [ ERRO DURANTE A EXECUÇÃO DO CREW ] ---")
        print(f"Detalhes: {e}")
        # Se houver um erro, é útil ver o traceback completo
        import traceback
        traceback.print_exc()


# Bloco padrão do Python
if __name__ == "__main__":
    run_crew()