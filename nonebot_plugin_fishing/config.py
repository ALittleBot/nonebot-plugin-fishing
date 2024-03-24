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
            "price": 20
        },
        {
            "name": "烤激光鱼",
            "frequency": 10,
            "weight": 1,
            "price": 50
        }
    ]

    fishing_limit: int = 30


config = get_plugin_config(Config)
