import os
from pathlib import Path

# Chemin absolu du dossier contenant ce fichier
BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    # Mise en place d'un chemin absolu pour la base de données
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "data" / "hbnb.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # Chemins relatifs pour le développement (pour la compatibilité)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    

class ProductionConfig(Config):
    # En production, on utilise un chemin absolu
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}