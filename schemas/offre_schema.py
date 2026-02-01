from marshmallow import fields, validates, ValidationError
from schemas import ma
from models.offre_emploi import OffreEmploi

class OffreEmploiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OffreEmploi
        load_instance = True
    
    id = fields.Integer(dump_only=True)
    titre = fields.String(required=True)
    description = fields.String(required=True)
    competences = fields.List(fields.String(), required=True)
    salaire = fields.Float(required=True)
    date_creation = fields.DateTime(dump_only=True)
    
    @validates('titre')
    def validate_titre(self, value):
        if not value or len(value.strip()) < 5:
            raise ValidationError("Le titre doit contenir au moins 5 caractères")
        if len(value) > 200:
            raise ValidationError("Le titre ne peut pas dépasser 200 caractères")
    
    @validates('description')
    def validate_description(self, value):
        if not value or len(value.strip()) < 20:
            raise ValidationError("La description doit contenir au moins 20 caractères")
        if len(value) > 5000:
            raise ValidationError("La description ne peut pas dépasser 5000 caractères")
    
    @validates('competences')
    def validate_competences(self, value):
        if not value or len(value) == 0:
            raise ValidationError("Au moins une compétence est requise")
        if len(value) > 20:
            raise ValidationError("Maximum 20 compétences autorisées")
    
    @validates('salaire')
    def validate_salaire(self, value):
        if value is None or value <= 0:
            raise ValidationError("Le salaire doit être un nombre positif")

offre_schema = OffreEmploiSchema()
offres_schema = OffreEmploiSchema(many=True)