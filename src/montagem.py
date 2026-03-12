import os

from PIL import Image

# Compatibilidade com Pillow novo
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout


def criar_video(imagens, audio_path, nome_video, pasta_saida="videos"):
    os.makedirs(pasta_saida, exist_ok=True)

    if not imagens:
        raise ValueError("Lista de imagens vazia")

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio não encontrado: {audio_path}")

    audio = AudioFileClip(audio_path)
    duracao_total = audio.duration
    duracao_por_imagem = duracao_total / len(imagens)

    clips = []

    for img_path in imagens:
        if not os.path.exists(img_path):
            print(f"Imagem não encontrada: {img_path}")
            continue

        try:
            clip = (
                ImageClip(img_path)
                .set_duration(duracao_por_imagem)
                .resize(height=720)
                .fx(fadein, 0.5)
                .fx(fadeout, 0.5)
            )
            clips.append(clip)

        except Exception as e:
            print(f"Aviso: Erro ao carregar {img_path}: {e}")

    if not clips:
        raise ValueError("Nenhuma imagem valida para criar video")

    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)

    caminho_final = os.path.join(pasta_saida, nome_video)

    video.write_videofile(
        caminho_final,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="ultrafast"
    )

    video.close()
    audio.close()

    return caminho_final