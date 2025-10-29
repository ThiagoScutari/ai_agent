# src/crew.py

from crewai import Crew, Process

# Importar os agentes da Fase 2
from src.agents import planner, researcher, analyst, compiler

# Importar as tarefas da Fase 3 (com a correção do 'context' que você fez)
from src.tasks import task_planning, task_research, task_analysis, task_compiling

# --- Montagem da Equipe (Crew) ---

# Definir a lista de agentes
agents_list = [planner, researcher, analyst, compiler]

# Definir a lista de tarefas
tasks_list = [task_planning, task_research, task_analysis, task_compiling]

# Criar o Crew
study_crew = Crew(
    agents=agents_list,
    tasks=tasks_list,
    process=Process.sequential, # Garante a execução sequencial
    verbose=True 
)

print("--- [crew] Crew montado com sucesso. ---")