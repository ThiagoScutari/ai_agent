import sys
import os

# --- Configuração de Caminho (Path) Robusta ---

# 1. Obter o diretório do projeto (ex: .../CREW-AI-PROJECT-7)
project_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Obter o diretório 'src' (ex: .../CREW-AI-PROJECT-7/src)
src_dir = os.path.join(project_dir, 'src')

# 3. Adicionar AMBOS ao sys.path
# Adiciona .../CREW-AI-PROJECT-7/
# (Permite o "from src.crew import study_crew")
sys.path.append(project_dir) 
# Adiciona .../CREW-AI-PROJECT-7/src/
# (Ajuda os arquivos dentro de 'src' a se encontrarem, resolvendo o erro)
sys.path.append(src_dir) 
# --- Fim da Configuração do Caminho ---

try:
    # Esta importação agora deve funcionar sem problemas
    from src.crew import study_crew
    print("--- [main.py] Crew importado com sucesso. ---")
except ImportError as e:
    print(f"Erro de Importação: {e}")
    print("Certifique-se de que todos os arquivos (agents, tasks, tools) estão em 'src/'.")
    sys.exit(1)
except Exception as e:
    print(f"Ocorreu um erro inesperado durante a inicialização: {e}")
    sys.exit(1)

def run():
    """
    Função principal para rodar o crew.
    """
    print("\n--- 🏁 Iniciando o Agente de Busca (POC) ---")
    # Pede o tópico ao usuário
    topic = input("Qual tópico você gostaria de pesquisar para a POC?\n> ")

    if not topic:
        print("Tópico não pode ser vazio. Saindo.")
        return

    print(f"\n--- 🚀 Dando 'kickoff' no Crew para o tópico: '{topic}' ---")
    print("--- (Aguarde... Isso pode levar vários minutos.) ---")

    # Prepara os inputs para o crew
    inputs = {
        'topic': topic
    }

    # "Dá o play" (kickoff) no crew
    try:
        result = study_crew.kickoff(inputs=inputs)

        print("\n\n--- ✅ Execução do Crew Finalizada (POC) ---")
        print("--- Resultado Final (Output da última tarefa) ---")
        print(result)
        
        print("\n--- 📁 Verificação dos Arquivos ---")
        print("Verifique a pasta 'CREW-AI-PROJECT-7/outputs/'")
        print("Você deve encontrar:")
        print("  - 0_plano_de_pesquisa.md (Log)")
        print("  - 0_relatorio_urls.md (Log)")
        print("  - 0_analise_lote_1.md (Log)")
        print("  - 0_analise_lote_2.md (Log)")
        print("  - 1_Fundamentos/fundamentos.md (Resultado Final Lote 1)")
        print("  - 2_Contexto_e_Aplicacoes/contexto.md (Resultado Final Lote 2)")


    except Exception as e:
        print(f"\n--- ❌ Ocorreu um erro durante a execução do crew ---")
        print(e)
        print("\n--- Dicas de Debug ---")
        print("1. Verifique suas chaves de API (GEMINI, FIRECRAWL) no .env na raiz 'ai_agent'.")
        print("2. Verifique se você instalou os requirements (pip install -r requirements.txt).")
        print("3. Verifique sua conexão com a internet.")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    run()