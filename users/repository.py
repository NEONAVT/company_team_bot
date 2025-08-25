from dataclasses import dataclass
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from users.models import User, Admins


@dataclass
class UsersRepository:
    db_session: AsyncSession

    async def get_user(self, chat_id: int) -> User | None:
        query = select(User).where(User.chat_id == chat_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def register_user(
        self,
        chat_id: int,
        username: str,
        first_name: str,
        access_key: str,
        role: str
    ) -> User:
        existing_user = await self.get_user(chat_id)
        if existing_user:
            return existing_user

        new_user = User(
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            access_key=access_key,
            role=role,
        )

        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
        return new_user

    async def grant_admin_permissions(
        self,
        user_id: int,
        role: str
    ) -> User | None:
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(role=role)
            .returning(User)
        )
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.scalar_one_or_none()

    async def add_admin(self, user_id: int, username: str, first_name: str) -> Admins:
        new_admin = Admins(
            user_id=user_id,
            username=username,
            first_name=first_name,
        )
        self.db_session.add(new_admin)
        await self.db_session.commit()
        await self.db_session.refresh(new_admin)
        return new_admin


    async def revoke_admin_permissions(self, user_id: int, role: str):
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(role=role)
            .returning(User)
        )
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        user = result.scalar_one_or_none()
        if not user:
            return None

        query_del = delete(Admins).where(Admins.user_id == user_id)
        await self.db_session.execute(query_del)
        await self.db_session.commit()

        return user

