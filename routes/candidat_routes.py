from flask import Blueprint, request, jsonify
from models import db
from models.candidat import Candidat
from schemas.candidat_schema import candidat_schema, candidats_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

candidat_bp = Blueprint('candidat', __name__)

# ========================================
# GET - Liste tous les candidats
# ========================================
@candidat_bp.route('/candidates', methods=['GET'])
def get_all_candidates():
    """GET /api/candidates - Récupérer tous les candidats"""
    try:
        candidats = Candidat.query.order_by(Candidat.date_inscription.desc()).all()
        
        return jsonify({
            "success": True,
            "candidats": candidats_schema.dump(candidats),
            "total": len(candidats)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# GET - Obtenir un candidat par ID
# ========================================
@candidat_bp.route('/candidates/<int:id>', methods=['GET'])
def get_candidate(id):
    """GET /api/candidates/<id> - Récupérer un candidat"""
    try:
        candidat = Candidat.query.get(id)
        
        if not candidat:
            return jsonify({
                "success": False,
                "error": "Candidat non trouvé"
            }), 404
        
        return jsonify({
            "success": True,
            "candidat": candidat_schema.dump(candidat)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# POST - Créer un candidat
# ========================================
@candidat_bp.route('/candidates', methods=['POST'])
def creer_candidat():
    """POST /api/candidates - Inscription d'un candidat"""
    try:
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                "success": False,
                "error": "Données JSON requises"
            }), 400
        
        # Validation des données avec Marshmallow
        try:
            candidat = candidat_schema.load(json_data)
        except ValidationError as e:
            return jsonify({
                "success": False,
                "error": "Données invalides",
                "details": e.messages
            }), 400
        
        # Vérifier l'unicité de l'email
        existing = Candidat.query.filter_by(email=json_data.get('email')).first()
        if existing:
            return jsonify({
                "success": False,
                "error": "Un candidat avec cet email existe déjà"
            }), 409
        
        # Créer le candidat
        db.session.add(candidat)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Candidat créé avec succès",
            "candidat": candidat_schema.dump(candidat)
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Email déjà utilisé"
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# PUT - Modifier un candidat
# ========================================
@candidat_bp.route('/candidates/<int:id>', methods=['PUT'])
def update_candidate(id):
    """PUT /api/candidates/<id> - Modifier un candidat"""
    try:
        candidat = Candidat.query.get(id)
        
        if not candidat:
            return jsonify({
                "success": False,
                "error": "Candidat non trouvé"
            }), 404
        
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                "success": False,
                "error": "Données JSON requises"
            }), 400
        
        # Mise à jour des champs
        if 'nom' in json_data:
            candidat.nom = json_data['nom']
        if 'email' in json_data:
            # Vérifier unicité du nouvel email
            existing = Candidat.query.filter(
                Candidat.email == json_data['email'],
                Candidat.id != id
            ).first()
            if existing:
                return jsonify({
                    "success": False,
                    "error": "Cet email est déjà utilisé"
                }), 409
            candidat.email = json_data['email']
        if 'bio' in json_data:
            candidat.bio = json_data['bio']
        if 'diplome' in json_data:
            candidat.diplome = json_data['diplome']
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Candidat mis à jour",
            "candidat": candidat_schema.dump(candidat)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ========================================
# DELETE - Supprimer un candidat
# ========================================
@candidat_bp.route('/candidates/<int:id>', methods=['DELETE'])
def delete_candidate(id):
    """DELETE /api/candidates/<id> - Supprimer un candidat"""
    try:
        candidat = Candidat.query.get(id)
        
        if not candidat:
            return jsonify({
                "success": False,
                "error": "Candidat non trouvé"
            }), 404
        
        nom = candidat.nom
        db.session.delete(candidat)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Candidat '{nom}' supprimé avec succès"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500