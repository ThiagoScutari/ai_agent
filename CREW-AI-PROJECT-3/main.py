import os
from dotenv import load_dotenv

# --- Passo 1: Carregar Nossas Chaves de API ---
# Como o .env está na mesma pasta, isso funciona perfeitamente.
load_dotenv()

# --- Passo 2: Importar as Ferramentas do CrewAI e o Cérebro (LLM) ---
from crewai import Agent, Task, Crew, Process
from crewai import LLM
import os


# --- Passo 3: Definir o Cérebro (LLM) ---
# Ele vai ler 'MODEL' e 'GOOGLE_API_KEY' do seu .env
# Configuração do LLM usando a classe nativa do CrewAI
llm = LLM(
  model="gemini/gemini-2.5-flash",
  api_key=os.getenv("GEMINI_API_KEY")
)
print("--- [MAIN] Cérebro (LLM) configurado. ---")

# --- Passo 4: Criar nosso Agente ---
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
  llm=llm # Define qual "cérebro" este agente usa
)

# --- Passo 5: Criar nossa Tarefa Dinâmica ---
task_research_destination = Task(
  description='Pesquise sobre as melhores praias e atividades culturais em {destino_desejado}.',
  expected_output=(
    "Um parágrafo de resumo sobre o {destino_desejado}, seguido por uma lista (bullet points) "
    "com 3 praias recomendadas e 3 atividades culturais imperdíveis."
  ),
  agent=destination_specialist
)

# --- Passo 6: Montar a Equipe e Obter Input do Usuário ---
def run_crew():
    travel_crew = Crew(
      agents=[destination_specialist],
      tasks=[task_research_destination],
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