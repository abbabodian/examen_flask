from marshmallow import fields
from schemas import ma
from models.candidature import Candidature

# Schéma Marshmallow pour le modèle Candidature
class CandidatureSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Candidature     # Modèle SQLAlchemy associé
        load_instance = True    # Conversion en objet Candidature
        include_fk = True       # Inclusion des clés étrangères
    
    id = fields.Integer(dump_only=True)        # Identifiant (lecture seule)
    candidat_id = fields.Integer(required=True)  # ID du candidat
    offre_id = fields.Integer(required=True)     # ID de l'offre
    date_depot = fields.DateTime(dump_only=True) # Date de dépôt automatique

# Schéma pour une seule candidature
candidature_schema = CandidatureSchema()

# Schéma pour plusieurs candidatures
candidatures_schema = CandidatureSchema(many=True)
