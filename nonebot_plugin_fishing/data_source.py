import random
import time
import json

from sqlalchemy import select, update, delete
from sqlalchemy.sql.expression import func
from nonebot_plugin_orm import get_session

from .config import config
from .model import FishingRecord, SpecialFishes

fishing_coin_name = config.fishing_coin_name


def choice() -> tuple:
    config_fishes = config.fishes
    weights = [weight["weight"] for weight in config_fishes]
    choices = random.choices(
        config_fishes,
        weights=weights,
    )
    return choices[0]["name"], choices[0]["frequency"]


def get_price(fish_name: str) -> int:
    """获取鱼的价格"""
    config_fishes = config.fishes
    return next(
        (
            fish["price"]
            for fish in config_fishes
            if fish["name"] == fish_name
        ),
        0
    )


async def random_get_a_special_fish() -> str:
    """随机返回一条别人放生的鱼"""
    session = get_session()
    async with session.begin():
        random_select = select(SpecialFishes).order_by(func.random())
        data = await session.scalar(random_select)
        return data.fish


async def can_fishing(user_id: str) -> bool:
    """判断是否可以钓鱼"""
    time_now = int(time.time())
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        record = await session.scalar(select_user)
        return True if not record else record.time < time_now


def can_free_fish() -> bool:
    return config.special_fish_enabled


async def save_fish(user_id: str, fish_name: str) -> None:
    """向数据库写入鱼以持久化保存"""
    time_now = int(time.time())
    fishing_limit = config.fishing_limit
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        record = await session.scalar(select_user)
        if record:
            loads_fishes = json.loads(record.fishes)
            try:
                loads_fishes[fish_name] += 1
            except KeyError:
                loads_fishes[fish_name] = 1
            dump_fishes = json.dumps(loads_fishes)
            user_update = update(FishingRecord).where(
                FishingRecord.user_id == user_id
            ).values(
                time=time_now + fishing_limit,
                frequency=record.frequency + 1,
                fishes=dump_fishes
            )
            await session.execute(user_update)
            await session.commit()
            return
        data = {
            fish_name: 1
        }
        dump_fishes = json.dumps(data)
        new_record = FishingRecord(
            user_id=user_id,
            time=time_now + fishing_limit,
            frequency=1,
            fishes=dump_fishes,
            special_fishes="{}",
            coin=0
        )
        session.add(new_record)
        await session.commit()


async def can_catch_special_fish():
    session = get_session()
    async with session.begin():
        records = await session.execute(select(SpecialFishes))
        return len(records.all()) != 0 and random.random() <= config.special_fish_probability


async def save_special_fish(user_id: str, fish_name: str) -> None:
    time_now = int(time.time())
    fishing_limit = config.fishing_limit
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        record = await session.scalar(select_user)
        if record:
            loads_fishes = json.loads(record.special_fishes)
            try:
                loads_fishes[fish_name] += 1
            except KeyError:
                loads_fishes[fish_name] = 1
            dump_fishes = json.dumps(loads_fishes)
            user_update = update(FishingRecord).where(
                FishingRecord.user_id == user_id
            ).values(
                time=time_now + fishing_limit,
                frequency=record.frequency + 1,
                special_fishes=dump_fishes
            )
            await session.execute(user_update)
        else:
            data = {
                fish_name: 1
            }
            dump_fishes = json.dumps(data)
            new_record = FishingRecord(
                user_id=user_id,
                time=time_now + fishing_limit,
                frequency=1,
                fishes="{}",
                special_fishes=dump_fishes,
                coin=0
            )
            session.add(new_record)
        select_fish = select(SpecialFishes).where(
            SpecialFishes.fish == fish_name
        ).order_by(SpecialFishes.id).limit(1)
        record = await session.scalar(select_fish)
        fish_id = record.id
        delete_fishes = delete(SpecialFishes).where(SpecialFishes.id == fish_id)
        await session.execute(delete_fishes)
        await session.commit()


async def get_stats(user_id: str) -> str:
    """获取钓鱼统计信息"""
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishing_record = await session.scalar(select_user)
        if fishing_record:
            return f"你钓鱼了 {fishing_record.frequency} 次"
        return "你还没有钓过鱼，快去钓鱼吧"


def print_backpack(backpack: dict, special_backpack=None) -> str:
    """输出背包内容"""
    result = [
        f"{fish_name}×{str(quantity)}"
        for fish_name, quantity in backpack.items()
    ]
    if special_backpack:
        special_result = [
            f"{fish_name}×{str(quantity)}"
            for fish_name, quantity in special_backpack.items()
        ]
        return "背包:\n" + "\n".join(result) + "\n\n特殊鱼:\n" + "\n".join(special_result)
    return "背包:\n" + "\n".join(result)


async def get_backpack(user_id: str) -> str:
    """从数据库查询背包内容"""
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishes_record = await session.scalar(select_user)
        if fishes_record:
            load_fishes = json.loads(fishes_record.fishes)
            load_special_fishes = json.loads(fishes_record.special_fishes)
            if load_special_fishes:
                return print_backpack(load_fishes, load_special_fishes)
            return "你的背包里空无一物" if load_fishes == {} else print_backpack(load_fishes)
        return "你的背包里空无一物"


async def sell_fish(user_id: str, fish_name: str, quantity: int = 1) -> str:
    """
    卖鱼

    参数：
      - user_id: 用户标识符
      - fish_name: 将要卖鱼的鱼名称
      - quantity: 卖出鱼的数量

    返回：
      - (str): 回复的文本
    """
    if quantity <= 0:
        return "你在卖什么 w(ﾟДﾟ)w"
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishes_record = await session.scalar(select_user)
        if fishes_record := fishes_record:
            loads_fishes = json.loads(fishes_record.fishes)
            if fish_name in loads_fishes and loads_fishes[fish_name] > 0:
                fish_price = get_price(fish_name)
                if loads_fishes[fish_name] < quantity:
                    return f"{fish_name} 太少了!"
                loads_fishes[fish_name] -= quantity
                if loads_fishes[fish_name] == 0:
                    del loads_fishes[fish_name]
                dump_fishes = json.dumps(loads_fishes)
                user_update = update(FishingRecord).where(
                    FishingRecord.user_id == user_id
                ).values(
                    coin=fishes_record.coin + fish_price * quantity,
                    fishes=dump_fishes
                )
                await session.execute(user_update)
                await session.commit()
                return (f"你以 {fish_price} {fishing_coin_name} / 条的价格卖出了 {quantity} 条 {fish_name}, "
                        f"你获得了 {fish_price * quantity} {fishing_coin_name}")
            return "查无此鱼"
        else:
            return "还没钓鱼就想卖鱼?"


async def get_balance(user_id: str) -> str:
    """获取余额"""
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishes_record = await session.scalar(select_user)
        if fishes_record:
            return f"你有 {fishes_record.coin} {fishing_coin_name}"
        return "你什么也没有 :)"


async def free_fish(user_id: str, fish_name: str) -> str:
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishes_record = await session.scalar(select_user)
        if fishes_record:
            user_coin = fishes_record.coin
            if user_coin < config.special_fish_price:
                special_fish_coin_less = str(config.special_fish_price - fishes_record.coin)
                return f"你没有足够的 {fishing_coin_name}, 还需 {special_fish_coin_less} {fishing_coin_name}"
            user_coin -= config.special_fish_price
            new_record = SpecialFishes(
                user_id=user_id,
                fish=fish_name
            )
            session.add(new_record)
            user_update = update(FishingRecord).where(
                FishingRecord.user_id == user_id
            ).values(
                coin=user_coin
            )
            await session.execute(user_update)
            await session.commit()
            return f"你花费 {config.special_fish_price} {fishing_coin_name} 放生了 {fish_name}, 未来或许会被有缘人钓到呢"
        return "你甚至还没钓过鱼"


async def lottery(user_id: str) -> str:
    """算法来自于 https://github.com/fossifer/minesweeperbot/blob/master/cards.py"""
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        fishes_record = await session.scalar(select_user)
        if fishes_record:
            user_coin = fishes_record.coin
            if user_coin <= 0:
                return f"你只有 {user_coin} {fishing_coin_name}, 不足以祈愿"
            new_coin = abs(user_coin) / 3
            new_coin = random.randrange(5000, 15000) / 10000 * new_coin
            new_coin = int(new_coin) if new_coin > 1 else 1
            new_coin *= random.randrange(-1, 2, 2)
            user_update = update(FishingRecord).where(
                FishingRecord.user_id == user_id
            ).values(
                coin=fishes_record.coin + new_coin,
            )
            await session.execute(user_update)
            await session.commit()
            return f'你{"获得" if new_coin >= 0 else "血亏"}了 {abs(new_coin)} {fishing_coin_name}'


async def give(user_id: str, fish_name: str, quantity: int = 1) -> str:
    session = get_session()
    async with session.begin():
        select_user = select(FishingRecord).where(FishingRecord.user_id == user_id)
        record = await session.scalar(select_user)
        if record:
            loads_fishes = json.loads(record.fishes)
            try:
                loads_fishes[fish_name] += quantity
            except KeyError:
                loads_fishes[fish_name] = quantity
            dump_fishes = json.dumps(loads_fishes)
            user_update = update(FishingRecord).where(
                FishingRecord.user_id == user_id
            ).values(
                fishes=dump_fishes
            )
            await session.execute(user_update)
            await session.commit()
            return f"使用滥权之力成功使 {fish_name} 添加到 {user_id} 的背包之中 ヾ(≧▽≦*)o"
        return "未查找到用户信息, 无法执行滥权操作 w(ﾟДﾟ)w"
