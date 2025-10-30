import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")  
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")
    JWT_ALGO = os.getenv("JWT_ALGO")
    ACCESS_EXPIRE_MINUTES = int(os.getenv("ACCESS_EXPIRE_MINUTES"))
    REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_EXPIRE_DAYS"))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///library.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")          
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT")) 
    MONGO_URI = os.getenv("MONGO_URI") 