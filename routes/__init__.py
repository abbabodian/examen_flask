from flask import Blueprint

def register_blueprints(app):
    from routes.candidat_routes import candidat_bp
    from routes.offre_routes import offre_bp
    from routes.candidature_routes import candidature_bp
    
    app.register_blueprint(candidat_bp, url_prefix='/api')
    app.register_blueprint(offre_bp, url_prefix='/api')
    app.register_blueprint(candidature_bp, url_prefix='/api')