import google.generativeai as genai
import re
import os

def gerar_roteiro(tema, duracao="2min"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    duracao_map = {"1min": "80 palavras", "2min": "150 palavras", "3min": "220 palavras", "5min": "350 palavras"}
    limite = duracao_map.get(duracao, "150 palavras")
    
    prompt = f"""Crie um roteiro de video documentario de {duracao} ({limite}) sobre: {tema}

REGRAS:
- Maximo {limite}
- EXATAMENTE 3 cenas com [CENA: descricao em ingles para imagem]
- Tom: documentario National Geographic
- Texto em portugues do Brasil

FORMATO:
[CENA: descricao detalhada em ingles - cinematic, 4k, documentary]
Texto da narracao em portugues...

[CENA: descricao detalhada em ingles]
Texto da narracao...

[CENA: descricao detalhada em ingles]
Texto da narracao...

Inscreva-se para mais conteudo!
"""
    
    response = model.generate_content(prompt)
    return response.text

def parsear_roteiro(roteiro):
    cenas = re.findall(r'\[CENA:\s*(.*?)\]', roteiro, re.IGNORECASE | re.DOTALL)
    texto_limpo = re.sub(r'\[CENA:.*?\]', '', roteiro, flags=re.DOTALL)
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    return cenas, texto_limpo