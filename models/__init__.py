from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importer tous les modèles APRÈS l'initialisation de db
# Ceci permet à SQLAlchemy de résoudre les relations
def init_models():
    from models.candidat import Candidat
    from models.offre_emploi import OffreEmploi
    from models.candidature import Candidature