import os
from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.tools import DuckDuckGoSearchRun
from firecrawl import FirecrawlApp # Importar o App


serper_search_tool = SerperDevTool()

# --- Validação da Chave Firecrawl ---
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

if not firecrawl_api_key:
    print("AVISO: FIRECRAWL_API_KEY não encontrada no .env. A ferramenta de SCRAPE Firecrawl não funcionará.")
    # Define uma função 'dummy' se a chave não existir
    @tool("Firecrawl web scrape tool")
    def scrape_tool(url: str) -> str:
        """[Ferramenta Desativada - API Key Faltando]"""
        return "Erro: Firecrawl API Key não configurada para scrape."
else:
    # --- Ferramenta de SCRAPE (Firecrawl - Robusta) ---
    @tool("Firecrawl web scrape tool")
    def scrape_tool(url: str) -> str:
        """
        Raspa (scrape) uma página da web usando Firecrawl e retorna o conteúdo principal
        em formato Markdown ou texto cru, otimizado para análise de LLM.
        Input: A URL completa da página a ser raspada.
        """
        print(f"\n--- [Scrape Tool] Tentando raspar com Firecrawl: {url} ---")
        try:
            app = FirecrawlApp(api_key=firecrawl_api_key)
            scraped_data = app.scrape(url=url)
            print(f"--- [Scrape Tool] Dados BRUTOS retornados para {url}: {scraped_data} ---") # Debug

            if scraped_data:
                if hasattr(scraped_data, 'markdown') and scraped_data.markdown:
                    print(f"--- [Scrape Tool] SUCESSO - Retornando Markdown para: {url} ---")
                    return scraped_data.markdown
                elif hasattr(scraped_data, 'content') and scraped_data.content:
                    print(f"--- [Scrape Tool] SUCESSO - Retornando Content para: {url} ---")
                    return scraped_data.content
                elif hasattr(scraped_data, 'text') and scraped_data.text:
                     print(f"--- [Scrape Tool] SUCESSO - Retornando 'text' para: {url} ---")
                     return scraped_data.text
                else:
                    msg = f"Erro: Firecrawl retornou objeto sem conteúdo ('markdown', 'content', 'text') para {url}. Obj: {str(scraped_data)[:200]}..."
                    print(f"--- [Scrape Tool] FALHA - {msg}")
                    return msg
            else:
                msg = f"Erro: Firecrawl retornou resposta vazia ou None para {url}."
                print(f"--- [Scrape Tool] FALHA - {msg}")
                return msg
        except Exception as e:
            msg = f"Erro ao usar Firecrawl para raspar {url}: {type(e).__name__} - {str(e)}"
            print(f"--- [Scrape Tool] EXCEÇÃO - {msg}")
            return msg

# --- Ferramenta de BUSCA (DuckDuckGo) ---
# Usaremos esta como nossa ferramenta de busca principal por enquanto
@tool("DuckDuckGo Search")
def search_tool(query: str) -> str:
    """
    Realiza uma busca na web usando o DuckDuckGo para encontrar
    informações sobre um 'query' (tópico). Retorna os resultados da busca.
    Usada pelo Agente Pesquisador.
    """
    print(f"\n--- [Search Tool] Buscando com DDG: {query} ---")
    try:
        results = DuckDuckGoSearchRun().run(query)
        print(f"--- [Search Tool] Resultados DDG encontrados para: {query} ---")
        return results
    except Exception as e:
        msg = f"Erro ao usar DuckDuckGo para buscar '{query}': {type(e).__name__} - {str(e)}"
        print(f"--- [Search Tool] EXCEÇÃO - {msg}")
        return msg


print("--- [search_tools.py] Ferramentas (DDG Search, Firecrawl Scrape v5) carregadas. ---")