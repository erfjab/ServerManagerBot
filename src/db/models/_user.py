import logging
from datetime import datetime
from typing import Optional, Union
from eiogram.types import User as EioUser, Message, CallbackQuery
from sqlalchemy import String, BigInteger, DateTime, Integer, Text, JSON
from sqlalchemy.sql import select, delete
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property

from src.config import BOT, TELEGRAM_ADMINS_ID
from ..core import Base, GetDB

logger = logging.getLogger(__name__)


class UserState(Base):
    __tablename__ = "user_states"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    state: Mapped[str] = mapped_column(Text, nullable=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<UserState(id={self.id})>"


class UserMessage(Base):
    __tablename__ = "user_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    message_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now(), nullable=False)

    @classmethod
    async def _get_chat_id(cls, update: Union[Message, CallbackQuery]) -> int:
        message = update.message if isinstance(update, CallbackQuery) else update
        return message.chat.id

    @classmethod
    async def add(cls, update: Union[Message, CallbackQuery]) -> None:
        async with GetDB() as db:
            message = update.message if isinstance(update, CallbackQuery) else update
            db.add(UserMessage(chat_id=message.chat.id, message_id=message.message_id))

    @classmethod
    async def clear(cls, update: Union[Message, CallbackQuery], *, keep_current: bool = False) -> None:
        async with GetDB() as db:
            chat_id = await cls._get_chat_id(update)
            message_id = getattr(
                update.message if isinstance(update, CallbackQuery) else update,
                "message_id",
                None,
            )
            delete_condition = UserMessage.chat_id == chat_id
            if keep_current and message_id:
                delete_condition &= UserMessage.message_id != message_id
            messages = await db.execute(select(UserMessage.message_id).where(delete_condition))
            message_ids = [msg[0] for msg in messages.all()]
            if message_ids:
                try:
                    await BOT.delete_messages(chat_id=chat_id, message_ids=message_ids)
                except Exception as e:
                    logger.warning(f"Failed to delete messages: {e}")
            await db.execute(delete(UserMessage).where(delete_condition))
            message = update.message if isinstance(update, CallbackQuery) else update
            db.add(UserMessage(chat_id=message.chat.id, message_id=message.message_id))

    def __repr__(self) -> str:
        return f"<UserMessage(id={self.id})>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(256), nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    join_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    online_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    @hybrid_property
    def has_access(self) -> bool:
        return self.id in TELEGRAM_ADMINS_ID

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int) -> Optional["User"]:
        result = await db.execute(select(cls).where(cls.id == id))
        user = result.scalars().first()
        return user

    @classmethod
    async def upsert(cls, db: AsyncSession, *, user: EioUser) -> Optional["User"]:
        dbuser = await cls.get_by_id(db, user.id)
        if dbuser:
            dbuser.full_name = user.full_name
            dbuser.username = user.username
            dbuser.online_at = datetime.now()
        else:
            dbuser = cls(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
            )
            db.add(dbuser)
        await db.flush()
        return dbuser

    def __repr__(self) -> str:
        return f"<User(id={self.id})>"
