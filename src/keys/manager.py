from eiogram.types import InlineKeyboardMarkup
from eiogram.utils.inline_builder import InlineKeyboardBuilder

from src.lang import Buttons


class BotKB:
    @classmethod
    def home(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(text=Buttons.OWNER, url="https://t.me/erfjabs")
        kb.adjust(1)
        return kb.as_markup()
