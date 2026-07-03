from logging.config import fileConfig
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

# --------------------------------------------------
# Project Path
# --------------------------------------------------

sys.path.append(os.getcwd())

# --------------------------------------------------
# Settings
# --------------------------------------------------

from app.core.config import settings

# --------------------------------------------------
# Import ALL Models
# --------------------------------------------------

import app.models.user
import app.models.topic
import app.models.user_skill
import app.models.question
import app.models.test_attempt
import app.models.test_attempt_question
import app.models.test_answer
import app.models.notification
import app.models.availability
import app.models.session
import app.models.token_transaction
import app.models.profile
import app.models.skill
import app.models.tutor_profile
import app.models.learner_profile

# --------------------------------------------------
# Alembic Config
# --------------------------------------------------

config = context.config

# Read DATABASE_URL from .env
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL
)

# --------------------------------------------------
# Logging
# --------------------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --------------------------------------------------
# Metadata
# --------------------------------------------------

target_metadata = SQLModel.metadata


# --------------------------------------------------
# Offline Migration
# --------------------------------------------------

def run_migrations_offline():

    url = config.get_main_option("sqlalchemy.url")

    context.configure(

        url=url,

        target_metadata=target_metadata,

        literal_binds=True,

        dialect_opts={"paramstyle": "named"}

    )

    with context.begin_transaction():

        context.run_migrations()


# --------------------------------------------------
# Online Migration
# --------------------------------------------------

def run_migrations_online():

    connectable = engine_from_config(

        config.get_section(
            config.config_ini_section,
            {}
        ),

        prefix="sqlalchemy.",

        poolclass=pool.NullPool

    )

    with connectable.connect() as connection:

        context.configure(

            connection=connection,

            target_metadata=target_metadata,

            compare_type=True,

            compare_server_default=True

        )

        with context.begin_transaction():

            context.run_migrations()


# --------------------------------------------------
# Run
# --------------------------------------------------

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()