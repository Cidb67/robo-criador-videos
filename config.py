import os

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PASTA_TEMP = "temp"
    PASTA_VIDEOS = "videos"
    
    @classmethod
    def validar(cls):
        os.makedirs(cls.PASTA_TEMP, exist_ok=True)
        os.makedirs(cls.PASTA_VIDEOS, exist_ok=True)
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY nao configurado")