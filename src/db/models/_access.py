from sqlalchemy import BigInteger, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import Base


class ServerAccess(Base):
    __tablename__ = "server_accesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    server_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    @classmethod
    async def create(cls, db: AsyncSession, *, client_id: int, server_id: int, user_id: int) -> "ServerAccess":
        access = cls(client_id=client_id, server_id=server_id, user_id=user_id)
        db.add(access)
        await db.commit()
        await db.refresh(access)
        return access

    @classmethod
    async def get_all_by_server(cls, db: AsyncSession, client_id: int, server_id: int) -> list["ServerAccess"]:
        result = await db.execute(select(cls).where(cls.client_id == client_id, cls.server_id == server_id))
        return result.scalars().all()

    @classmethod
    async def get_by_user(cls, db: AsyncSession, user_id: int) -> list["ServerAccess"]:
        result = await db.execute(select(cls).where(cls.user_id == user_id))
        return result.scalars().all()

    @classmethod
    async def delete(cls, db: AsyncSession, client_id: int, server_id: int, user_id: int) -> None:
        result = await db.execute(
            select(cls).where(cls.client_id == client_id, cls.server_id == server_id, cls.user_id == user_id)
        )
        access = result.scalars().first()
        if access:
            await db.delete(access)
            await db.commit()
