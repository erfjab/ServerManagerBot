from .keyboard import KeyboardTextsFile
from .message import MessageTextsFile

MessageText = MessageTextsFile()
KeyboardText = KeyboardTextsFile()

__all__ = ["MessageText", "KeyboardText"]
