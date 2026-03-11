import requests
import os

def gerar_imagens_pollinations(cenas, pasta_temp="temp"):
    """
    Baixa imagens da internet baseadas na descrição das cenas
    """
    arquivos = []
    os.makedirs(pasta_temp, exist_ok=True)
    
    for i, cena in enumerate(cenas):
        print(f"   Imagem {i+1}/{len(cenas)}...", end=" ")
        
        # Usa a descrição da cena para buscar imagem
        keyword = cena.replace(" ", ",")[:60]
        
        url = f"https://source.unsplash.com/1280x720/?{keyword}"
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                nome_arquivo = os.path.join(pasta_temp, f"imagem_{i:02d}.jpg")
                
                with open(nome_arquivo, "wb") as f:
                    f.write(response.content)
                
                if os.path.getsize(nome_arquivo) > 5000:
                    arquivos.append(nome_arquivo)
                    print("OK")
                else:
                    print("Imagem pequena, usando fallback")
                    arquivos.append(criar_imagem_padrao(pasta_temp, i))
            
            else:
                print("Erro download, usando fallback")
                arquivos.append(criar_imagem_padrao(pasta_temp, i))
        
        except Exception as e:
            print("Erro conexão, usando fallback")
            arquivos.append(criar_imagem_padrao(pasta_temp, i))
    
    return arquivos


def criar_imagem_padrao(pasta_temp, index):
    """
    Baixa uma imagem de fallback
    """
    url = f"https://via.placeholder.com/1280x720/333333/FFFFFF?text=Cena+{index+1}"
    
    try:
        response = requests.get(url, timeout=10)
        nome_arquivo = os.path.join(pasta_temp, f"imagem_{index:02d}.jpg")
        
        with open(nome_arquivo, "wb") as f:
            f.write(response.content)
        
        return nome_arquivo
    
    except:
        return os.path.join(pasta_temp, f"imagem_{index:02d}.jpg")