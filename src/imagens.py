import requests
import urllib.parse
import os
import time

def gerar_imagens_pollinations(cenas, pasta_temp="temp"):
    arquivos = []
    os.makedirs(pasta_temp, exist_ok=True)
    
    for i, cena in enumerate(cenas):
        print(f"   Imagem {i+1}/{len(cenas)}...", end=" ")
        
        # Simplifica a descrição para evitar erros
        descricao = cena.strip()[:300]
        if "cinematic" not in descricao.lower():
            descricao += ", cinematic, 4k, documentary"
        
        encoded = urllib.parse.quote(descricao)
        
        # Tenta com URL mais simples
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&seed={i+42}&nologo=true"
        
        # Tenta 3 vezes
        for tentativa in range(3):
            try:
                response = requests.get(url, timeout=60)
                
                if response.status_code == 200:
                    nome_arquivo = os.path.join(pasta_temp, f"imagem_{i:02d}.jpg")
                    with open(nome_arquivo, "wb") as f:
                        f.write(response.content)
                    
                    # Verifica se nao esta vazio
                    if os.path.getsize(nome_arquivo) > 1000:
                        arquivos.append(nome_arquivo)
                        print("OK")
                        time.sleep(2)
                        break
                    else:
                        os.remove(nome_arquivo)
                        raise Exception("Arquivo vazio")
                        
                elif response.status_code == 500:
                    print(f"Erro 500, tentativa {tentativa+1}/3...", end=" ")
                    time.sleep(5)
                    continue
                else:
                    response.raise_for_status()
                    
            except Exception as e:
                if tentativa == 2:  # Ultima tentativa
                    print(f"Falhou: {e}")
                    raise
                print(f"Tentativa {tentativa+1} falhou, tentando novamente...")
                time.sleep(3)
    
    return arquivos