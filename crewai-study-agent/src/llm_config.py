import os
from dotenv import load_dotenv
from crewai import LLM

# Carrega as variáveis de ambiente do arquivo .env
# Isso é crucial para carregar a GEMINI_API_KEY
load_dotenv()

# Pega a API Key do ambiente
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env!")

# Configuração global do LLM (Gemini)
# 'temperature=0.1' (ou 0) é importante para tarefas de pesquisa.
# Isso torna o modelo mais determinístico e focado nos fatos,
# reduzindo a "criatividade" (alucinações).

llm=LLM(
    model="gemini/gemini-2.5-flash-lite",
    api_key=gemini_key
)

print("Modelo Gemini carregado com sucesso.") 
