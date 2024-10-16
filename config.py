import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# Charge les variables d'environnement à partir du fichier .env
load_dotenv()

class Config:
    # Configuration Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_cle_secrete_difficile_a_deviner'
    
    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration pour Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configuration pour Google Custom Search API
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
    
    # Configuration pour le téléchargement de fichiers
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 

# Sélectionner la configuration en fonction de la variable d'environnement FLASK_ENV
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Utiliser la configuration par défaut si FLASK_ENV n'est pas défini
config_name = os.environ.get('FLASK_ENV')
config = config[config_name]