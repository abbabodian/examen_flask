from marshmallow import fields
from schemas import ma
from models.candidature import Candidature

class CandidatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidature
        load_instance = True
        include_fk = True
    
    candidat_id = fields.Integer(required=True)
    offre_id = fields.Integer(required=True)

candidature_schema = CandidatureSchema()
candidatures_schema = CandidatureSchema(many=True)