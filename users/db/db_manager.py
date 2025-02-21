from db.db_manager import BaseDB
from users.db.models import User
from sqlalchemy import select, desc,delete, and_, not_


class UserDB(BaseDB):

    @staticmethod
    async def get_or_create_user(user_id: int, username: str = None):
        """Получает или создаёт пользователя."""
        async def _get_or_create_user(session):
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().first()
            if not user:
                user = User(user_id=user_id, username=username)
                session.add(user)
                await session.commit()
                await session.refresh(user)
            return user

        return await BaseDB.execute_with_session(_get_or_create_user)
