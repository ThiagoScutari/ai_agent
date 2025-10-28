# src/tools/file_tools.py

import os
from crewai.tools import tool # Importando o decorador '@tool'

@tool("File Write Tool")
def file_write_tool(filename: str, content: str, overwrite: bool = False):
    """
    Uma ferramenta para escrever 'content' (texto) em um 'filename' (arquivo).
    'filename' deve ser o caminho completo, ex: 'outputs/meu_arquivo.md'.
    'content' é o texto que você quer salvar.
    'overwrite' (bool) define se deve sobrescrever o arquivo (default: False).
    Esta ferramenta FORÇA o encoding UTF-8 para salvar acentos corretamente.
    """

    # Checagem de segurança para 'overwrite'
    should_overwrite = str(overwrite).lower() == 'true'

    if not should_overwrite and os.path.exists(filename):
        return f"Erro: O arquivo {filename} já existe. Permita 'overwrite=True' para sobrescrevê-lo."

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f: # Força UTF-8
            f.write(content)
        return f"Conteúdo salvo com sucesso em: {filename}"
    except Exception as e:
        return f"Erro ao salvar o arquivo {filename}: {str(e)}"

# Adicionar um print para confirmar o carregamento (opcional, mas útil)
print("--- [file_tools.py] Ferramenta file_write_tool (UTF-8) carregada. ---")