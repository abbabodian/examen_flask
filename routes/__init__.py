def register_blueprints(app):
    """Enregistrer tous les blueprints de l'application"""
    from routes.candidat_routes import candidat_bp
    from routes.offre_routes import offre_bp
    from routes.candidature_routes import candidature_bp
    
    app.register_blueprint(candidat_bp, url_prefix='/api')
    app.register_blueprint(offre_bp, url_prefix='/api')
    app.register_blueprint(candidature_bp, url_prefix='/api')
    
    print("✅ Routes enregistrées:")
    print("   - GET/POST /api/candidates")
    print("   - GET/POST /api/offers")
    print("   - POST /api/apply")