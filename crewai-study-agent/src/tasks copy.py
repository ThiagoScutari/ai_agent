# src/tasks.py

from crewai import Task

# Importar os agentes da Fase 2
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
)

# --- TAREFA ATUALIZADA ---
# Tarefa 2: Realizar a Pesquisa na Web (Instruções e Output Reforçados)
task_research = Task(
    description=(
        "1. Usar o plano de pesquisa detalhado fornecido (do contexto) como guia OBRIGATÓRIO.\n"
        "2. **Para CADA pergunta-chave** listada no plano, você DEVE usar as ferramentas de busca "
        "(Serper e/ou DuckDuckGo) para encontrar fontes relevantes e de alta qualidade.\n"
        "3. Seja EXAUSTIVO. Tente encontrar pelo menos 2-3 fontes por pergunta-chave, se possível.\n"
        "4. Priorize fontes confiáveis: documentação oficial, artigos acadêmicos, "
        "blogs de especialistas, notícias de fontes respeitáveis.\n"
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
        "* URL 4\n"
        "\nSe NENHUMA URL for encontrada para uma pergunta específica, indicar claramente: '* Nenhuma fonte encontrada.'\n"
        "Este formato estruturado é ESSENCIAL para o próximo agente."
    ),
    agent=researcher,
    context=[task_planning] # Depende da Tarefa 1
)


# Tarefa 3: Analisar o Conteúdo das Fontes (Versão anterior, já robusta)
task_analysis = Task(
    description=(
        "1. Receber o tópico original '{topic}' e a lista ESTRUTURADA de URLs (do contexto).\n"
        "2. Para CADA URL listada no relatório do pesquisador:\n"
        "   a) Usar a ferramenta de 'scrape' para ler o conteúdo da página.\n"
        "   b) **FILTRO DE QUALIDADE (CRÍTICO):** Antes de analisar, avaliar o texto:\n"
        "      i. **Verificação de Relevância:** O texto *DEVE* ser sobre o tópico '{topic}' e responder à pergunta-chave associada. "
        "         Se for um texto genérico (ex: 'Google Cloud Security', 'Página de Login', 'Erro 404', 'Aviso de Cookies') "
        "         ou claramente não relacionado, **DESCARTE O CONTEÚDO** desta URL e anote-o como 'irrelevante'.\n"
        "      ii. **Verificação de Lixo (Spam):** Se o texto parecer ser um loop de palavras repetitivas "
        "          (como o 'Google Cloud' que vimos) ou spam, **DESCARTE O CONTEÚDO** como 'lixo'.\n"
        "   c) **Análise (Se Passar no Filtro):** Se o texto for relevante e limpo: "
        "      i. Extrair as informações que respondem à pergunta-chave associada.\n"
        "      ii. Sintetizar a informação em blocos de texto claros e concisos, MANTENDO A REFERÊNCIA à URL original.\n"
        "3. Ignorar informações irrelevantes (anúncios, menus, etc.) durante a síntese.\n"
        "4. O output final deve ser um único documento de texto contendo todos os "
        "blocos de conhecimento *válidos* sintetizados, agrupados pela pergunta-chave e subtópico originais, e incluindo a URL de origem de cada bloco."
    ),
    expected_output=(
        "Um documento de texto com todo o conhecimento VÁLIDO e RELEVANTE extraído, "
        "sintetizado e organizado por subtópico e pergunta-chave, com cada bloco de informação "
        "claramente associado à sua URL de origem."
    ),
    agent=analyst,
    context=[task_research] # Depende da Tarefa 2
)


# Tarefa 4: Compilar e Salvar os Arquivos Finais (Versão anterior, já robusta)
task_compiling = Task(
    description=(
        "1. Receber o conteúdo sintetizado (do contexto da tarefa de análise), que inclui URLs de origem.\n"
        "2. Receber o tópico original: '{topic}'.\n"
        "3. **Verificação de Conteúdo:** Se o conteúdo recebido for vazio ou "
        "   contiver apenas notas de 'irrelevante' ou 'lixo', pule para a etapa 8.\n"
        "4. Organizar o conteúdo VÁLIDO de acordo com a estrutura do projeto: "
        "   '1_Fundamentos', '2_Contexto_e_Aplicacoes', '3_Aprofundamento_e_Nuvem'.\n"
        "5. Formatar o conteúdo em Markdown (.md), com títulos, listas e, crucialmente, "
        "   **links para as URLs de origem** fornecidas pelo Analista.\n"
        "6. Criar um nome de pasta principal baseado no tópico, "
        "   substituindo espaços por underscores (ex: 'Inteligencia_Artificial').\n"
        "7. Usar a 'File Write Tool' para salvar CADA subtópico (agrupando as respostas de suas perguntas) como um "
        "   arquivo .md separado dentro da sua respectiva subpasta.\n"
        "   Exemplo: 'outputs/Inteligencia_Artificial/1_Fundamentos/1_1_Definicao_e_Tipos.md'\n"
        "8. Se nenhum conteúdo válido foi encontrado (etapa 3), salvar um único "
        "   arquivo 'README.md' na pasta principal (ex: 'outputs/Nome_Topico/README.md') "
        "   explicando que a pesquisa não encontrou conteúdo relevante.\n"
        "9. O output final deve ser um relatório de status confirmando o que foi salvo."
    ),
    expected_output=(
        "Um relatório de status final confirmando o sucesso da operação e listando "
        "a estrutura de pastas e arquivos criada."
    ),
    agent=compiler,
    context=[task_analysis] # Depende da Tarefa 3
)


print("--- [tasks] 4 Tarefas (v3, com Pesquisador reforçado) criadas com sucesso. ---")