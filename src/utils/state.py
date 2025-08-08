from typing import Any, Dict, Optional, Union
from eiogram.state.storage import BaseStorage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import UserState, GetDB


class DatabaseStorage(BaseStorage):
    async def _get_or_create(self, key: Union[int, str], db: AsyncSession) -> UserState:
        stmt = await db.execute(select(UserState).where(UserState.id == key))
        user = stmt.scalar_one_or_none()
        if not user:
            user = UserState(id=key, state=None, data={})
            db.add(user)
            await db.flush()
        return user

    async def get_state(self, key: Union[int, str], db: Optional[AsyncSession] = None) -> Optional[Dict[str, Any]]:
        if db:
            user = await self._get_or_create(key, db)
            return user.state
        else:
            async with GetDB() as db:
                await self.get_state(key, db)

    async def get_context(self, key: Union[int, str], db: Optional[AsyncSession] = None) -> Optional[Dict[str, Any]]:
        if db:
            user = await self._get_or_create(key, db)
            return {"state": user.state, "data": user.data}
        else:
            async with GetDB() as db:
                return await self.get_context(key, db)

    async def upsert_context(
        self,
        key: Union[int, str],
        state: Dict[str, Any],
        db: Optional[AsyncSession] = None,
        **data: Any,
    ) -> Optional[Dict[str, Any]]:
        if db:
            user = await self._get_or_create(key, db)
            user.state = state
            current_data = user.data or {}
            new_data = {**current_data, **data}
            user.data = new_data
            await db.flush()
        else:
            async with GetDB() as db:
                await self.upsert_context(key, state, db, **data)

    async def set_state(
        self,
        key: Union[int, str],
        state: Dict[str, Any],
        db: Optional[AsyncSession] = None,
    ) -> None:
        if db:
            user = await self._get_or_create(key, db)
            user.state = state
            await db.flush()
        else:
            async with GetDB() as db:
                await self.set_state(key, state, db)

    async def upsert_data(self, key: Union[int, str], db: Optional[AsyncSession] = None, **data: Any) -> None:
        if db:
            user = await self._get_or_create(key, db)
            current_data = user.data or {}
            new_data = {**current_data, **data}
            user.data = new_data
            await db.flush()
        else:
            async with GetDB() as db:
                await self.upsert_data(key, db, **data)

    async def get_data(self, key: Union[int, str], db: Optional[AsyncSession] = None) -> Dict[str, Any]:
        if db:
            user = await self._get_or_create(key, db)
            return user.data

        async with GetDB() as db:
            return await self.get_data(key, db)

    async def clear_state(self, key: Union[int, str], db: Optional[AsyncSession] = None) -> None:
        if db:
            user = await self._get_or_create(key, db)
            user.state = None
            await db.flush()
        else:
            async with GetDB() as db:
                await self.clear_state(key, db)

    async def clear_data(self, key: Union[int, str], db: Optional[AsyncSession] = None) -> None:
        if db:
            user = await self._get_or_create(key, db)
            user.data = {}
            await db.flush()
        else:
            async with GetDB() as db:
                await self.clear_data(key, db)

    async def clear_all(self, key: Union[int, str], db: Optional[AsyncSession] = None) -> None:
        if db:
            user = await self._get_or_create(key, db)
            user.data = {}
            user.state = None
            await db.flush()
        else:
            async with GetDB() as db:
                await self.clear_all(key, db)
