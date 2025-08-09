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
        return None
    clinet = await Client.get_by_id(db, client_id)
    if not clinet:
        return None
    return hcloud_client(token=clinet.secret)


GetHetzner = Annotated[Optional[hcloud_client], Depends(get_hetzner)]
ClearState = Annotated[None, Depends(clear_state)]
