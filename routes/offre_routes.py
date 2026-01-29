from flask import Blueprint, request, jsonify
from models import db
from models.offre_emploi import OffreEmploi
from models.candidature import Candidature
from schemas.offre_schema import offre_schema
from schemas.candidat_schema import candidats_schema
from marshmallow import ValidationError
from services.ai_service import AIService

offre_bp = Blueprint('offre', __name__)

@offre_bp.route('/offers', methods=['POST'])
def creer_offre():
    """POST /offers: Création d'une offre"""
    try:
        data = offre_schema.load(request.json)
        
        db.session.add(data)
        db.session.commit()
        
        return jsonify({
            "message": "Offre créée avec succès",
            "offre": offre_schema.dump(data)
        }), 201
        
    except ValidationError as e:
        return jsonify({"error": "Données invalides", "details": e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@offre_bp.route('/offers/<int:id>/candidates', methods=['GET'])
def liste_candidats_offre(id):
    """GET /offers/<id>/candidates: Liste les candidats d'une offre"""
    try:
        offre = OffreEmploi.query.get(id)
        
        if not offre:
            return jsonify({"error": "Offre non trouvée"}), 404
        
        # Récupérer tous les candidats ayant postulé
        candidats = [candidature.candidat for candidature in offre.candidatures]
        
        return jsonify({
            "offre_id": id,
            "offre_titre": offre.titre,
            "nombre_candidats": len(candidats),
            "candidats": candidats_schema.dump(candidats)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@offre_bp.route('/offers/<int:id>/analyze-match', methods=['POST'])
def analyser_compatibilite(id):
    """POST /offers/<id>/analyze-match: Analyse la compatibilité avec Gemini"""
    try:
        offre = OffreEmploi.query.get(id)
        
        if not offre:
            return jsonify({"error": "Offre non trouvée"}), 404
        
        # Récupérer l'ID du candidat
        data = request.json
        candidat_id = data.get('candidat_id')
        
        if not candidat_id:
            return jsonify({"error": "candidat_id requis"}), 400
        
        from models.candidat import Candidat
        candidat = Candidat.query.get(candidat_id)
        
        if not candidat:
            return jsonify({"error": "Candidat non trouvé"}), 404
        
        # Appeler le service IA
        result = AIService.analyser_compatibilite(offre, candidat)
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify({
            "offre": {
                "id": offre.id,
                "titre": offre.titre
            },
            "candidat": {
                "id": candidat.id,
                "nom": candidat.nom
            },
            "analyse": result
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500