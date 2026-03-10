import requests
import os
import random

def gerar_imagens_pollinations(cenas, pasta_temp="temp"):
    """
    Busca imagens do Unsplash
    """
    arquivos = []
    os.makedirs(pasta_temp, exist_ok=True)
    
    # Palavras-chave para busca
    keywords = [
        "industrial revolution",
        "steam engine",
        "factory vintage",
        "19th century",
        "machinery old"
    ]
    
    for i, cena in enumerate(cenas):
        print(f"   Imagem {i+1}/{len(cenas)}...", end=" ")
        
        keyword = random.choice(keywords)
        url = f"https://source.unsplash.com/1280x720/?{keyword.replace(' ', ',')}"
        
        try:
            response = requests.get(url, timeout=30, allow_redirects=True)
            
            if response.status_code == 200:
                nome_arquivo = os.path.join(pasta_temp, f"imagem_{i:02d}.jpg")
                with open(nome_arquivo, "wb") as f:
                    f.write(response.content)
                
                if os.path.getsize(nome_arquivo) > 5000:
                    arquivos.append(nome_arquivo)
                    print("OK")
                else:
                    print("pequena, usando padrao")
                    arquivos.append(criar_imagem_padrao(pasta_temp, i))
            else:
                print(f"erro {response.status_code}, usando padrao")
                arquivos.append(criar_imagem_padrao(pasta_temp, i))
                
        except Exception as e:
            print(f"erro, usando padrao")
            arquivos.append(criar_imagem_padrao(pasta_temp, i))
    
    return arquivos

def criar_imagem_padrao(pasta_temp, index):
    """
    Cria uma imagem simples sem usar PIL
    """
    # Baixa uma imagem padrao do placeholder.com
    url = f"https://via.placeholder.com/1280x720/333333/FFFFFF?text=Imagem+{index+1}"
    
    try:
        response = requests.get(url, timeout=10)
        nome_arquivo = os.path.join(pasta_temp, f"imagem_{index:02d}.jpg")
        with open(nome_arquivo, "wb") as f:
            f.write(response.content)
        return nome_arquivo
    except:
        # Se tudo falhar, retorna o caminho mesmo assim
        # O MoviePy vai lidar com isso
        return os.path.join(pasta_temp, f"imagem_{index:02d}.jpg")