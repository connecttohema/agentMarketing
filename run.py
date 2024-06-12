from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app)  # This will enable CORS for all routes

if __name__ == "__main__":
    app.run(port=5000, debug=True)
