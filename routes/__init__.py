def register_blueprints(app):
    # Fonction qui enregistre tous les blueprints de l'application

    from routes.candidat_routes import candidat_bp   # Routes des candidats
    from routes.offre_routes import offre_bp         # Routes des offres
    from routes.candidature_routes import candidature_bp  # Routes des candidatures
    
    app.register_blueprint(candidat_bp, url_prefix='/api')  # Enregistrement candidats
    app.register_blueprint(offre_bp, url_prefix='/api')     # Enregistrement offres
    app.register_blueprint(candidature_bp, url_prefix='/api')  # Enregistrement candidatures
    
    print("✅ Routes enregistrées:")
    print("   - GET/POST /api/candidates")
    print("   - GET/POST /api/offers")
    print("   - POST /api/apply")
