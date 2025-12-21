import logging
from typing import Optional, Annotated

from eiogram.state import StateManager
from eiogram.types import Update
from eiogram.utils.depends import Depends
from hcloud import Client as hcloud_client

from src.db import AsyncSession, Client, User, UserMessage


async def clear_state(db: AsyncSession, state: StateManager) -> None:
    await state.clear_state(db=db)


async def get_hetzner(db: AsyncSession, state_data: dict) -> Optional[hcloud_client]:
    client_id = state_data.get("client_id")
    if client_id is None:
        logging.warning("Dependency injection failed: No client_id found in state data.")
        return None
    client = await Client.get_by_id(db, client_id)
    if not client:
        logging.warning(f"Dependency injection failed: Client not found for client_id: {client_id}")
        return None
    return hcloud_client(token=client.secret)


async def should_be_owner(update: Update, dbuser: User, db: AsyncSession) -> None:
    if not dbuser.is_owner:
        if update.callback_query:
            await update.callback_query.answer("Access Denied", show_alert=True)
        elif update.message:
            _update = await update.message.answer("Access Denied", reply_markup=None)
            await UserMessage.clear(_update)
        raise Exception("Access Denied")


GetHetzner = Annotated[Optional[hcloud_client], Depends(get_hetzner)]
ClearState = Annotated[None, Depends(clear_state)]
ShouldBeOwner = Annotated[None, Depends(should_be_owner)]
