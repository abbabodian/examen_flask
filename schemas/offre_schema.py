from marshmallow import fields, validates, ValidationError
from schemas import ma
from models.offre_emploi import OffreEmploi

class OffreEmploiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OffreEmploi
        load_instance = True
    
    titre = fields.String(required=True)
    description = fields.String(required=True)
    competences = fields.List(fields.String(), required=True)
    salaire = fields.Float(required=True)
    
    @validates('titre')
    def validate_titre(self, value):
        if not value or len(value) < 5 or len(value) > 200:
            raise ValidationError("Le titre doit contenir entre 5 et 200 caractères")
    
    @validates('description')
    def validate_description(self, value):
        if not value or len(value) < 20 or len(value) > 5000:
            raise ValidationError("La description doit contenir entre 20 et 5000 caractères")
    
    @validates('competences')
    def validate_competences(self, value):
        if not value or len(value) == 0:
            raise ValidationError("Au moins une compétence est requise")
        if len(value) > 20:
            raise ValidationError("Maximum 20 compétences autorisées")
    
    @validates('salaire')
    def validate_salaire(self, value):
        if value <= 0:
            raise ValidationError("Le salaire doit être positif")

offre_schema = OffreEmploiSchema()
offres_schema = OffreEmploiSchema(many=True)