import os
from dotenv import load_dotenv
from google import genai

# --- Lógica para encontrar o .env na raiz do mono-repo ---
load_dotenv()

# __file__ é o caminho deste arquivo (.../CREW-AI-PROJECT-7/src/llm_config.py)
project_root = os.path.dirname(     # 1º dirname -> .../CREW-AI-PROJECT-7/src/
    os.path.dirname(                # 2º dirname -> .../CREW-AI-PROJECT-7/
        os.path.dirname(            # 3º dirname -> .../ai_agent/  (Esta é a raiz)
            os.path.abspath(__file__)
            )
        )
    )
dotenv_path = os.path.join(project_root, '.env')

if not dotenv_path:
    print('Chave não encontrada em: ', {dotenv_path})

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

def test(text)-> None:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text
    )
    return response.text

teste = test("Me diga como um IA funciona em poucas paralavras")

print(teste)


