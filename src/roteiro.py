import requests
import re
import os
import json

def gerar_roteiro(tema, duracao="2min"):
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY nao configurado")
    
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

    # Usa API da Groq
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        texto = result["choices"][0]["message"]["content"]
        return texto
        
    except Exception as e:
        print(f"Erro na API Groq: {e}")
        if 'response' in locals():
            print(f"Resposta: {response.text}")
        raise

def parsear_roteiro(roteiro):
    cenas = re.findall(r'\[CENA:\s*(.*?)\]', roteiro, re.IGNORECASE | re.DOTALL)
    texto_limpo = re.sub(r'\[CENA:.*?\]', '', roteiro, flags=re.DOTALL)
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    return cenas, texto_limpo