from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from users.db.models import Base
from db.db_postgres_settings import DATABASE_URL

# Конфигурация Alembic
config = context.config
url = config.get_main_option("sqlalchemy.url", DATABASE_URL)
engine = create_async_engine(url)

# Настройка логгера
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные базы данных
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """Выполняет миграции с использованием переданного соединения."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    async with engine.begin() as connection:  # Используйте engine.begin(), а не engine.connect()
        await connection.run_sync(do_run_migrations)

# Запуск миграций
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())