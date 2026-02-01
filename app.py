from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from models import db, init_models
from schemas import ma

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(Config)
    
    # Activer CORS pour les requêtes frontend
    CORS(app)
    
    # Initialiser les extensions
    db.init_app(app)
    ma.init_app(app)
    
    # Créer les tables
    with app.app_context():
        # Importer les modèles AVANT de créer les tables
        init_models()
        db.create_all()
        print("✅ Base de données initialisée")
    
    # Enregistrer les blueprints APRÈS l'initialisation des modèles
    from routes import register_blueprints
    register_blueprints(app)
    
    # ========== GESTIONNAIRES D'ERREURS ==========
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Resource not found",
            "message": "La ressource demandée n'existe pas"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error",
            "message": "Une erreur interne s'est produite"
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad request",
            "message": "Requête invalide"
        }), 400
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method not allowed",
            "message": "Méthode HTTP non autorisée"
        }), 405
    
    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            "error": "Conflict",
            "message": "Conflit de données"
        }), 409
    # =============================================
    
    # Route pour servir le frontend
    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')
    
    # Route API info
    @app.route('/api')
    def api_info():
        return jsonify({
            "message": "Smart-Recruit API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "POST /api/candidates": "Créer un candidat",
                "POST /api/offers": "Créer une offre",
                "POST /api/apply": "Soumettre une candidature",
                "GET /api/offers/<id>/candidates": "Liste des candidats d'une offre",
                "POST /api/offers/<id>/analyze-match": "Analyser compatibilité avec IA"
            }
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*70)
    print("🚀 Smart-Recruit API + Frontend démarrée !")
    print("="*70)
    print("📱 Frontend:  http://localhost:5000")
    print("🔧 API Info:  http://localhost:5000/api")
    print("📚 Endpoints: http://localhost:5000/api/candidates, /api/offers, etc.")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)