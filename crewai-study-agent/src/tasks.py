# src/tasks.py

from crewai import Task

# Importar os agentes da Fase 4
from src.agents import planner, researcher, analyst, compiler

# --- Definição das Tarefas ---

# Tarefa 1: Criar o Plano de Pesquisa (Sem Mudanças)
task_planning = Task(
    description=(
        "1. Analisar o tópico de entrada: '{topic}'.\n"
        "2. Gerar um plano de pesquisa detalhado para este tópico.\n"
        "3. O plano DEVE ser estruturado em 3 seções, conforme o "
        "planejamento original do projeto:\n"
        "    a) 1_Fundamentos (Conceitos-chave, definições, 80% do conhecimento)\n"
        "    b) 2_Contexto_e_Aplicacoes (Exemplos práticos, casos de uso, ferramentas)\n"
        "    c) 3_Aprofundamento_e_Nuvem (Tópicos avançados, o futuro, os 20%)\n"
        "4. Para CADA seção, definir 3-5 subtópicos claros.\n"
        "5. Para CADA subtópico, formular 2-3 perguntas de pesquisa específicas "
        "que o pesquisador deve responder.\n"
        "6. O output final deve ser este plano estruturado."
    ),
    expected_output=(
        "Um plano de pesquisa abrangente em formato de texto, "
        "listando todos os subtópicos e perguntas-chave, "
        "perfeitamente organizado nas 3 seções."
    ),
    agent=planner,
    output_file="logs/1_plano_de_pesquisa.md" # Salva o plano para debug
)

# Tarefa 2: Realizar a Pesquisa na Web (Sem Mudanças)
task_research = Task(
    description=(
        "1. Usar o plano de pesquisa detalhado fornecido (do contexto) como guia OBRIGATÓRIO.\n"
        "2. **Para CADA pergunta-chave** listada no plano, você DEVE usar as ferramentas de busca "
        "(Serper e/ou DuckDuckGo) para encontrar fontes relevantes e de alta qualidade.\n"
        "3. Seja EXAUSTIVO. Tente encontrar pelo menos 2-3 fontes por pergunta-chave, se possível.\n"
        "4. Priorize fontes confiáveis: documentação oficial, artigos acadêmicos, "
        "blogs de especialistas, notícias de respeitáveis.\n"
        "5. **CRÍTICO:** O output final DEVE ser uma lista CLARAMENTE ESTRUTURADA em Markdown, "
        "agrupando as URLs encontradas sob cada pergunta-chave original do plano."
    ),
    expected_output=(
        "Um relatório em formato Markdown contendo:\n"
        "- Para cada SUBTÓPICO do plano:\n"
        "  - Para cada PERGUNTA-CHAVE desse subtópico:\n"
        "    - Uma lista (bullet points) das URLs relevantes encontradas para ESSA pergunta.\n"
        "Exemplo:\n"
        "## 1.1. Definição e Tipos de Agentes de IA\n"
        "### Pergunta: O que são agentes de IA...?\n"
        "* URL 1\n"
        "* URL 2\n"
        "### Pergunta: Quais são as diferentes taxonomias...?\n"
        "* URL 3\n"
        "\nSe NENHUMA URL for encontrada para uma pergunta específica, indicar claramente: '* Nenhuma fonte encontrada.'\n"
        "Este formato estruturado é ESSENCIAL para o próximo agente."
    ),
    agent=researcher,
    context=[task_planning], # Depende da Tarefa 1
    output_file="logs/2_relatorio_urls.md" # Salva as URLs para debug
)


# --- TAREFA 3 (REESCRITA) ---
# Tarefa 3: Analisar e SINTETIZAR o Conteúdo
task_analysis = Task(
    description=(
        "1. Receber o tópico original '{topic}' e o relatório ESTRUTURADO de URLs (do contexto).\n"
        "2. Seu trabalho é iterar **pergunta por pergunta** pelo relatório de URLs.\n"
        "3. Para CADA PERGUNTA-CHAVE no relatório:\n"
        "   a. Pegue a lista de URLs associada a ela (ex: * URL 1, * URL 2).\n"
        "   b. Se for '* Nenhuma fonte encontrada', pule para a próxima pergunta.\n"
        "   c. Use a ferramenta 'Firecrawl web scrape tool' para raspar o conteúdo de CADA UMA dessas URLs.\n"
        "   d. **SÍNTESE CRÍTICA:** Analise o conteúdo raspado (de todas as URLs daquela pergunta) e "
        "      use seu LLM para escrever uma **resposta única, coesa e concisa** (máx 500 palavras) "
        "      que responda DIRETAMENTE à pergunta-chave.\n"
        "   e. **FILTRAGEM:** Aplique os filtros de qualidade. Se o conteúdo raspado for "
        "      irrelevante, lixo (spam, repetições) ou erro 404, DESCARTE-O. Se nenhuma "
        "      fonte válida for encontrada para uma pergunta, anote: "
        "      'Nenhuma informação relevante encontrada.'\n"
        "   f. **CITAÇÃO:** No final da sua resposta sintetizada, inclua as URLs de "
        "      origem que você usou, ex: `(Fontes: URL 1, URL 2)`.\n"
        "4. O seu output final DEVE ser um **único documento Markdown**, mantendo a "
        "estrutura de tópicos original, mas substituindo as *listas de URLs* pelas "
        "*respostas sintetizadas*."
    ),
    expected_output=(
        "Um relatório Markdown finalizado (O 'Relatório de Conhecimento'), pronto "
        "para ser 'fatiado' e salvo pelo Compilador. O formato deve ser:\n"
        "## 1.1. Definição e Tipos de Agentes de IA\n"
        "### Pergunta: O que são agentes de IA...?\n"
        "Uma agente de IA é uma entidade que percebe seu ambiente... (Fontes: URL 1, URL 2)\n"
        "### Pergunta: Quais são as diferentes taxonomias...?\n"
        "Os principais tipos são: agentes reativos simples, ... (Fontes: URL 3)\n"
        "\n"
        "## 1.2. Próximo Subtópico\n"
        "..."
    ),
    agent=analyst,
    context=[task_research], # Depende da Tarefa 2
    output_file="logs/3_relatorio_sintetizado.md" # Salva o .md final para debug
)


# --- TAREFA 4 (REESCRITA) ---
# Tarefa 4: Fatiar e Salvar os Arquivos Finais
task_compiling = Task(
    description=(
        "1. Receber o 'Relatório de Conhecimento' **JÁ SINTETIZADO** (do contexto da tarefa de análise).\n"
        "2. Receber o tópico original: '{topic}'.\n"
        "3. **NÃO REESCREVER OU SINTETIZAR NADA.** Seu trabalho é puramente processual: fatiar o relatório e salvar os arquivos.\n"
        "4. Criar um nome de pasta principal baseado no tópico, substituindo espaços e "
        "   caracteres especiais por underscores (ex: 'Agentes_de_IA_na_industria_textil'). "
        "   O caminho base será 'outputs/NOME_DA_PASTA/'.\n"
        "5. Ler o relatório Markdown e 'fatiá-lo' por subtópico. Cada subtópico "
        "   começa com um título Nível 2 (ex: `## 1.1. ...`, `## 1.2. ...`, `## 2.1. ...`).\n"
        "6. Para CADA subtópico encontrado:\n"
        "   a. Determinar a pasta de categoria (ex: '1_Fundamentos', '2_Contexto_e_Aplicacoes', '3_Aprofundamento_e_Nuvem') "
        "      baseado no número do título (ex: `## 1.1` vai para `1_Fundamentos/`, `## 3.2` vai para `3_Aprofundamento_e_Nuvem/`).\n"
        "   b. Criar um nome de arquivo .md para esse subtópico (ex: `1_1_Definicao_e_Tipos.md`).\n"
        "   c. O conteúdo do arquivo será *todo* o texto sob aquele título (incluindo as perguntas e respostas sintetizadas) até o próximo título de subtópico.\n"
        "   d. Montar o caminho completo, ex: `outputs/Agentes_de_IA.../1_Fundamentos/1_1_Definicao_e_Tipos.md`\n"
        "   e. Usar a 'File Write Tool' para salvar esse conteúdo nesse caminho.\n"
        "7. Repetir para todos os subtópicos.\n"
        "8. Se o conteúdo recebido for vazio ou contiver apenas falhas, salvar um único "
        "   arquivo 'README.md' na pasta principal (ex: 'outputs/Nome_Topico/README.md') "
        "   explicando que a pesquisa não encontrou conteúdo relevante."
    ),
    expected_output=(
        "Um relatório de status final confirmando o sucesso da operação e listando "
        "a estrutura de pastas e os arquivos .md que foram criados e salvos no disco."
    ),
    agent=compiler,
    context=[task_analysis] # Depende da Tarefa 3
    # Não há output_file aqui, pois o agente usa a FileWriteTool
)

print("--- [tasks.py] 4 Tarefas (v4 - Fluxo de Síntese Refinado) criadas com sucesso. ---")