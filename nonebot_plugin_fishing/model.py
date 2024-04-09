from nonebot_plugin_orm import Model
from sqlalchemy import String, TEXT
from sqlalchemy.orm import Mapped, mapped_column


class FishingRecord(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(32))
    time: Mapped[int]
    frequency: Mapped[int]
    fishes: Mapped[str] = mapped_column(TEXT)
    coin: Mapped[int] = mapped_column(default=0)
