# test_analyst.py

import sys
sys.path.append('src')

from crewai import Crew, Process, Task

# Importe o LLM, o Analista e o Compilador
try:
    from src.llm_config import llm
    from src.agents import analyst, compiler
    print("--- [TESTE] Agentes e LLM importados com sucesso. ---")
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se que seus arquivos em 'src/' estão corretos.")
    sys.exit(1)

# --- 1. Defina o Tópico ---
topic = "Agentes de IA na industria textil"

# --- 2. Defina os Dados Mock (LISTA DE URLS) ---
# Usando a lista JSON limpa do log
mock_url_list = [
    {"url": "https://cloud.google.com/discover/what-are-ai-agents?hl=pt-BR"},
    {"url": "https://aws.amazon.com/pt/what-is/ai-agents/"},
    {"url": "https://www.iweaver.ai/pt/guide/what-is-an-ai-agent-definition-function-and-how-they-work/"},
    {"url": "https://www.oracle.com/br/artificial-intelligence/ai-agents/"},
    {"url": "https://brainpod.ai/pt/o-que-e-um-agente-composto-em-ia-explorando-os-componentes-e-tipos-de-agentes-em-inteligencia-artificial/"},
    # Adicionando mais algumas para um teste robusto (o resto da lista)
    {"url": "https://latenode.com/pt-br/blog/what-is-ai-agent-the-complete-guide-to-artificial-intelligence-agents"},
    {"url": "https://www.datacamp.com/pt/blog/types-of-ai-agents"},
    {"url": "https://botpress.com/pt/blog/types-of-ai-agents"},
    {"url": "https://www.ibm.com/br-pt/think/topics/ai-agents"},
    {"url": "https://brainpod.ai/pt/explorando-tipos-de-agentes-inteligentes-em-caracteristicas-de-ia-exemplos-e-seu-papel-na-inteligencia-artificial/"}
    # Vamos parar em 10 URLs por enquanto para um teste rápido
]

# --- 3. Crie Tarefas de Teste DINAMICAMENTE ---
def run_test_crew():
    """Função para encapsular e rodar o crew de teste."""
    
    analysis_tasks = []
    
    # LIMITADOR DE TESTE: Mude "len(mock_url_list)" para um número menor (ex: 5) para testes mais rápidos
    urls_to_test = mock_url_list[:5] # Vamos testar apenas as 5 primeiras
    
    print(f"--- [TESTE] Criando {len(urls_to_test)} tarefas de análise... ---")

    # Criar uma tarefa dinamicamente PARA CADA URL
    for url_data in urls_to_test:
        url = url_data['url']
        
        # ***** MUDANÇA PRINCIPAL AQUI (v3 - Analista mais robusto) *****
        task = Task(
            description=(
                f"1. Receber o tópico original '{topic}'.\n"
                f"2. Receber UMA ÚNICA URL para analisar: {url}\n"
                "3. Executar a análise (scrape, filtro, síntese) para ESTA URL.\n"
                "   (Lembre-se: Use a ferramenta 'Firecrawl web scrape tool').\n"
                "   (Lembre-se: Aplique os FILTROS DE QUALIDADE - descarte se for irrelevante, lixo, ou erro).\n"
                "   (Lembre-se: Sintetize o conteúdo VÁLIDO, mantendo a URL de origem).\n"
                "   **DIRETRIZES IMPORTANTES PARA A SÍNTESE:**\n"
                "   - Seja CONCISO. Foque APENAS na informaçãa essencial.\n"
                "   - **NUNCA repita** frases ou parágrafos.\n"
                "   - Se o conteúdo raspado for muito longo ou confuso, sumarize apenas os pontos principais.\n"
                "   - **Limite sua resposta final (a síntese) a um máximo de 500 palavras.**" # Adiciona um limite prático
            ),
            expected_output=(
                f"Um bloco de texto CONCISO (máximo 500 palavras) com o conhecimento VÁLIDO e RELEVANTE extraído da URL {url}, "
                "incluindo a URL de origem. A resposta NÃO DEVE conter repetições.\n"
                "Se a URL falhar, for irrelevante ou o conteúdo for lixo (ex: apenas menus, cookies, repetições), "
                "retorne uma nota clara, ex: 'FALHA: URL [url] irrelevante/lixo/falha.'"
            ),
            agent=analyst
            )
        analysis_tasks.append(task)

# --- NOVO TRECHO AQUI ---
    # Vamos pré-calcular o nome da pasta que queremos
    # Isso torna a instrução para o agente muito mais clara
    topic_folder = topic.replace(' ', '_') # Resultado: "Agentes_de_IA_na_industria_textil"
    # -------------------------

    # Tarefa de compilação que depende de TODAS as tarefas de análise
    # ***** MUDANÇA PRINCIPAL AQUI *****
    task_compiling_test = Task(
        description=(
            "1. Receber uma LISTA de conteúdos sintetizados (do contexto de todas as tarefas de análise anteriores).\n"
            f"2. Receber o tópico original: '{topic}'.\n"
            f"3. O nome da pasta principal OBRIGATÓRIA para salvar todos os arquivos é: '{topic_folder}'.\n"
            f"4. O caminho base COMPLETO para todos os arquivos deve ser 'outputs/{topic_folder}/'.\n"
            "5. **Verificação de Conteúdo (CRÍTICO):** Analise a LISTA de resultados das tarefas anteriores.\n"
            "   - **CASO A (Sucesso):** Se a lista contiver QUALQUER conteúdo VÁLIDO (qualquer texto que NÃO seja 'FALHA' ou 'irrelevante'), "
            "     você DEVE organizar esse conteúdo nas subpastas ('1_Fundamentos', '2_Contexto_e_Aplicacoes', etc.) e "
            "     usar a 'File Write Tool' para salvar os arquivos .md."
            f"     Exemplo de caminho: 'outputs/{topic_folder}/1_Fundamentos/nome_do_arquivo.md'.\n"
            "   - **CASO B (Falha Total):** Se a LISTA contiver APENAS mensagens de 'FALHA', 'irrelevante', ou estiver vazia, "
            "     você DEVE pular a criação de subpastas e usar a 'File Write Tool' UMA ÚNICA VEZ para salvar um arquivo de log de falha.\n"
            f"   - **Ação OBRIGATÓRIA do CASO B:** Chamar a 'File Write Tool' com:\n"
            f"     - filename: 'outputs/{topic_folder}/README_FALHA.md'\n"
            "     - content: 'Relatório de Falha: A pesquisa sobre o tópico \"{topic}\" falhou. Nenhuma informação relevante foi extraída das URLs fornecidas.'"
        ),
        expected_output=(
            "Um relatório de status final. \n"
            "Se SUCESSO (Caso A), liste os arquivos .md criados DENTRO de 'outputs/{topic_folder}/'.\n"
            "Se FALHA (Caso B), confirme que o arquivo 'outputs/{topic_folder}/README_FALHA.md' foi salvo."
        ),
        agent=compiler,
        context=analysis_tasks # <-- Depende de TODAS as tarefas da lista
    )
    
    # --- 4. Crie um Crew de Teste ---
    all_tasks = analysis_tasks + [task_compiling_test]
    
    test_crew = Crew(
        agents=[analyst, compiler],
        tasks=all_tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # --- 5. Execute o Teste ---
    
    print(f"--- [TESTE] Iniciando Crew de Análise e Compilação para o tópico: '{topic}' ---")
    
    try:
        result = test_crew.kickoff() 
        
        print("\n--- [TESTE] Execução Finalizada ---")
        print(result)
        print(f"\nVerifique a pasta 'outputs/{topic.replace(' ', '_')}/' para os arquivos.")
        
    except Exception as e:
        print(f"\nOcorreu um erro durante a execução do crew de teste: {e}")
        print("Verifique suas chaves de API (GEMINI, FIRECRAWL) no .env e a conexão.")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    run_test_crew()