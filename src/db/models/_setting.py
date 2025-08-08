from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..core import Base


class Setting(Base):
    __tablename__ = "setting"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
