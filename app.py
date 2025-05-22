import os
from flask_cors import CORS

# App Initialization
from . import create_app  # from __init__ file
app = create_app(os.getenv("CONFIG_MODE"))

CORS(app)

# Import all routes
from .src.routes import routes

if __name__ == "__main__":
    app.run()