from marshmallow import fields, validates, ValidationError, post_load
from schemas import ma
from models.candidat import Candidat
import re

class CandidatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidat
        load_instance = True
        include_fk = True
    
    id = fields.Integer(dump_only=True)
    nom = fields.String(required=True)
    email = fields.Email(required=True)
    bio = fields.String(required=True)
    diplome = fields.String(required=True)
    date_inscription = fields.DateTime(dump_only=True)
    
    @validates('nom')
    def validate_nom(self, value):
        if not value or len(value.strip()) < 2:
            raise ValidationError("Le nom doit contenir au moins 2 caractères")
        if len(value) > 100:
            raise ValidationError("Le nom ne peut pas dépasser 100 caractères")
    
    @validates('bio')
    def validate_bio(self, value):
        if not value or len(value.strip()) < 10:
            raise ValidationError("La bio doit contenir au moins 10 caractères")
        if len(value) > 2000:
            raise ValidationError("La bio ne peut pas dépasser 2000 caractères")
    
    @validates('diplome')
    def validate_diplome(self, value):
        if not value or len(value.strip()) < 2:
            raise ValidationError("Le diplôme doit contenir au moins 2 caractères")
        if len(value) > 200:
            raise ValidationError("Le diplôme ne peut pas dépasser 200 caractères")
    
    @validates('email')
    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValidationError("Format d'email invalide")

candidat_schema = CandidatSchema()
candidats_schema = CandidatSchema(many=True)