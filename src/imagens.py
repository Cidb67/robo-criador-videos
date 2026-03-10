import requests
import urllib.parse
import os
import time

def gerar_imagens_pollinations(cenas, pasta_temp="temp"):
    arquivos = []
    os.makedirs(pasta_temp, exist_ok=True)
    
    for i, cena in enumerate(cenas):
        print(f"   Imagem {i+1}/{len(cenas)}...", end=" ")
        
        descricao = cena.strip()[:400]
        if "cinematic" not in descricao.lower():
            descricao += ", cinematic, 4k, documentary style"
        
        encoded = urllib.parse.quote(descricao)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&seed={i+42}&nologo=true"
        
        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            
            nome_arquivo = os.path.join(pasta_temp, f"imagem_{i:02d}.jpg")
            with open(nome_arquivo, "wb") as f:
                f.write(response.content)
            
            arquivos.append(nome_arquivo)
            print("OK")
            time.sleep(1.5)
            
        except Exception as e:
            print(f"Erro: {e}")
            raise
    
    return arquivos