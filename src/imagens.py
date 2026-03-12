import os
import requests
import numpy as np
import imageio.v2 as imageio

def gerar_imagens_pollinations(cenas, pasta_temp="temp"):
    """
    Tenta baixar imagens da internet.
    Se falhar, cria imagens locais válidas em PNG.
    """
    arquivos = []
    os.makedirs(pasta_temp, exist_ok=True)

    for i, cena in enumerate(cenas):
        print(f"   Imagem {i+1}/{len(cenas)}...", end=" ")

        keyword = cena.replace(" ", ",")[:60]
        nome_arquivo = os.path.join(pasta_temp, f"imagem_{i:02d}.png")

        # Fonte aleatória de imagem
        url = f"https://picsum.photos/seed/{i+1}/1280/720"

        try:
            response = requests.get(url, timeout=20)

            if response.status_code == 200 and len(response.content) > 5000:
                with open(nome_arquivo, "wb") as f:
                    f.write(response.content)

                if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 5000:
                    arquivos.append(nome_arquivo)
                    print("OK")
                else:
                    print("falhou, criando fallback local")
                    arquivos.append(criar_imagem_padrao(nome_arquivo, i))
            else:
                print("erro download, criando fallback local")
                arquivos.append(criar_imagem_padrao(nome_arquivo, i))

        except Exception:
            print("erro conexão, criando fallback local")
            arquivos.append(criar_imagem_padrao(nome_arquivo, i))

    return arquivos


def criar_imagem_padrao(caminho_arquivo, index):
    """
    Cria uma imagem PNG local simples e válida.
    """
    cores = [
        (44, 62, 80),
        (142, 68, 173),
        (39, 174, 96),
        (243, 156, 18),
        (231, 76, 60),
        (26, 188, 156),
    ]

    cor = cores[index % len(cores)]

    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    img[:, :] = cor

    imageio.imwrite(caminho_arquivo, img)
    return caminho_arquivo