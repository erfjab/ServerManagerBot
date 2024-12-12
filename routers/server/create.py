import secrets

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keys import Keyboards, SelectCB, Pages, Actions, PageCB, ServerCreate
from language import MessageText
from api import HetznerManager

router = Router(name="server_create")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVER)) & (F.action.is_(Actions.CREATE)))
)
async def show_location_types(callback: CallbackQuery, key: str | None):
    location_types = await HetznerManager.get_datacenters(key)

    if not location_types:
        return await callback.answer(MessageText.NOT_FOUND)

    return await callback.message.edit_text(
        text=MessageText.SELECT_LOCATION_TYPE,
        reply_markup=Keyboards.location_types(key, location_types),
    )


@router.callback_query(
    SelectCB.filter(
        (F.page.is_(Pages.SERVER))
        & (F.action.is_(Actions.CREATE))
        & (F.datatype.is_(ServerCreate.LOCATION))
    )
)
async def show_server_types(
    callback: CallbackQuery, state: FSMContext, callback_data: SelectCB, key: str | None
):
    await state.update_data(location=callback_data.datavalue)

    location_server_types = await HetznerManager.get_datacenter(
        key, callback_data.datavalue
    )

    if not location_server_types:
        return await callback.answer(MessageText.NOT_FOUND)

    return await callback.message.edit_text(
        text=MessageText.SELECT_SERVER_TYPE,
        reply_markup=Keyboards.server_types(
            key, location_server_types.server_types.available
        ),
    )


@router.callback_query(
    SelectCB.filter(
        (F.page.is_(Pages.SERVER))
        & (F.action.is_(Actions.CREATE))
        & (F.datatype.is_(ServerCreate.SERVER))
    )
)
async def select_server_types(
    callback: CallbackQuery, state: FSMContext, callback_data: SelectCB, key: str | None
):
    await state.update_data(server=callback_data.datavalue)

    server_select = await HetznerManager.get_server_type(
        key, int(callback_data.datavalue)
    )
    image_types = await HetznerManager.get_images(key, arch=server_select.architecture)

    if not image_types:
        return await callback.answer(MessageText.NOT_FOUND)

    return await callback.message.edit_text(
        text=MessageText.SELECT_IMAGE_TYPE,
        reply_markup=Keyboards.image_types(key, image_types),
    )


@router.callback_query(
    SelectCB.filter(
        (F.page.is_(Pages.SERVER))
        & (F.action.is_(Actions.CREATE))
        & (F.datatype.is_(ServerCreate.IMAGE))
    )
)
async def select_image_type(
    callback: CallbackQuery, state: FSMContext, callback_data: SelectCB, key: str | None
):
    data = await state.get_data()

    server_create = await HetznerManager.create_server(
        key=key,
        name=secrets.token_hex(2),
        server_type=await HetznerManager.get_server_type(key, int(data["server"])),
        image=await HetznerManager.get_image(key, int(callback_data.datavalue)),
    )

    if not server_create:
        return await callback.answer(MessageText.CHECK_LOGS)

    return await callback.message.edit_text(
        text=MessageText.SERVER_CREATED, reply_markup=Keyboards.back_home()
    )
