from models import db
from datetime import datetime

class Candidat(db.Model):
    __tablename__ = 'candidats'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    diplome = db.Column(db.String(200), nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Utiliser lazy='dynamic' et back_populates
    candidatures = db.relationship('Candidature', back_populates='candidat', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Candidat {self.nom}>'