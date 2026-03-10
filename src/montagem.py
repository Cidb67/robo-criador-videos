from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout
import os

def criar_video(imagens, audio_path, nome_video, pasta_saida="videos"):
    os.makedirs(pasta_saida, exist_ok=True)
    
    audio = AudioFileClip(audio_path)
    duracao_total = audio.duration
    duracao_por_imagem = duracao_total / len(imagens)
    
    clips = []
    for img_path in imagens:
        # Verifica se imagem existe e tem tamanho
        if not os.path.exists(img_path) or os.path.getsize(img_path) < 1000:
            print(f"  Aviso: Imagem {img_path} invalida, pulando")
            continue
            
        clip = (ImageClip(img_path)
                .set_duration(duracao_por_imagem)
                .resize(height=720)  # Reduzido para 720p
                .fx(fadein, duration=0.5)
                .fx(fadeout, duration=0.5))
        clips.append(clip)
    
    if not clips:
        raise ValueError("Nenhuma imagem valida para criar video")
    
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    
    caminho_final = os.path.join(pasta_saida, nome_video)
    
    video.write_videofile(
        caminho_final,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        threads=4,
        preset='ultrafast',
        logger=None
    )
    
    video.close()
    audio.close()
    
    return caminho_final