from pydantic import BaseModel


class Config(BaseModel):
    """
    (名称, 等待时间, 权重)
    """
    fishes: list = [
        ("小鱼", 2, 10),
        ("尚方宝剑", 2, 10),
        ("小杂鱼~♡", 3, 5),
        ("烤激光鱼", 10, 1)
    ]
    fishing_limit: int = 30
