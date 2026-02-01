from flask import Blueprint, request, jsonify
from models import db
from models.offre_emploi import OffreEmploi
from models.candidat import Candidat
from models.candidature import Candidature
from schemas.offre_schema import offre_schema, offres_schema
from schemas.candidat_schema import candidats_schema
from marshmallow import ValidationError
from services.ai_service import AIService

offre_bp = Blueprint('offre', __name__)

# ========================================
# GET - Liste toutes les offres
# ========================================
@offre_bp.route('/offers', methods=['GET'])
def get_all_offers():
    """GET /api/offers - Récupérer toutes les offres"""
    try:
        offres = OffreEmploi.query.order_by(OffreEmploi.date_creation.desc()).all()
        
        return jsonify({
            "success": True,
            "offres": offres_schema.dump(offres),
            "total": len(offres)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# GET - Obtenir une offre par ID
# ========================================
@offre_bp.route('/offers/<int:id>', methods=['GET'])
def get_offer(id):
    """GET /api/offers/<id> - Récupérer une offre"""
    try:
        offre = OffreEmploi.query.get(id)
        
        if not offre:
            return jsonify({
                "success": False,
                "error": "Offre non trouvée"
            }), 404
        
        return jsonify({
            "success": True,
            "offre": offre_schema.dump(offre)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# POST - Créer une offre
# ========================================
@offre_bp.route('/offers', methods=['POST'])
def creer_offre():
    """POST /api/offers - Création d'une offre"""
    try:
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                "success": False,
                "error": "Données JSON requises"
            }), 400
        
        try:
            offre = offre_schema.load(json_data)
        except ValidationError as e:
            return jsonify({
                "success": False,
                "error": "Données invalides",
                "details": e.messages
            }), 400
        
        db.session.add(offre)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Offre créée avec succès",
            "offre": offre_schema.dump(offre)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# PUT - Modifier une offre
# ========================================
@offre_bp.route('/offers/<int:id>', methods=['PUT'])
def update_offer(id):
    """PUT /api/offers/<id> - Modifier une offre"""
    try:
        offre = OffreEmploi.query.get(id)
        
        if not offre:
            return jsonify({
                "success": False,
                "error": "Offre non trouvée"
            }), 404
        
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                "success": False,
                "error": "Données JSON requises"
            }), 400
        
        if 'titre' in json_data:
            offre.titre = json_data['titre']
        if 'description' in json_data:
            offre.description = json_data['description']
        if 'competences' in json_data:
            offre.competences = json_data['competences']
        if 'salaire' in json_data:
            offre.salaire = json_data['salaire']
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Offre mise à jour",
            "offre": offre_schema.dump(offre)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# DELETE - Supprimer une offre
# ========================================
@offre_bp.route('/offers/<int:id>', methods=['DELETE'])
def delete_offer(id):
    """DELETE /api/offers/<id> - Supprimer une offre"""
    try:
        offre = OffreEmploi.query.get(id)
        
        if not offre:
            return jsonify({
                "success": False,
                "error": "Offre non trouvée"
            }), 404
        
        titre = offre.titre
        db.session.delete(offre)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Offre '{titre}' supprimée avec succès"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# GET - Candidats d'une offre
# ========================================
@offre_bp.route('/offers/<int:id>/candidates', methods=['GET'])
def liste_candidats_offre(id):
    """GET /api/offers/<id>/candidates - Liste les candidats d'une offre"""
    try:
        offre = OffreEmploi.query.get(id)
        
        if not offre:
            return jsonify({
                "success": False,
                "error": "Offre non trouvée"
            }), 404
        
        # Récupérer les candidatures
        candidatures = Candidature.query.filter_by(offre_id=id).all()
        
        # Récupérer les candidats
        candidats = []
        for candidature in candidatures:
            candidat = Candidat.query.get(candidature.candidat_id)
            if candidat:
                candidats.append({
                    "id": candidat.id,
                    "nom": candidat.nom,
                    "email": candidat.email,
                    "bio": candidat.bio,
                    "diplome": candidat.diplome,
                    "date_candidature": candidature.date_depot.isoformat() if candidature.date_depot else None
                })
        
        return jsonify({
            "success": True,
            "offre": {
                "id": offre.id,
                "titre": offre.titre
            },
            "candidats": candidats,
            "nombre_candidats": len(candidats)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# POST - Analyser compatibilité IA
# ========================================
@offre_bp.route('/offers/<int:id>/analyze-match', methods=['POST'])
def analyser_compatibilite(id):
    """POST /api/offers/<id>/analyze-match - Analyse avec IA"""
    try:
        offre = OffreEmploi.query.get(id)
        
        if not offre:
            return jsonify({
                "success": False,
                "error": "Offre non trouvée"
            }), 404
        
        json_data = request.get_json()
        
        if not json_data or 'candidat_id' not in json_data:
            return jsonify({
                "success": False,
                "error": "candidat_id requis"
            }), 400
        
        candidat_id = json_data['candidat_id']
        candidat = Candidat.query.get(candidat_id)
        
        if not candidat:
            return jsonify({
                "success": False,
                "error": "Candidat non trouvé"
            }), 404
        
        # Appeler le service IA
        result = AIService.analyser_compatibilite(offre, candidat)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 500
        
        return jsonify({
            "success": True,
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
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500