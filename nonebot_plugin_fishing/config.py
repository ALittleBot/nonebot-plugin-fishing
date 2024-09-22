from pydantic import BaseModel
from typing import List, Dict
from nonebot import get_plugin_config


class Config(BaseModel):
    fishes: List[Dict] = [
        {
            "name": "小鱼",
            "frequency": 2,
            "weight": 100,
            "price": 2
        },
        {
            "name": "尚方宝剑",
            "frequency": 2,
            "weight": 100,
            "price": 1
        },
        {
            "name": "小杂鱼~♡",
            "frequency": 3,
            "weight": 5,
            "price": 100
        },
        {
            "name": "烤激光鱼",
            "frequency": 10,
            "weight": 1,
            "price": 1000
        }
    ]

    fishing_limit: int = 30

    fishing_coin_name: str = "FC"  # It means Fishing Coin.

    special_fish_enabled: bool = False

    special_fish_price: int = 50

    special_fish_probability: float = 0.01

    fishing_achievement: List[Dict] = [
        {
            "type": "fishing_frequency",
            "name": "腥味十足的生意",
            "data": 1,
            "description": "钓到一条鱼。"
        },
        {
            "type": "fishing_frequency",
            "name": "还是钓鱼大佬",
            "data": 100,
            "description": "累计钓鱼一百次。"
        },
        {
            "type": "fish_type",
            "name": "那是鱼吗？",
            "data": "小杂鱼~♡",
            "description": "获得#####。[原文如此]"
        },
        {
            "type": "fish_type",
            "name": "那一晚, 激光鱼和便携式烤炉都喝醉了",
            "data": "烤激光鱼",
            "description": "获得烤激光鱼。"
        }
    ]


config = get_plugin_config(Config)
