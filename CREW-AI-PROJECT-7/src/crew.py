# src/crew.py
from crewai import Crew, Process

# Importações Locais Absolutas
from src.agents import planner, researcher, analyst, compiler

from src.tasks import (
    task_planning,
    task_research,
    task_analysis_lote1,
    task_compiling_lote1,
    task_analysis_lote2,
    task_compiling_lote2,
    task_analysis_lote3,  # Placeholder
    task_compiling_lote3  # Placeholder
)

# --- Montagem da Equipe (Crew) ---

agents_list = [
    planner,
    researcher,
    analyst,
    compiler
]

# Lista com as 8 tarefas na ordem correta
tasks_list = [
    task_planning,
    task_research,
    task_analysis_lote1,
    task_compiling_lote1,
    task_analysis_lote2,
    task_compiling_lote2,
    task_analysis_lote3,  # Placeholder Lote 3
    task_compiling_lote3  # Placeholder Lote 3
]

study_crew = Crew(
    agents=agents_list,
    tasks=tasks_list, # Usando a lista de 8 tarefas
    process=Process.sequential,
    verbose=True
)

print("--- [crew.py] Crew montado com sucesso (8 tarefas sequenciais - POC). ---")