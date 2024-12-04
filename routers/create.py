import secrets

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keys import Keyboards, ServerTypeSelect, LocationTypeSelect, ImageTypeSelect
from language import MessageText
from api import HetznerAPI

router = Router(name="create")


@router.callback_query(LocationTypeSelect.filter(F.is_select.is_(False)))
async def show_location_types(callback: CallbackQuery):
    location_types = await HetznerAPI.get_datacenters()

    if not location_types:
        return await callback.answer(MessageText.NOT_FOUND)

    return await callback.message.edit_text(
        text=MessageText.SELECT_LOCATION_TYPE,
        reply_markup=Keyboards.location_types(location_types),
    )


@router.callback_query(LocationTypeSelect.filter(F.is_select.is_(True)))
async def show_server_types(
    callback: CallbackQuery, state: FSMContext, callback_data: LocationTypeSelect
):
    await state.update_data(location=callback_data.location)

    location_server_types = await HetznerAPI.get_datacenter(callback_data.location)

    if not location_server_types:
        return await callback.answer(MessageText.NOT_FOUND)

    return await callback.message.edit_text(
        text=MessageText.SELECT_SERVER_TYPE,
        reply_markup=Keyboards.server_types(
            location_server_types.server_types.available
        ),
    )


@router.callback_query(ServerTypeSelect.filter(F.is_select.is_(True)))
async def select_server_types(
    callback: CallbackQuery, state: FSMContext, callback_data: ServerTypeSelect
):
    await state.update_data(server=callback_data.server)

    server_select = await HetznerAPI.get_server_type(int(callback_data.server))
    image_types = await HetznerAPI.get_images(arch=server_select.architecture)

    if not image_types:
        return await callback.answer(MessageText.NOT_FOUND)

    return await callback.message.edit_text(
        text=MessageText.SELECT_IMAGE_TYPE,
        reply_markup=Keyboards.image_types(image_types),
    )


@router.callback_query(ImageTypeSelect.filter(F.is_select.is_(True)))
async def select_image_type(
    callback: CallbackQuery, state: FSMContext, callback_data: ImageTypeSelect
):
    data = await state.get_data()

    server_create = await HetznerAPI.create_server(
        name=secrets.token_hex(2),
        server_type=await HetznerAPI.get_server_type(int(data["server"])),
        image=await HetznerAPI.get_image(int(callback_data.image)),
    )

    if not server_create:
        return await callback.answer(MessageText.CHECK_LOGS)

    return await callback.message.edit_text(
        text=MessageText.SERVER_CREATED, reply_markup=Keyboards.home()
    )
