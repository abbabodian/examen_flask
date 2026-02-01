from flask import Blueprint, request, jsonify
from models import db
from models.candidature import Candidature
from models.candidat import Candidat
from models.offre_emploi import OffreEmploi
from schemas.candidature_schema import candidature_schema
from sqlalchemy.exc import IntegrityError

candidature_bp = Blueprint('candidature', __name__)

# ========================================
# POST - Soumettre une candidature
# ========================================
@candidature_bp.route('/apply', methods=['POST'])
def soumettre_candidature():
    """POST /api/apply - Soumettre une candidature"""
    try:
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                "success": False,
                "error": "Données JSON requises"
            }), 400
        
        candidat_id = json_data.get('candidat_id')
        offre_id = json_data.get('offre_id')
        
        if not candidat_id or not offre_id:
            return jsonify({
                "success": False,
                "error": "candidat_id et offre_id sont requis"
            }), 400
        
        # Vérifier que le candidat existe
        candidat = Candidat.query.get(candidat_id)
        if not candidat:
            return jsonify({
                "success": False,
                "error": "Candidat non trouvé"
            }), 404
        
        # Vérifier que l'offre existe
        offre = OffreEmploi.query.get(offre_id)
        if not offre:
            return jsonify({
                "success": False,
                "error": "Offre non trouvée"
            }), 404
        
        # Vérifier si candidature existe déjà
        existing = Candidature.query.filter_by(
            candidat_id=candidat_id,
            offre_id=offre_id
        ).first()
        
        if existing:
            return jsonify({
                "success": False,
                "error": "Candidature déjà soumise pour cette offre"
            }), 409
        
        # Créer la candidature
        candidature = Candidature(
            candidat_id=candidat_id,
            offre_id=offre_id
        )
        
        db.session.add(candidature)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Candidature de '{candidat.nom}' pour '{offre.titre}' soumise",
            "candidature": candidature_schema.dump(candidature)
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Candidature déjà existante"
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# POST - Postuler via /offers/<id>/apply
# ========================================
@candidature_bp.route('/offers/<int:offre_id>/apply', methods=['POST'])
def postuler_offre(offre_id):
    """POST /api/offers/<id>/apply - Postuler à une offre"""
    try:
        json_data = request.get_json()
        
        if not json_data or 'candidat_id' not in json_data:
            return jsonify({
                "success": False,
                "error": "candidat_id requis"
            }), 400
        
        candidat_id = json_data['candidat_id']
        
        # Vérifier l'offre
        offre = OffreEmploi.query.get(offre_id)
        if not offre:
            return jsonify({
                "success": False,
                "error": "Offre non trouvée"
            }), 404
        
        # Vérifier le candidat
        candidat = Candidat.query.get(candidat_id)
        if not candidat:
            return jsonify({
                "success": False,
                "error": "Candidat non trouvé"
            }), 404
        
        # Vérifier doublon
        existing = Candidature.query.filter_by(
            candidat_id=candidat_id,
            offre_id=offre_id
        ).first()
        
        if existing:
            return jsonify({
                "success": False,
                "error": "Candidature déjà existante"
            }), 409
        
        # Créer
        candidature = Candidature(
            candidat_id=candidat_id,
            offre_id=offre_id
        )
        
        db.session.add(candidature)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Candidature enregistrée avec succès"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500