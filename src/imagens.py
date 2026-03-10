import requests
import os
import random

def gerar_imagens_pollinations(cenas, pasta_temp="temp"):
    """
    Busca imagens do Unsplash baseadas nas cenas do roteiro
    """
    arquivos = []
    os.makedirs(pasta_temp, exist_ok=True)
    
    # Palavras-chave para busca no Unsplash
    keywords = [
        "industrial revolution factory",
        "19th century steam engine", 
        "victorian era machinery",
        "historical manufacturing",
        "old factory workers",
        "steam locomotive vintage",
        "industrial machinery",
        "factory smokestacks",
        "vintage workshop",
        "historical technology"
    ]
    
    for i, cena in enumerate(cenas):
        print(f"   Imagem {i+1}/{len(cenas)}...", end=" ")
        
        # Escolhe uma palavra-chave aleatoria
        keyword = random.choice(keywords)
        
        # URL do Unsplash Source (gratuito)
        url = f"https://source.unsplash.com/1280x720/?{keyword.replace(' ', ',')}"
        
        try:
            # Faz download da imagem
            response = requests.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            nome_arquivo = os.path.join(pasta_temp, f"imagem_{i:02d}.jpg")
            with open(nome_arquivo, "wb") as f:
                f.write(response.content)
            
            # Verifica se a imagem é válida
            if os.path.getsize(nome_arquivo) > 5000:
                arquivos.append(nome_arquivo)
                print("OK")
            else:
                print("Imagem muito pequena, usando placeholder")
                criar_placeholder(nome_arquivo)
                arquivos.append(nome_arquivo)
                
        except Exception as e:
            print(f"Erro: {e}, criando placeholder")
            nome_arquivo = os.path.join(pasta_temp, f"imagem_{i:02d}.jpg")
            criar_placeholder(nome_arquivo)
            arquivos.append(nome_arquivo)
    
    return arquivos

def criar_placeholder(caminho):
    """
    Cria uma imagem placeholder simples se o download falhar
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Cria imagem cinza
        img = Image.new('RGB', (1280, 720), color=(50, 50, 50))
        draw = ImageDraw.Draw(img)
        
        # Adiciona texto
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        text = "Imagem Indisponivel"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1280 - text_width) // 2
        y = (720 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        img.save(caminho)
        
    except Exception as e:
        # Se PIL nao funcionar, cria arquivo vazio
        with open(caminho, "wb") as f:
            f.write(b"")