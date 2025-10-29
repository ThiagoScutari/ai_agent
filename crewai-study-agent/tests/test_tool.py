# src/tests/test_tool.py

from crewai_tools import FileWriterTool
import os

print("Iniciando o teste da FileWriterTool...")

# Instanciar a ferramenta
file_writer = FileWriterTool()

meu_arquivo_relativo = os.path.join("outputs", "teste_ferramenta.txt")
meu_conteudo = "Olá, mundo! O teste da FileWriterTool funcionou com sucesso."

# Usar o método .run() da ferramenta
try:
    # --- CORREÇÃO 3: Adicionando o argumento 'overwrite' ---
    #
    # O novo erro "KeyError: 'overwrite'" foi claro.
    # Vamos adicionar 'overwrite=True' para permitir que o script
    # sobrescreva o arquivo em testes futuros.
    resultado = file_writer.run(
        filename=meu_arquivo_relativo,
        content=meu_conteudo,
        overwrite=True  # <-- AQUI ESTÁ A NOVA CORREÇÃO
    )

    print(f"Resultado da ferramenta: {resultado}")
    print(f"Verifique se o arquivo '{meu_arquivo_relativo}' foi criado com o conteúdo correto.")

except Exception as e:
    print(f"Ocorreu um erro ao testar a ferramenta: {e}")