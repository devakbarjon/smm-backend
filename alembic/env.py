from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from app.database.base import Base
from app.core.config import settings

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

# override URL from settings
config.set_main_option("sqlalchemy.url", settings.database_url())


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

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