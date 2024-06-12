from flask import Flask
from .db import load_csv_to_db

def create_app():
    app = Flask(__name__)
    load_csv_to_db()
    
    with app.app_context():
        # Import and register the blueprint
        from .routes import bp
        app.register_blueprint(bp)
    
    return app
