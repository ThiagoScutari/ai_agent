import os
from dotenv import load_dotenv
# Esta é a importação que o CrewAI precisa:
from crewai import LLM
# --- Sua lógica (correta) para encontrar o .env na raiz ---
# __file__ é o caminho deste arquivo (.../CREW-AI-PROJECT-7/src/llm_config.py)
project_root = os.path.dirname(     # 1º dirname -> .../CREW-AI-PROJECT-7/src/
    os.path.dirname(                # 2º dirname -> .../CREW-AI-PROJECT-7/
        os.path.dirname(            # 3º dirname -> .../ai_agent/  (Esta é a raiz)
            os.path.abspath(__file__)
            )
        )
    )
dotenv_path = os.path.join(project_root, '.env')

if not load_dotenv(dotenv_path):
    print(f"AVISO: Não foi possível encontrar o arquivo .env em {dotenv_path}")
    print("Certifique-se de que seu .env está na pasta raiz 'ai_agent'.")
# --- Fim da lógica do .env ---

# Carrega a chave de forma segura
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY não encontrada! Verifique seu .env na raiz 'ai_agent'.")

# --- ESTA É A MUDANÇA PRINCIPAL ---
# Instanciamos o LLM que o CrewAI/LangChain entende.
# Usamos 'gemini-pro' como planejado no escopo,
# pois ele é ótimo para as tarefas de raciocínio do Planejador.
llm = LLM(
    model="gemini/gemini-2.5-flash-lite", 
    google_api_key=gemini_key
)

# Não precisamos mais da função de teste,
# então o arquivo termina aqui.
print("--- [llm_config.py] Modelo LangChain/Gemini (gemini-pro) carregado com sucesso. ---")