import random
import time
import json
from sqlalchemy import select
from sqlalchemy import update
from nonebot_plugin_orm import get_session

from .config import config
from .model import FishingRecord


def choice() -> tuple:
    config_fishes = config.fishes
    weights = [weight["weight"] for weight in config_fishes]
    choices = random.choices(
        config_fishes,
        weights=weights,
    )
    return choices[0]["name"], choices[0]["frequency"]


async def is_fishing(user_id: str) -> bool:
    time_now = int(time.time())
    session = get_session()
    async with session.begin():
        records = await session.execute(select(FishingRecord))
        for record in records.scalars():
            if record.user_id == user_id:
                if record.time >= time_now:
                    return False
                return True
        else:
            return True


async def save_fish(user_id: str, fish_name: str) -> None:
    time_now = int(time.time())
    fishing_limit = config.fishing_limit
    session = get_session()
    async with session.begin():
        records = await session.execute(select(FishingRecord))
        for record in records.scalars():
            if record.user_id == user_id:
                loads_fishes = json.loads(record.fishes)
                try:
                    loads_fishes[fish_name] += 1
                except KeyError:
                    loads_fishes[fish_name] = 1
                dump_fishes = json.dumps(loads_fishes)
                user_update = update(FishingRecord).where(FishingRecord.user_id == user_id).values(
                    time=time_now + fishing_limit,
                    frequency=record.frequency + 1,
                    fishes=dump_fishes
                )
                await session.execute(user_update)
                await session.commit()
                return
        else:
            data = {
                fish_name: 1
            }
            dump_fishes = json.dumps(data)
            new_record = FishingRecord(
                user_id=user_id,
                time=time_now + fishing_limit,
                frequency=1,
                fishes=dump_fishes,
                coin=0
            )
            session.add(new_record)
            await session.commit()


async def get_stats(user_id: str) -> str:
    session = get_session()
    async with session.begin():
        fishing_records = await session.execute(select(FishingRecord))
        for fishing_record in fishing_records.scalars():
            if fishing_record.user_id == user_id:
                return f"你钓鱼了 {fishing_record.frequency} 次"
        return "你还没有钓过鱼, 快去钓鱼吧"


def print_backpack(backpack: dict) -> str:
    _ = "\n"
    result = [fish_name + "×" + str(quantity)
              for fish_name, quantity in backpack.items()]
    return "背包:\n" + _.join(result)


async def get_backpack(user_id: str) -> str:
    session = get_session()
    async with session.begin():
        fishes_records = await session.execute(select(FishingRecord))
        for fishes_record in fishes_records.scalars():
            if fishes_record.user_id == user_id:
                load_fishes = json.loads(fishes_record.fishes)
                return print_backpack(load_fishes)
        return "你的背包里空无一物"
