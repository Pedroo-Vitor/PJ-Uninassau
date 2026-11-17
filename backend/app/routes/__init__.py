from .health import bp as health_bp
from .auth import bp as auth_bp

def register_blueprints(app):
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    # depois: auth, assistidos, atendimentos, casos, atividades,
    # documentos, prazos, dashboard