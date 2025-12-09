from flask import Flask, render_template, after_this_request
from .extensions import db, login_manager, csrf
from .models import User, Patient


def create_app(config_object="config.DevConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .auth import bp as auth_bp
    from .patients import bp as patients_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(patients_bp, url_prefix="/patients")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.after_request
    def set_security_headers(response):
        response.headers["Content-Security-Policy"] = "default-src 'self' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; script-src 'self' https://cdn.jsdelivr.net"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    with app.app_context():
        db.create_all()

    return app
