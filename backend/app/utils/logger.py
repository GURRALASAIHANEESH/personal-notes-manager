import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    log_file = app.config.get("LOG_FILE", "logs/app.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    if not app.debug:
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
