from logging.config import fileConfig
from alembic import context
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", "sqlite:///notes_dev.db"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models.user import User
from app.models.note import Note

target_metadata = db.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata,
                      literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    app = create_app()
    with app.app_context():
        connectable = db.engine
        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
