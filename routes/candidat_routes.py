from flask import Blueprint, request, jsonify
from models import db
from models.candidat import Candidat
from schemas.candidat_schema import candidat_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

candidat_bp = Blueprint('candidat', __name__)

@candidat_bp.route('/candidates', methods=['POST'])
def creer_candidat():
    """POST /candidates: Inscription d'un candidat"""
    try:
        # Validation des données
        data = candidat_schema.load(request.json)
        
        # Vérifier l'unicité de l'email
        if Candidat.query.filter_by(email=data.email).first():
            return jsonify({"error": "Un candidat avec cet email existe déjà"}), 409
        
        # Créer le candidat
        db.session.add(data)
        db.session.commit()
        
        return jsonify({
            "message": "Candidat créé avec succès",
            "candidat": candidat_schema.dump(data)
        }), 201
        
    except ValidationError as e:
        return jsonify({"error": "Données invalides", "details": e.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Erreur d'intégrité des données"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500