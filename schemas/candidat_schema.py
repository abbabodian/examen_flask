from marshmallow import fields, validates, ValidationError
from schemas import ma
from models.candidat import Candidat
import re

class CandidatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidat
        load_instance = True
        include_fk = True
    
    nom = fields.String(required=True)
    email = fields.Email(required=True)
    bio = fields.String(required=True)
    diplome = fields.String(required=True)
    
    @validates('nom')
    def validate_nom(self, value):
        if not value or len(value) < 2 or len(value) > 100:
            raise ValidationError("Le nom doit contenir entre 2 et 100 caractères")
    
    @validates('bio')
    def validate_bio(self, value):
        if not value or len(value) < 10 or len(value) > 2000:
            raise ValidationError("La bio doit contenir entre 10 et 2000 caractères")
    
    @validates('diplome')
    def validate_diplome(self, value):
        if not value or len(value) < 2 or len(value) > 200:
            raise ValidationError("Le diplôme doit contenir entre 2 et 200 caractères")
    
    @validates('email')
    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValidationError("Format d'email invalide")

candidat_schema = CandidatSchema()
candidats_schema = CandidatSchema(many=True)