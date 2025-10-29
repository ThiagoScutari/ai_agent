import sys

# Adiciona o diretório 'src' ao path do Python
# Isso é necessário para que possamos importar 'src.crew'
sys.path.append('src')

# Importar a instância do nosso crew
# O 'try...except' garante que TODOS os nossos arquivos
# (llm_config, tools, agents, tasks) sejam carregados primeiro.
try:
    from src.crew import study_crew
    print("--- [main] Crew importado com sucesso. ---")
except ImportError as e:
    print(f"Erro ao importar o crew: {e}")
    print("Certifique-se de que todos os arquivos em 'src/' existem.")
    sys.exit(1)
except Exception as e:
    print(f"Ocorreu um erro inesperado durante a inicialização: {e}")
    sys.exit(1)

def run_crew():
    """
    Função principal para rodar o crew.
    """
    # Pede o tópico ao usuário
    topic = input("Olá! Qual tópico você gostaria de estudar hoje? \n> ")

    if not topic:
        print("Tópico não pode ser vazio. Saindo.")
        return

    print(f"\n--- [main] Iniciando o Crew para o tópico: '{topic}' ---")

    # Prepara os inputs para o crew
    # Isso "injeta" a variável '{topic}' que definimos nas tarefas
    inputs = {
        'topic': topic
    }

    # "Dá o play" (kickoff) no crew
    try:
        # O kickoff começa com a primeira tarefa da lista (task_planning)
        # e segue a sequência
        result = study_crew.kickoff(inputs=inputs)

        print("\n\n--- [main] Execução do Crew Finalizada ---")
        print("--- Resultado Final ---")
        print(result)
        print(f"\nVerifique a pasta 'outputs/' para os arquivos Markdown gerados.")

    except Exception as e:
        print(f"\nOcorreu um erro durante a execução do crew: {e}")
        print("Verifique suas chaves de API (GEMINI, SERPER) no .env e a conexão com a internet.")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    run_crew()