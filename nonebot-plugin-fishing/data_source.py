from nonebot import get_plugin_config
from nonebot import require
from nonebot.log import logger

require("nonebot_plugin_localstore")  # noqa
import nonebot_plugin_localstore as store

import random
import time
import json
from os.path import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import update

from .config import Config
from .model import Base
from .model import FishingRecord, FishingBackpack

plugin_config = get_plugin_config(Config)


def choice() -> tuple:
    config_fishes = plugin_config.fishes
    weights = [weight[2] for weight in config_fishes]
    choices = random.choices(
        config_fishes,
        weights=weights,
    )
    return choices[0][0], choices[0][1]


data_path = str(store.get_data_file("fishing", "data.db"))
async_engine = create_async_engine("sqlite+aiosqlite:///" + data_path)
async_session = sessionmaker(class_=AsyncSession, bind=async_engine)  # noqa
engine = create_engine("sqlite:///" + data_path)


def init_database():
    logger.info("正在初始化数据库…")
    Base.metadata.create_all(engine)


if not exists(data_path):
    init_database()
else:
    logger.info(f"使用 {data_path} 的数据库")


async def get_fishing(user_id: str) -> bool:
    time_now = int(time.time())
    fishing_limit = plugin_config.fishing_limit
    async with async_session() as session:
        records = await session.execute(select(FishingRecord))
        for record in records.scalars():
            if record.user_id == user_id:
                if record.time >= time_now:
                    return False
                user_update = update(FishingRecord).where(FishingRecord.user_id == user_id).values(
                    time=time_now + fishing_limit,
                    frequency=record.frequency + 1
                )
                await session.execute(user_update)
                await session.commit()
                return True
        else:
            new_record = FishingRecord(
                user_id=user_id,
                time=time_now + fishing_limit,
                frequency=1
            )
            session.add(new_record)
            await session.commit()
            return True


async def save_fish(user_id: str, fish_name: str) -> None:
    async with async_session() as session:
        records = await session.execute(select(FishingBackpack))
        for record in records.scalars():
            if record.user_id == user_id:
                loads_fishes = json.loads(record.fishes)
                try:
                    loads_fishes[fish_name] += 1
                except KeyError:
                    loads_fishes[fish_name] = 1
                dump_fishes = json.dumps(loads_fishes)
                user_update = update(FishingBackpack).where(FishingBackpack.user_id == user_id).values(
                    fishes=dump_fishes
                )
                await session.execute(user_update)
                await session.commit()
                return
        data = {
            fish_name: 1
        }
        dump_fishes = json.dumps(data)
        new_record = FishingBackpack(
            user_id=user_id,
            fishes=dump_fishes
        )
        session.add(new_record)
        await session.commit()


async def get_stats(user_id: str) -> str:
    async with async_session() as session:
        fishing_records = await session.execute(select(FishingRecord))
        for fishing_record in fishing_records.scalars():
            if fishing_record.user_id == user_id:
                return f"你钓鱼了 {fishing_record.frequency} 次\n"
        return "你还没有钓过鱼, 快去钓鱼吧"


def print_backpack(backpack: dict) -> str:
    _ = "\n"
    result = [fish_name + "×" + str(quantity)
              for fish_name, quantity in backpack.items()]
    return "背包:\n" + _.join(result)


async def get_backpack(user_id: str) -> str:
    async with async_session() as session:
        fishes_records = await session.execute(select(FishingBackpack))
        for fishes_record in fishes_records.scalars():
            if fishes_record.user_id == user_id:
                load_fishes = json.loads(fishes_record.fishes)
                return print_backpack(load_fishes)
        return "你的背包里空无一物"
