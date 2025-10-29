# tests/test_custom_tool.py
import os
import sys

# --- Configuração de Path ---
# Adiciona a pasta raiz do projeto (crewai-study-agent) ao path do Python
# para que possamos importar 'src'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR) # Sobe um nível (de 'tests' para 'crewai-study-agent')
sys.path.append(PROJECT_ROOT)
# --------------------------

# Agora o import de 'src.tools' vai funcionar
from src.tools.file_tools import file_write_tool 

print("Iniciando o teste da file_write_tool CUSTOMIZADA...")

# O arquivo de saída será salvo em 'outputs/teste_custom_tool.txt'
# O os.path.join(PROJECT_ROOT, ...) garante o caminho absoluto correto
meu_arquivo = os.path.join(PROJECT_ROOT, "outputs", "teste_custom_tool.txt")
meu_conteudo = "Olá, mundo! O teste da ferramenta customizada funcionou com acentos."

print(f"Salvando em: {meu_arquivo}")

try:
    # O .run() é adicionado automaticamente pelo decorador @tool
    resultado = file_write_tool.run(
        filename=meu_arquivo,
        content=meu_conteudo,
        overwrite=True
    )
    
    print(f"Resultado da ferramenta: {resultado}")
    
    # Teste de verificação (Lendo o arquivo de volta)
    print("Verificando o conteúdo do arquivo...")
    with open(meu_arquivo, 'r', encoding='utf-8') as f:
        conteudo_lido = f.read()
        if conteudo_lido == meu_conteudo:
            print(f"VERIFICAÇÃO SUCESSO: Conteúdo lido é IDÊNTICO.")
            print(f"Conteúdo: '{conteudo_lido}'")
        else:
            print(f"VERIFICAÇÃO FALHOU: Conteúdo lido: '{conteudo_lido}'")

except Exception as e:
    print(f"Ocorreu um erro ao testar a ferramenta: {e}")