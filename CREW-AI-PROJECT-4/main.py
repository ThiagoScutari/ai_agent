import os
from dotenv import load_dotenv

# --- Passo 1: Carregar Nossas Chaves de API ---
load_dotenv()

# --- Passo 2: Importar as Ferramentas do CrewAI e o Cérebro (LLM) ---
from crewai import Agent, Task, Crew, Process
from crewai import LLM

# --- Passo 3: Definir o Cérebro (LLM) ---
print("--- [MAIN] Configurando o cérebro (LLM) com o Gemini... ---")
llm = LLM(
    model="gemini/gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)
print("--- [MAIN] Cérebro (LLM) configurado. ---")

# --- Passo 4: Criar nossos Agentes ---

# Agente 1 (sem mudanças)
destination_specialist = Agent(
  role='Especialista em Destinos de Viagem',
  goal='Pesquisar e analisar destinos de viagem com base nos interesses do cliente.',
  backstory=(
    "Como um viajante experiente e analista de pesquisa, você é mestre em "
    "encontrar joias escondidas e planejar viagens inesquecíveis. Você "
    "entende de cultura, custos, logística e atividades locais."
  ),
  verbose=True,
  allow_delegation=False,
  llm=llm
)

# ### NOVO ### Agente 2: Especialista em Mapas
location_finder = Agent(
  role='Especialista em Localização Geográfica',
  goal='Encontrar links precisos do Google Maps para locais específicos mencionados em um texto.',
  backstory=(
    "Você é um especialista em geolocalização e mestre em usar ferramentas de "
    "mapeamento digital. Sua precisão em encontrar as coordenadas e links corretos "
    "para qualquer ponto de interesse é inigualável."
  ),
  verbose=True,
  allow_delegation=False,
  llm=llm
  # tools=[SerperDevTool()] # Exemplo se fôssemos usar Serper. Para Maps_Local, não precisa definir aqui.
)

# --- Passo 5: Criar nossas Tarefas ---

# Tarefa 1 (sem mudanças)
task_research_destination = Task(
  description='Pesquise sobre as melhores praias e atividades culturais em {destino_desejado}.',
  expected_output=(
    "Um parágrafo de resumo sobre o {destino_desejado}, seguido por uma lista (bullet points) "
    "com 3 praias recomendadas e 3 atividades culturais imperdíveis, incluindo seus nomes exatos." # Adicionamos clareza sobre nomes exatos
  ),
  agent=destination_specialist
)

# ### NOVO ### Tarefa 2: Encontrar Links do Maps
task_find_locations = Task(
  description=(
    "Para cada uma das 3 praias e 3 atividades culturais mencionadas no texto anterior, "
    "encontre o link correspondente no Google Maps. Certifique-se de usar os nomes exatos fornecidos."
  ),
  expected_output=(
    "Uma lista formatada em markdown contendo o nome de cada local (praia ou atividade cultural) "
    "e seu respectivo link direto para o Google Maps. Exemplo:\n"
    "- Nome do Local 1: [Link do Google Maps]\n"
    "- Nome do Local 2: [Link do Google Maps]\n"
    "..."
  ),
  agent=location_finder,
  context=[task_research_destination] # ### NOVO ### Diz que esta tarefa depende da saída da anterior
)

# --- Passo 6: Montar a Equipe e Obter Input do Usuário --- ### MODIFICADO ###
def run_crew():
    # ### MODIFICADO ### Adicionamos o novo agente e a nova tarefa
    travel_crew = Crew(
      agents=[destination_specialist, location_finder],
      tasks=[task_research_destination, task_find_locations],
      process=Process.sequential, # Garante que a tarefa 1 rode antes da 2
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
    print(result) # Agora o resultado final será a saída da *última* tarefa (os links)

# Bloco padrão do Python
if __name__ == "__main__":
    run_crew()