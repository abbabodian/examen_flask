from models import db
from datetime import datetime

class OffreEmploi(db.Model):
    __tablename__ = 'offres_emploi'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    competences = db.Column(db.JSON, nullable=False)
    salaire = db.Column(db.Float, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Utiliser lazy='dynamic' et back_populates
    candidatures = db.relationship('Candidature', back_populates='offre', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<OffreEmploi {self.titre}>'