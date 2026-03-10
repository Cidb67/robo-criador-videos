from gtts import gTTS
import os

def gerar_narracao_gtts(texto, caminho_saida):
    texto_limpo = texto.replace('"', '').replace("'", "")[:4500]
    
    print(f"   Gerando audio ({len(texto_limpo)} chars)...", end=" ")
    
    tts = gTTS(text=texto_limpo, lang='pt-br', slow=False)
    tts.save(caminho_saida)
    
    print("OK")
    return caminho_saida