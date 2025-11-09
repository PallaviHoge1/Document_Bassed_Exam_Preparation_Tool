import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()  # load .env

    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change_me")
    app.config["UPLOAD_FOLDER"] = os.path.join(app.instance_path, "uploads")
    app.config["DATA_FOLDER"] = os.path.join(app.instance_path, "data")

    # Ensure instance subdirs exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["DATA_FOLDER"], exist_ok=True)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
