from backend.routes.predict import predict_bp
from backend.routes.health import health_bp

def register_routes(app):
    app.register_blueprint(predict_bp)
    app.register_blueprint(health_bp)