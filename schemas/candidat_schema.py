from marshmallow import fields, validates, ValidationError, post_load
from schemas import ma
from models.candidat import Candidat
import re

# Schéma Marshmallow pour le modèle Candidat
class CandidatSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Candidat        # Modèle SQLAlchemy associé
        load_instance = True    # Conversion en objet Candidat
        include_fk = True       # Inclusion des clés étrangères
    
    id = fields.Integer(dump_only=True)          # Identifiant (lecture seule)
    nom = fields.String(required=True)           # Nom du candidat
    email = fields.Email(required=True)          # Email du candidat
    bio = fields.String(required=True)           # Biographie
    diplome = fields.String(required=True)       # Diplôme
    date_inscription = fields.DateTime(dump_only=True)  # Date automatique
    
    @validates('nom')
    def validate_nom(self, value):
        # Validation du nom
        if not value or len(value.strip()) < 2:
            raise ValidationError("Le nom doit contenir au moins 2 caractères")
        if len(value) > 100:
            raise ValidationError("Le nom ne peut pas dépasser 100 caractères")
    
    @validates('bio')
    def validate_bio(self, value):
        # Validation de la bio
        if not value or len(value.strip()) < 10:
            raise ValidationError("La bio doit contenir au moins 10 caractères")
        if len(value) > 2000:
            raise ValidationError("La bio ne peut pas dépasser 2000 caractères")
    
    @validates('diplome')
    def validate_diplome(self, value):
        # Validation du diplôme
        if not value or len(value.strip()) < 2:
            raise ValidationError("Le diplôme doit contenir au moins 2 caractères")
        if len(value) > 200:
            raise ValidationError("Le diplôme ne peut pas dépasser 200 caractères")
    
    @validates('email')
    def validate_email(self, value):
        # Validation du format de l'email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValidationError("Format d'email invalide")

# Schéma pour un seul candidat
candidat_schema = CandidatSchema()

# Schéma pour plusieurs candidats
candidats_schema = CandidatSchema(many=True)
