import logging
from typing import Optional, Annotated

from eiogram.state import StateManager
from eiogram.utils.depends import Depends
from hcloud import Client as hcloud_client

from src.db import AsyncSession, Client


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


GetHetzner = Annotated[Optional[hcloud_client], Depends(get_hetzner)]
ClearState = Annotated[None, Depends(clear_state)]
