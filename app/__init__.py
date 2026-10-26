from pathlib import Path
from flask import Flask
from .database import init_db
from .scheduler import start_scheduler

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="change-this-in-production",
        DATABASE=str(Path(app.instance_path) / "agendador.sqlite3"),
        LOG_DIR=str(Path(app.instance_path) / "logs"),
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["LOG_DIR"]).mkdir(parents=True, exist_ok=True)
    init_db(app.config["DATABASE"])

    from .routes import bp
    app.register_blueprint(bp)
    start_scheduler(app)
    return app
