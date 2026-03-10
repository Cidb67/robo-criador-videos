import os

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PASTA_TEMP = "temp"
    PASTA_VIDEOS = "videos"
    
    @classmethod
    def validar(cls):
        os.makedirs(cls.PASTA_TEMP, exist_ok=True)
        os.makedirs(cls.PASTA_VIDEOS, exist_ok=True)
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY nao configurado")