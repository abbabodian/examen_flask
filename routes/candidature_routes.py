from flask import Blueprint, request, jsonify
from models import db
from models.candidature import Candidature
from models.candidat import Candidat
from models.offre_emploi import OffreEmploi
from schemas.candidature_schema import candidature_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

candidature_bp = Blueprint('candidature', __name__)

@candidature_bp.route('/apply', methods=['POST'])
def soumettre_candidature():
    """POST /apply: Soumettre une candidature"""
    try:
        data = request.json
        
        if not data or 'candidat_id' not in data or 'offre_id' not in data:
            return jsonify({"error": "candidat_id et offre_id requis"}), 400
        
        candidat_id = data['candidat_id']
        offre_id = data['offre_id']
        
        # Vérifier que le candidat existe
        candidat = Candidat.query.get(candidat_id)
        if not candidat:
            return jsonify({"error": "Candidat non trouvé"}), 404
        
        # Vérifier que l'offre existe
        offre = OffreEmploi.query.get(offre_id)
        if not offre:
            return jsonify({"error": "Offre non trouvée"}), 404
        
        # Vérifier si une candidature existe déjà
        candidature_existante = Candidature.query.filter_by(
            candidat_id=candidat_id,
            offre_id=offre_id
        ).first()
        
        if candidature_existante:
            return jsonify({"error": "Candidature déjà soumise pour cette offre"}), 409
        
        # Créer la candidature
        candidature = Candidature(candidat_id=candidat_id, offre_id=offre_id)
        db.session.add(candidature)
        db.session.commit()
        
        return jsonify({
            "message": "Candidature soumise avec succès",
            "candidature": candidature_schema.dump(candidature)
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Candidature déjà existante"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500