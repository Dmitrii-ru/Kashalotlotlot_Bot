from sqlalchemy.exc import SQLAlchemyError
from .db_postgres_settings import async_session, engine, Base

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        print("Таблицы созданы!")


class BaseDB:
    """Базовый класс для работы с базой данных."""

    @staticmethod
    async def get_session():
        """Возвращает асинхронную сессию."""
        return async_session()

    @staticmethod
    async def execute_with_session(func):
        """Выполняет функцию с автоматическим управлением сессией."""
        async with async_session() as session:
            try:
                result = await func(session)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                print(f"Ошибка при работе с базой данных: {e}")
                return None
            finally:
                await session.close()