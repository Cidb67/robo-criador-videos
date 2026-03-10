import google.generativeai as genai
import re
import os

def gerar_roteiro(tema, duracao="2min"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Usa o modelo gemini-1.0-pro (versão estável)
    model = genai.GenerativeModel('gemini-1.0-pro')
    
    duracao_map = {"1min": "80 palavras", "2min": "150 palavras", "3min": "220 palavras", "5min": "350 palavras"}
    limite = duracao_map.get(duracao, "150 palavras")
    
    prompt = f"""Crie um roteiro de video documentario de {duracao} ({limite}) sobre: {tema}

REGRAS:
- Maximo {limite}
- EXATAMENTE 3 cenas com [CENA: descricao em ingles para imagem]
- Tom: documentario National Geographic
- Texto em português do Brasil

FORMATO:
[CENA: descricao detalhada em ingles - cinematic, 4k, documentary]
Texto da narracao em português...

[CENA: descricao detalhada em ingles]
Texto da narracao...

[CENA: descricao detalhada em ingles]
Texto da narracao...

Inscreva-se para mais conteudo!
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Se falhar, tenta com outro modelo
        print(f"Erro com gemini-1.0-pro: {e}")
        print("Tentando com gemini-pro...")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text

def parsear_roteiro(roteiro):
    cenas = re.findall(r'\[CENA:\s*(.*?)\]', roteiro, re.IGNORECASE | re.DOTALL)
    texto_limpo = re.sub(r'\[CENA:.*?\]', '', roteiro, flags=re.DOTALL)
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    return cenas, texto_limpo