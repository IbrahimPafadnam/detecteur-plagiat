from app import create_app, db
from app.models import AnalysisResult
from config import Config

app = create_app(config=Config)

with app.app_context():
    # Cela va créer toutes les tables définies dans nos modèles
    db.create_all()
    print("Base de données initialisée avec succès.")