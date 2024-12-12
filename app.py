import os

# App Initialization
from . import create_app # from __init__ file
app = create_app(os.getenv("CONFIG_MODE"))

# Hello World!
@app.route('/')
def hello():
    return "Hello World!"

from .src.routes import routes

if __name__ == "__main__":
    app.run()