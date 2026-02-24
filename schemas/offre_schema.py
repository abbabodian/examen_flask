from marshmallow import fields, validates, ValidationError
from schemas import ma
from models.offre_emploi import OffreEmploi

# Schéma Marshmallow pour le modèle OffreEmploi
class OffreEmploiSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = OffreEmploi      # Modèle lié au schéma
        load_instance = True     # Conversion automatique en objet SQLAlchemy
    
    id = fields.Integer(dump_only=True)          # Identifiant (lecture seule)
    titre = fields.String(required=True)         # Titre de l'offre
    description = fields.String(required=True)   # Description de l'offre
    competences = fields.List(fields.String(), required=True)  # Liste des compétences
    salaire = fields.Float(required=True)        # Salaire proposé
    date_creation = fields.DateTime(dump_only=True)  # Date auto-générée
    
    @validates('titre')
    def validate_titre(self, value):
        # Validation du titre
        if not value or len(value.strip()) < 5:
            raise ValidationError("Le titre doit contenir au moins 5 caractères")
        if len(value) > 200:
            raise ValidationError("Le titre ne peut pas dépasser 200 caractères")
    
    @validates('description')
    def validate_description(self, value):
        # Validation de la description
        if not value or len(value.strip()) < 20:
            raise ValidationError("La description doit contenir au moins 20 caractères")
        if len(value) > 5000:
            raise ValidationError("La description ne peut pas dépasser 5000 caractères")
    
    @validates('competences')
    def validate_competences(self, value):
        # Validation des compétences
        if not value or len(value) == 0:
            raise ValidationError("Au moins une compétence est requise")
        if len(value) > 20:
            raise ValidationError("Maximum 20 compétences autorisées")
    
    @validates('salaire')
    def validate_salaire(self, value):
        # Validation du salaire
        if value is None or value <= 0:
            raise ValidationError("Le salaire doit être un nombre positif")

# Schéma pour une seule offre
offre_schema = OffreEmploiSchema()

# Schéma pour plusieurs offres
offres_schema = OffreEmploiSchema(many=True)
