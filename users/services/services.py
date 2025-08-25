import secrets
import string
from dataclasses import dataclass
from database import AsyncSessionLocal
from users.repository import UsersRepository
import logging
from settings import settings

logger = logging.getLogger(__name__)

@dataclass
class UsersService:

    def generate_access_key(self) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(24))

    async def register_guest(self, chat_id: int, username: str, first_name: str):
        try:
            async with AsyncSessionLocal() as session:
                repo = UsersRepository(session)
                user = await repo.register_user(
                    chat_id=chat_id,
                    username=username,
                    first_name=first_name,
                    access_key=None,
                    role=settings.GUEST_ROLE,
                )
                return user
        except Exception:
            logger.exception("Ошибка при регистрации гостя")
            return None

    async def update_user(self, chat_id: int):
        try:
            async with AsyncSessionLocal() as session:
                repo = UsersRepository(session)
                user = await repo.get_user(chat_id)
                if not user:
                    return None
                updated = await repo.update_user_role(
                    user_id=user.user_id,
                    role=settings.USER_ROLE,
                )
                return updated
        except Exception:
            logger.exception("Ошибка обновления пользователя")
            return None

    async def get_user(self, chat_id: int):
        async with AsyncSessionLocal() as session:
            repo = UsersRepository(session)
            return await repo.get_user(chat_id=chat_id)

    async def get_user_by_username(self, username: str):
        async with AsyncSessionLocal() as session:
            repo = UsersRepository(session)
            return await repo.get_user_by_username(username=username)

    async def grant_admin_permissions(self, username: str):
        try:
            async with AsyncSessionLocal() as session:
                repo = UsersRepository(session)
                user = await repo.get_user_by_username(username)
                if not user:
                    return None

                updated = await repo.grant_admin_permissions(
                    user_id=user.user_id,
                    role=settings.MANAGER_ROLE,
                )
                if not updated:
                    return None

                await repo.add_admin(
                    user_id=updated.user_id,
                    username=updated.username,
                    first_name=updated.first_name,
                )
                return updated
        except Exception:
            logger.exception("Ошибка выдачи прав админа")
            return None

    async def revoke_admin_permissions(self, username: str):
        try:
            async with AsyncSessionLocal() as session:
                repo = UsersRepository(session)
                user = await repo.get_user_by_username(username)
                if not user:
                    return None

                updated = await repo.revoke_admin_permissions(
                    user_id=user.user_id,
                    role=settings.USER_ROLE,
                )
                if not updated:
                    return None

                await repo.add_admin(
                    user_id=updated.user_id,
                    username=updated.username,
                    first_name=updated.first_name,
                )
                return updated
        except Exception:
            logger.exception("Ошибка выдачи прав админа")
            return None

users_service = UsersService()
