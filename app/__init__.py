from flask import Flask
from app.routes.auth import home_bp
from app.routes.products import products_bp
from app.routes.upload import upload_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'  

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(upload_bp)
    

    return app
