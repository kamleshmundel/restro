import os
from logging.config import fileConfig
from urllib.parse import quote_plus

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Alembic Config object
config = context.config

# Setup Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models here
from app.database.models import *  # replace with your actual models path

# Build DB URL safely (encode special chars in password)
DB_USER = os.getenv("DATABASE_USERNAME")
DB_PASS = quote_plus(os.getenv("DATABASE_PASSWORD"))
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "3306")
DB_NAME = os.getenv("DATABASE_NAME")
DB_CHARSET = os.getenv("DATABASE_CHARSET", "utf8mb4")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

print('DATABASE_URL >>>>>>>>>>>>>>>>>>>>>>>>> ', DATABASE_URL)

# Do NOT escape % or set via config.set_main_option - pass directly to context.configure instead

# Metadata for 'autogenerate'
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Pass the raw DATABASE_URL directly (no config.get_main_option)
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Use engine_from_config but override the URL with the raw DATABASE_URL
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL,  # Override here to use the correct URL
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()