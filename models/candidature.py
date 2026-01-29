from models import db
from datetime import datetime

class Candidature(db.Model):
    __tablename__ = 'candidatures'
    
    id = db.Column(db.Integer, primary_key=True)
    candidat_id = db.Column(db.Integer, db.ForeignKey('candidats.id'), nullable=False)
    offre_id = db.Column(db.Integer, db.ForeignKey('offres_emploi.id'), nullable=False)
    date_depot = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Utiliser back_populates au lieu de backref
    candidat = db.relationship('Candidat', back_populates='candidatures')
    offre = db.relationship('OffreEmploi', back_populates='candidatures')
    
    # Contrainte d'unicité
    __table_args__ = (
        db.UniqueConstraint('candidat_id', 'offre_id', name='unique_candidature'),
    )
    
    def __repr__(self):
        return f'<Candidature {self.candidat_id} -> {self.offre_id}>'