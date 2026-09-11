"""Alembic migration environment.

The database URL is sourced exclusively from ``app.core.config.settings``
(populated from environment variables).  It is never written into alembic.ini
so credentials never appear in a config file that might be committed to VCS.
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

import app.models  # noqa: F401  - ensures all models are registered with Base.metadata for autogenerate
from alembic import context
from app.core.config import settings
from app.db.base import Base

# ---------------------------------------------------------------------------
# Alembic Config object – provides access to values in alembic.ini.
# ---------------------------------------------------------------------------
config = context.config

# Inject the database URL from our settings object so it is the single
# source of truth and never leaks into alembic.ini.
config.set_main_option("sqlalchemy.url", settings.database_url)

# Set up Python logging as declared in alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData for autogenerate support.
target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# Migration runners
# ---------------------------------------------------------------------------


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Configures the context with just a URL rather than a live Engine.
    Useful for generating SQL scripts without a running database.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Render server-side defaults so autogenerate is accurate.
        render_as_batch=False,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode with a live database connection.

    Uses NullPool so Alembic never holds an idle connection after the
    migration completes – important for short-lived CLI invocations.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Detect column-type and server-default changes automatically.
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
