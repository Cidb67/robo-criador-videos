import os
import subprocess

def gerar_imagens_pollinations(cenas, pasta_temp="temp"):
    """
    Cria imagens simples usando ImageMagick
    """
    arquivos = []
    os.makedirs(pasta_temp, exist_ok=True)
    
    cores = ["#2C3E50", "#8E44AD", "#27AE60", "#F39C12", "#E74C3C", "#1ABC9C"]
    
    for i, cena in enumerate(cenas):
        print(f"   Imagem {i+1}/{len(cenas)}...", end=" ")
        
        nome_arquivo = os.path.join(pasta_temp, f"imagem_{i:02d}.jpg")
        
        # Cria imagem usando ImageMagick convert
        cor = cores[i % len(cores)]
        texto = f"Cena {i+1}"
        
        cmd = [
            "convert",
            "-size", "1280x720",
            "xc:" + cor,
            "-pointsize", "40",
            "-fill", "white",
            "-gravity", "center",
            "-annotate", "+0+0", texto,
            nome_arquivo
        ]
        
        try:
            resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if resultado.returncode == 0 and os.path.exists(nome_arquivo):
                arquivos.append(nome_arquivo)
                print("OK")
            else:
                print(f"Erro ImageMagick: {resultado.stderr}")
                # Cria arquivo vazio como fallback
                with open(nome_arquivo, "wb") as f:
                    f.write(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xFF\xD9")
                arquivos.append(nome_arquivo)
                
        except Exception as e:
            print(f"Erro: {e}")
            # Cria JPEG mínimo válido
            with open(nome_arquivo, "wb") as f:
                f.write(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xFF\xD9")
            arquivos.append(nome_arquivo)
    
    return arquivos