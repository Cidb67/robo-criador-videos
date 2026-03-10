import requests
import re
import os
import json

def gerar_roteiro(tema, duracao="2min"):
    api_key = os.getenv("GEMINI_API_KEY")
    
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

    # Usa a API REST diretamente
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        texto = result["candidates"][0]["content"]["parts"][0]["text"]
        return texto
        
    except Exception as e:
        print(f"Erro na API: {e}")
        print(f"Resposta: {response.text if 'response' in locals() else 'N/A'}")
        raise

def parsear_roteiro(roteiro):
    cenas = re.findall(r'\[CENA:\s*(.*?)\]', roteiro, re.IGNORECASE | re.DOTALL)
    texto_limpo = re.sub(r'\[CENA:.*?\]', '', roteiro, flags=re.DOTALL)
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    return cenas, texto_limpo