from flask import Flask
from app.routes.auth import home_bp
from app.routes.products import products_bp
from app.routes.upload import upload_bp
from app.routes.login import login_bp
from app.routes.signup import signup_bp
from app.routes.cart import cart_bp
from app.routes.delivery import delivery_bp
from app.routes.checkout import checkout_bp
from app.routes.payment import payment_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'  

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(payment_bp)
    

    return app
