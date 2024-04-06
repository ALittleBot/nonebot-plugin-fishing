from nonebot import on_command, require

require("nonebot_plugin_orm")  # noqa
from nonebot.plugin import PluginMetadata
from nonebot.adapters import Event, Message
from nonebot.params import CommandArg

import asyncio

from .config import Config
from .data_source import (choice,
                          is_fishing,
                          get_stats,
                          save_fish,
                          get_backpack,
                          sell_fish,
                          get_balance)

__plugin_meta__ = PluginMetadata(
    name="赛博钓鱼",
    description="你甚至可以电子钓鱼",
    usage="发送“钓鱼”，放下鱼竿。",
    type="application",
    homepage="https://github.com/C14H22O/nonebot-plugin-fishing",
    config=Config,
    supported_adapters=None
)

fishing = on_command("fishing", aliases={"钓鱼"}, priority=5)
stats = on_command("stats", aliases={"统计信息"}, priority=5)
backpack = on_command("backpack", aliases={"背包"}, priority=5)
sell = on_command("sell", aliases={"卖鱼"}, priority=5)
balance = on_command("balance", aliases={"余额"}, priority=5)


@fishing.handle()
async def _fishing(event: Event):
    user_id = event.get_user_id()
    if not await is_fishing(user_id):
        await fishing.finish("河累了, 休息一下吧")
    await fishing.send("正在钓鱼…")
    choice_result = choice()
    fish = choice_result[0]
    sleep_time = choice_result[1]
    result = f"钓到了一条{fish}, 你把它收进了背包里"
    await save_fish(user_id, fish)
    await asyncio.sleep(sleep_time)
    await fishing.finish(result)


@stats.handle()
async def _stats(event: Event):
    user_id = event.get_user_id()
    await stats.finish(await get_stats(user_id))


@backpack.handle()
async def _backpack(event: Event):
    user_id = event.get_user_id()
    await backpack.finish(await get_backpack(user_id))


@sell.handle()
async def _sell(event: Event, arg: Message = CommandArg()):
    fish_name = arg.extract_plain_text()
    if fish_name == "":
        await sell.finish("请输入要卖出的鱼的名字, 如 /卖鱼 小鱼")
    user_id = event.get_user_id()
    await sell.finish(await sell_fish(user_id, fish_name))


@balance.handle()
async def _balance(event: Event):
    user_id = event.get_user_id()
    await balance.finish(await get_balance(user_id))
