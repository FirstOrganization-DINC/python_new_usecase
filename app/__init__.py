from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.upload_routes import upload_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    return app
