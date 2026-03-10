#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

from config import Config
from src.roteiro import gerar_roteiro, parsear_roteiro
from src.imagens import gerar_imagens_pollinations
from src.narracao import gerar_narracao_gtts
from src.montagem import criar_video

def main():
    parser = argparse.ArgumentParser(description="Robo Criador de Videos")
    parser.add_argument("--tema", required=True, help="Tema do video")
    parser.add_argument("--duracao", default="2min", help="Duracao aproximada")
    args = parser.parse_args()
    
    Config.validar()
    
    print(f"\n{'='*60}")
    print(f"INICIANDO: {args.tema}")
    print(f"{'='*60}\n")
    
    try:
        print("Etapa 1/4: Gerando roteiro...")
        roteiro = gerar_roteiro(args.tema, args.duracao)
        cenas, texto_narracao = parsear_roteiro(roteiro)
        print(f"   {len(cenas)} cenas identificadas")
        
        print("\nEtapa 2/4: Gerando imagens...")
        imagens_geradas = gerar_imagens_pollinations(cenas, Config.PASTA_TEMP)
        
        print("\nEtapa 3/4: Criando narracao...")
        audio_path = os.path.join(Config.PASTA_TEMP, "narracao.mp3")
        audio_gerado = gerar_narracao_gtts(texto_narracao, audio_path)
        
        print("\nEtapa 4/4: Montando video...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_seguro = "".join(c for c in args.tema if c.isalnum() or c in (' ', '-', '_')).rstrip()[:30]
        nome_video = f"{nome_seguro.replace(' ', '_')}_{timestamp}.mp4"
        
        video_final = criar_video(imagens_geradas, audio_gerado, nome_video, Config.PASTA_VIDEOS)
        
        for f in imagens_geradas + [audio_gerado]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass
        
        print(f"\n{'='*60}")
        print("SUCESSO!")
        print(f"   {video_final}")
        print(f"{'='*60}")
        
        return 0
        
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())