# src/tasks.py
from crewai import Task

# Importar os agentes (agora usando import absoluto)
from src.agents import planner, researcher, analyst, compiler

# === Definição das 8 Tarefas da POC (Baseado no task.pdf) ===

# --- Tarefa 1: Planejamento (POC) ---
task_planning = Task(
    description=(
        "Você é o Arquiteto-Chefe. Analise o tópico de entrada: '{topic}'.\n"
        "Sua missão é criar um 'Plano de Pesquisa' tático para a equipe.\n"
        "**REQUISITO DE POC (Prova de Conceito):** O plano deve ser ENXUTO.\n"
        "Gere APENAS:\n"
        "  - 1 (um) subtópico para a categoria '1_Fundamentos'.\n"
        "  - 1 (um) subtópico para a categoria '2_Contexto_e_Aplicacoes'.\n"
        "NÃO gere subtópicos para '3_Aprofundamento' nesta POC.\n"
        "Para CADA um dos 2 subtópicos, formule 2-3 perguntas-chave exatas.\n"
        "Seu output final é este plano rigoroso, que será o passo-a-passo para o Pesquisador."
    ),
    expected_output=(
        "Um plano de pesquisa detalhado em formato Markdown, contendo "
        "exatamente 1 subtópico para Fundamentos e 1 para Contexto, "
        "cada um com 2-3 perguntas-chave."
    ),
    agent=planner,
    output_file="outputs/0_plano_de_pesquisa.md" # Log
)

# --- Tarefa 2: Pesquisa (Total Qualificada) ---
task_research = Task(
    description=(
        "Receba o plano de POC do Planejador. Sua missão é encontrar as fontes.\n"
        "Para **CADA pergunta-chave** no plano, você DEVE encontrar as "
        "**3 (três) melhores e mais relevantes URLs**.\n"
        "Use sua ferramenta de busca (DuckDuckGo Search) e priorize " # Usando DDG agora
        "fontes primárias (documentação oficial, artigos .edu, etc.).\n"
        "Seu output final DEVE ser um relatório estruturado em Markdown, "
        "mapeando claramente as 3 URLs encontradas para cada pergunta original."
    ),
    expected_output=(
        "Um relatório Markdown mapeando cada pergunta-chave do plano "
        "a uma lista de 3 URLs de alta qualidade."
    ),
    agent=researcher,
    context=[task_planning],
    output_file="outputs/0_relatorio_urls.md" # Log
)

# --- Tarefa 3: Análise (Lote 1: Fundamentos) ---
task_analysis_lote1 = Task(
    description=(
        "Seu trabalho é de **Validação e Síntese** para o lote '1_Fundamentos'.\n"
        "1. Receba o relatório de URLs do Pesquisador (do contexto).\n"
        "2. Identifique as perguntas e URLs pertencentes APENAS a '1_Fundamentos'.\n"
        "3. Para CADA pergunta deste lote: \n"
        "   a. Use sua ferramenta de scraping (Firecrawl web scrape tool) para " # Usando scrape robusto
        "      ler o conteúdo de TODAS as 3 URLs fornecidas.\n"
        "   b. **AVALIE a relevância real** de cada fonte. \n"
        "   c. **COMPARE as fontes** e DESCARTE ativamente conteúdo irrelevante "
        "      (lixo, spam, 404, páginas de login).\n"
        "   d. **SINTETIZE uma resposta única** e coesa para a pergunta, "
        "      usando APENAS a informação validada das melhores fontes.\n"
        "   e. **CITE AS FONTES** que você realmente usou, ex: [Fonte: url.com].\n"
        "Seu output final é APENAS o texto sintetizado para este lote."
    ),
    expected_output=(
        "Um bloco de texto coeso em Markdown, contendo as respostas "
        "sintetizadas e citadas APENAS para o lote '1_Fundamentos'."
    ),
    agent=analyst,
    context=[task_research],
    output_file="outputs/0_analise_lote_1.md" # Log
)

# --- Tarefa 4: Compilação (Lote 1: Fundamentos) ---
task_compiling_lote1 = Task(
    description=(
        "Você é um robô de arquivamento. Sua missão é salvar o Lote 1.\n"
        "1. Receba o bloco de texto sintetizado (do contexto da Tarefa 3).\n"
        "2. **NÃO modifique o conteúdo.**\n"
        "3. Use sua 'File Write Tool' para salvar este conteúdo.\n" # Usando file write UTF-8
        "4. O caminho do arquivo DEVE ser: 'outputs/1_Fundamentos/fundamentos.md'\n"
        "   (Use 'outputs/1_Fundamentos/fundamentos.md' como 'filename')."
    ),
    expected_output=(
        "Uma string de confirmação indicando o sucesso e o caminho do "
        "arquivo salvo (ex: 'Conteúdo salvo com sucesso em: outputs/1_Fundamentos/fundamentos.md')."
    ),
    agent=compiler,
    context=[task_analysis_lote1]
)

# --- Tarefa 5: Análise (Lote 2: Contexto) ---
task_analysis_lote2 = Task(
    description=(
        "Mesma missão da Tarefa 3, mas agora para o **Lote 2 ('2_Contexto_e_Aplicacoes')**.\n"
        "1. Receba o relatório de URLs COMPLETO do Pesquisador (do contexto da Tarefa 2).\n"
        "2. Identifique as perguntas e URLs pertencentes APENAS a '2_Contexto...'.\n"
        "3. Para CADA pergunta deste lote, repita o processo de raspar, "
        "   **avaliar, comparar, descartar lixo e sintetizar** uma resposta única.\n"
        "4. Cite as fontes que você realmente usou.\n"
        "Seu output final é APENAS o texto sintetizado para este lote."
    ),
    expected_output=(
        "Um bloco de texto coeso em Markdown, contendo as respostas "
        "sintetizadas e citadas APENAS para o lote '2_Contexto_e_Aplicacoes'."
    ),
    agent=analyst,
    context=[task_research],
    output_file="outputs/0_analise_lote_2.md" # Log
)

# --- Tarefa 6: Compilação (Lote 2: Contexto) ---
task_compiling_lote2 = Task(
    description=(
        "Você é um robô de arquivamento. Sua missão é salvar o Lote 2.\n"
        "1. Receba o bloco de texto sintetizado (do contexto da Tarefa 5).\n"
        "2. **NÃO modifique o conteúdo.**\n"
        "3. Use sua 'File Write Tool' para salvar este conteúdo.\n"
        "4. O caminho do arquivo DEVE ser: 'outputs/2_Contexto_e_Aplicacoes/contexto.md'\n"
        "   (Use 'outputs/2_Contexto_e_Aplicacoes/contexto.md' como 'filename')."
    ),
    expected_output=(
        "Uma string de confirmação indicando o sucesso e o caminho do "
        "arquivo salvo (ex: 'Conteúdo salvo com sucesso em: outputs/2_Contexto_e_Aplicacoes/contexto.md')."
    ),
    agent=compiler,
    context=[task_analysis_lote2]
)

# --- Tarefas 7 e 8 (Placeholders da POC) ---
task_analysis_lote3 = Task(
    description="Placeholder - Tarefa de Análise Lote 3 (Não será usada na POC).",
    expected_output="N/A",
    agent=analyst,
    context=[task_research]
)

task_compiling_lote3 = Task(
    description="Placeholder - Tarefa de Compilação Lote 3 (Não será usada na POC).",
    expected_output="N/A",
    agent=compiler,
    context=[task_analysis_lote3]
)

print("--- [tasks.py] 8 Tarefas (Fluxo de POC com Lotes) carregadas. ---")