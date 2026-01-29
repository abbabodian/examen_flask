from flask import jsonify

def register_error_handlers(app):
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Resource not found",
            "message": str(error)
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
            "message": str(error)
        }), 400
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method not allowed",
            "message": str(error)
        }), 405