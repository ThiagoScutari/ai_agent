# src/tools/search_tools.py

import os
from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.tools import DuckDuckGoSearchRun
# Import the actual FirecrawlApp from the library we installed
from firecrawl import FirecrawlApp 

# --- Ferramenta 1: Serper (Busca Google) ---
serper_search_tool = SerperDevTool()

# --- Ferramenta 2: Firecrawl (Scrape Inteligente - CUSTOMIZADO) ---
# Em vez de usar a ferramenta pronta do crewai_tools, vamos criar a nossa
# para garantir que chamamos o método correto (.scrape())

# --- Ferramenta 2: Firecrawl (Scrape Inteligente - CUSTOMIZADO v5 - Correção de Objeto) ---
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY") # Certifique-se que a key está correta no .env

if not firecrawl_api_key:
    print("AVISO: FIRECRAWL_API_KEY não encontrada no .env. A ferramenta Firecrawl não funcionará.")
    @tool("Firecrawl web scrape tool")
    def firecrawl_tool(url: str) -> str:
        """[Ferramenta Desativada - API Key Faltando]"""
        return "Erro: Firecrawl API Key não configurada."
else:
    @tool("Firecrawl web scrape tool")
    def firecrawl_tool(url: str) -> str:
        """
        Raspa (scrape) uma página da web usando Firecrawl e retorna o conteúdo principal
        em formato Markdown ou texto cru, otimizado para análise de LLM.
        Input: A URL completa da página a ser raspada.
        """
        print(f"\n--- [Firecrawl Tool] Tentando raspar: {url} ---")
        try:
            app = FirecrawlApp(api_key=firecrawl_api_key)
            # A resposta 'scraped_data' é um OBJETO, não um dict
            scraped_data = app.scrape(url=url)

            # --- DEBUG: IMPRIMIR O OBJETO INTEIRO ---
            # Isso vai mostrar a estrutura do objeto retornado
            print(f"--- [Firecrawl Tool] Dados BRUTOS retornados para {url}: {scraped_data} ---")
            # ----------------------------------------

            # ***** MUDANÇA PRINCIPAL AQUI *****
            # Verificar se o objeto foi retornado E se ele possui os atributos esperados
            if scraped_data:
                # Tenta acessar o atributo .markdown primeiro (ideal)
                if hasattr(scraped_data, 'markdown') and scraped_data.markdown:
                    print(f"--- [Firecrawl Tool] SUCESSO - Retornando Markdown para: {url} ---")
                    return scraped_data.markdown
                # Se falhar, tenta o atributo .content (plano B)
                elif hasattr(scraped_data, 'content') and scraped_data.content:
                    print(f"--- [Firecrawl Tool] SUCESSO - Retornando Content (texto cru) para: {url} ---")
                    return scraped_data.content
                # --- NOVO PLANO C: Tentar extrair o atributo .text se existir ---
                elif hasattr(scraped_data, 'text') and scraped_data.text:
                     print(f"--- [Firecrawl Tool] SUCESSO - Retornando 'text' para: {url} ---")
                     return scraped_data.text
                # ----------------------------------------------------
                else:
                    print(f"--- [Firecrawl Tool] FALHA - Atributos esperados ('markdown', 'content', 'text') vazios ou ausentes no objeto para: {url} ---")
                    # Adicionando mais detalhes ao erro
                    return f"Erro: Firecrawl retornou um objeto sem conteúdo utilizável ('markdown', 'content', 'text') para {url}. Objeto recebido: {str(scraped_data)[:200]}..." # Mostra o início do objeto
            else:
                # Se scraped_data for None ou vazio
                print(f"--- [Firecrawl Tool] FALHA - Retorno vazio ou None para: {url} ---")
                return f"Erro: Firecrawl retornou uma resposta vazia ou None para {url}. Conteúdo não encontrado."

        except Exception as e:
            print(f"--- [Firecrawl Tool] EXCEÇÃO ao raspar {url}: {e} ---")
            # Incluindo o tipo da exceção para melhor depuração
            return f"Erro ao usar Firecrawl para raspar {url}: {type(e).__name__} - {str(e)}"

# [...] (Ferramenta DuckDuckGo e print final)
print("--- [search_tools] Ferramentas de busca e scrape (Firecrawl CUSTOM v5 - Correção Objeto) carregadas. ---")

# --- Ferramenta 3: DuckDuckGo (Busca Alternativa) ---
@tool("DuckDuckGo Search")
def ddg_search_tool(query: str) -> str:
    """
    Realiza uma busca na web usando o DuckDuckGo para encontrar 
    informações sobre um 'query' (tópico).
    Retorna os resultados da busca.
    """
    return DuckDuckGoSearchRun().run(query)

print("--- [search_tools] Ferramentas de busca e scrape (Firecrawl CUSTOM) carregadas. ---")