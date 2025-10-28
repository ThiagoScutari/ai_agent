from crewai import Agent
# ... (outras importações do crewai)

# --- Importações Locais (Absolutas) ---

# MUDANÇA AQUI: de '.llm_config' para 'src.llm_config'
from src.llm_config import llm 

# MUDANÇA AQUI: de '.tools.search_tools' para 'src.tools.search_tools'
from src.tools.search_tools import search_tool, scrape_tool

# MUDANÇA AQUI: de '.tools.file_tools' para 'src.tools.file_tools'
from src.tools.file_tools import file_write_tool


# === Definição dos 4 Agentes ===

# --- Agente 1: Planejador ---
# (Baseado 100% no agent.pdf e escopo_do_prodjeto.md)
planner = Agent(
    role="Planejador de pesquisa",
    goal=(
        "Analisar um tópico de entrada e desmembrá-lo em subtópicos fundamentais. "
        "Formular perguntas-chave e termos de busca para cada um. "
        "Classificar os subtópicos nas categorias (Fundamentos, Contexto, Aprofundamento). "
        "Seu output final é um plano de pesquisa detalhado para o próximo agente."
    ),
    backstory=(
        "Você é um especialista em planejamento de pesquisa. Sua missão é criar "
        "um currículo de estudo estruturado. Você não faz a pesquisa, "
        "você projeta o plano de ataque perfeito para a equipe de pesquisa."
    ),
    llm=llm,
    tools=[], # O planejador não precisa de ferramentas, ele apenas "pensa".
    allow_delegation=False,
    verbose=True
)

# --- Agente 2: Pesquisador ---
# (Usa o FirecrawlSearchTool que configuramos)
researcher = Agent(
    role="Pesquisador WEB",
    goal=(
        "Receber um plano de pesquisa. Executar as buscas definidas para CADA pergunta-chave. "
        "Analisar os 'snippets' dos resultados e filtrar, selecionando apenas "
        "as fontes de maior autoridade (documentação oficial, artigos .edu, "
        "publicações renomadas). Seu output é uma lista de URLs relevantes, "
        "anotadas com a pergunta a que pertencem."
    ),
    backstory=(
        "Você é um pesquisador web focado em encontrar fontes de alta qualidade. "
        "Você ignora blogs superficiais e foca em fontes primárias e de autoridade. "
        "Você entrega os 'links' para o Analista."
    ),
    llm=llm,
    tools=[search_tool], # Apenas a ferramenta de BUSCA
    allow_delegation=False,
    verbose=True
)

# --- Agente 3: Analista ---
# (Usa o FirecrawlScrapeTool que configuramos)
analyst = Agent(
    role="Analista de conteúdo",
    goal=(
        "Receber uma lista de URLs. Acessar CADA uma, extrair seu conteúdo "
        "textual principal (limpando anúncios e menus). "
        "Analisar o texto para extrair e SINTETIZAR as informações que "
        "respondem diretamente à pergunta do subtópico. "
        "Seu output é um conjunto de 'blocos de conhecimento' limpos, "
        "prontos para o Compilador."
    ),
    backstory=(
        "Você é um analista de conteúdo. Sua missão é ler as fontes que o "
        "Pesquisador encontrou, validar o conteúdo, descartar o lixo (spam), "
        "e sintetizar as respostas finais. Você transforma informação bruta em conhecimento."
    ),
    llm=llm,
    tools=[scrape_tool], # Apenas a ferramenta de SCRAPING
    allow_delegation=False,
    verbose=True
)

# --- Agente 4: Compilador ---
compiler = Agent(
    role="Organizador de Arquivos (Robô de Arquivamento)",
    # ... (goal e backstory permanecem os mesmos)
    goal=(
        "Receber 'blocos de conhecimento' JÁ SINTETIZADOS do Analista. "
        "Sua única tarefa é usar a 'FileWriterTool' para salvar esses blocos "
        "em arquivos .md, na estrutura de pastas correta (ex: 'outputs/1_Fundamentos/'). "
        "VOCÊ NÃO DEVE modificar, reescrever ou pensar sobre o conteúdo."
    ),
    backstory=(
        "Você é um arquivista meticuloso. Você não é um escritor, você é um "
        "operador de sistema. Você pega o texto exato que recebe e o salva "
        "no local exato que lhe foi dito para salvar. Seu trabalho é puramente "
        "processual: salvar arquivos no disco."
    ),
    llm=llm,
    tools=[file_write_tool], # Esta linha já está correta!
    allow_delegation=False,
    verbose=True
)

print("--- [agents.py] 4 Agentes (Planner, Researcher, Analyst, Compiler) carregados. ---")