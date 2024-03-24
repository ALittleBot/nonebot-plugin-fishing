from nonebot_plugin_orm import Model
from sqlalchemy.orm import Mapped, mapped_column


class FishingRecord(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    time: Mapped[int]
    frequency: Mapped[int]
    fishes: Mapped[str]
    coin: Mapped[int]
