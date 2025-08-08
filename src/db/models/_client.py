from typing import Optional
from datetime import datetime

from sqlalchemy import String, Integer
from sqlalchemy.future import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession


from ..core import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    remark: Mapped[str] = mapped_column(String(256), index=True, nullable=False)
    secret: Mapped[str] = mapped_column(String(256), index=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def kb_remark(self) -> str:
        return f"{self.remark} [{self.id}]"

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int) -> Optional["Client"]:
        result = await db.execute(select(cls).where(cls.id == int(id)))
        return result.scalars().first()

    @classmethod
    async def get_by_remark(cls, db: AsyncSession, remark: str) -> Optional["Client"]:
        result = await db.execute(select(cls).where(cls.remark == remark))
        return result.scalars().first()

    @classmethod
    async def get_by_secret(cls, db: AsyncSession, secret: str) -> Optional["Client"]:
        result = await db.execute(select(cls).where(cls.secret == secret))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list["Client"]:
        result = await db.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def create(cls, db: AsyncSession, *, remark: str, secret: str) -> "Client":
        item = cls(remark=remark, secret=secret)
        db.add(item)
        await db.flush()
        return item

    @classmethod
    async def update(
        cls,
        db: AsyncSession,
        id: int,
        *,
        remark: Optional[str] = None,
        secret: Optional[str] = None,
    ) -> Optional["Client"]:
        item = await cls.get_by_id(db, id)
        if not item:
            return None

        if remark is not None:
            item.remark = remark
        if secret is not None:
            item.secret = secret

        await db.flush()
        return item

    @classmethod
    async def remove(cls, db: AsyncSession, id: int) -> bool:
        item = await cls.get_by_id(db, id)
        if not item:
            return False
        await db.delete(item)
        await db.flush()
        return True

    def __repr__(self) -> str:
        return f"<Client(id={self.id})>"
