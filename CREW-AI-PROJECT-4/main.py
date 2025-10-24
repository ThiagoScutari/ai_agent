import os
from dotenv import load_dotenv

# --- Passo 1: Carregar Chaves ---
# Isso agora carrega AMBAS as chaves (GEMINI e SERPER)
load_dotenv()

# --- Passo 2: Importar Ferramentas ---
from crewai import Agent, Task, Crew, Process
from crewai import LLM
import os
# --- ADIÇÃO 1: Importar a ferramenta NATIVA do CrewAI ---
from crewai_tools import SerperDevTool


# --- Passo 3: Definir o Cérebro (LLM) ---
llm = LLM(
  model="gemini/gemini-2.5-flash-lite", # ou "gemini/gemini-1.5-pro-latest"
  api_key=os.getenv("GEMINI_API_KEY")
)
print("--- [MAIN] Cérebro (LLM) configurado. ---")

# --- ADIÇÃO 2: Instanciar a ferramenta CrewAI ---
# Ela automaticamente lê "SERPER_API_KEY" do .env
search_tool = SerperDevTool()


# --- Passo 4: Criar nossos Agentes ---

# Agente 1 (Destinos) - Sem alteração
destination_specialist = Agent(
  role='Especialista em Destinos de Viagem',
  goal='Pesquisar e analisar destinos de viagem com base nos interesses do cliente.',
  backstory=(
    "Como um viajante experiente e analista de pesquisa, você é mestre em "
    "encontrar joias escondidas e planejar viagens inesquecíveis. Você "
    "entende de cultura, custos, logística e atividades locais."
    "### Não responda nada que não esteja de acordo com suas atribuições."
    "### Caso seja perguntado sobre algo diferente do que está no escopo,"
    "### seja contez e encerre a conversa imediatamente."    
  ),
  verbose=True,
  allow_delegation=False,
  llm=llm 
)

# Agente 2 (Localização) - MODIFICADO
location_specialist = Agent(
  role='Especialista em Localização Geográfica',
  goal='Encontrar links do Google Maps para locais específicos.',
  backstory=(
    "Você é um especialista em GIS, mestre em usar ferramentas de busca "
    "para encontrar as URLs compartilháveis exatas para qualquer local na Terra."
    "### Não responda nada que não esteja de acordo com suas atribuições."
    "### Caso seja perguntado sobre algo diferente do que está no escopo,"
    "### seja contez e encerre a conversa imediatamente."    
  ),
  verbose=True,
  allow_delegation=False,
  llm=llm,
  # --- ADIÇÃO 3: Conceder a ferramenta Serper ao agente ---
  tools=[search_tool] 
)

# --- Passo 5: Criar as Tarefas ---

# Tarefa 1 (Pesquisa de Destino) - Sem alteração
task_research_destination = Task(
  description='Pesquise sobre as melhores praias e atividades culturais em {destino_desejado}.',
  expected_output=(
    "Um parágrafo de resumo sobre o {destino_desejado}, seguido por uma lista (bullet points) "
    "com 3 praias recomendadas e 3 atividades culturais imperdíveis."
  ),
  agent=destination_specialist
)

# Tarefa 2 (Busca de Links) - MODIFICADA
task_find_links = Task(
  description=(
    "Para cada uma das 3 praias e 3 atividades culturais mencionadas no texto anterior, "
    "use sua ferramenta de busca para encontrar o link compartilhável do Google Maps. "
    "Use os nomes exatos fornecidos para a busca (ex: 'Google Maps Ruínas de São Paulo Macao')."
  ),
  expected_output=(
    "Uma lista em bullet points (markdown) com o nome do local e o link do Google Maps. "
    "Exemplo: - Nome do Local: [link_real_do_google_maps]"
  ),
  agent=location_specialist,
  # Contexto para que a Tarefa 2 receba a saída da Tarefa 1
  context=[task_research_destination] 
)


# --- Passo 6: Montar a Equipe e Obter Input do Usuário ---
def run_crew():
    travel_crew = Crew(
      agents=[destination_specialist, location_specialist], # Ambos os agentes
      tasks=[task_research_destination, task_find_links], # Ambas as tarefas
      process=Process.sequential,
      verbose=True
    )

    # 1. Perguntamos ao usuário
    print("\n\n--- [ Bem-vindo à Agência de Viagens CrewAI ] ---")
    destino = input("Para onde você gostaria de viajar? ")

    # 2. Criamos o dicionário de inputs
    inputs_do_usuario = {
        'destino_desejado': destino
    }

    print("\n--- [ Iniciando a Execução do Crew ] ---\n")

    # 3. Passamos os inputs para o kickoff()
    result = travel_crew.kickoff(inputs=inputs_do_usuario)

    print("\n\n--- [ Execução Concluída ] ---")
    print("Resultado Final:")
    print(result)

# Bloco padrão do Python
if __name__ == "__main__":
    run_crew()