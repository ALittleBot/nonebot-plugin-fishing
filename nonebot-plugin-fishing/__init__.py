from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters import Event

import asyncio

from .config import Config
from .data_source import (choice,
                          get_fishing,
                          get_stats,
                          save_fish,
                          get_backpack)

__plugin_meta__ = PluginMetadata(
    name="赛博钓鱼",
    description="你甚至可以电子钓鱼",
    usage="发送“钓鱼”",
    type="application",
    homepage="https://github.com/C14H22O/nonebot-plugin-fishing",
    config=Config
)

fishing = on_command("fishing", aliases={"钓鱼"})
stats = on_command("stats", aliases={"统计信息"})
backpack = on_command("backpack", aliases={"背包"})


@fishing.handle()
async def _fishing(event: Event):
    user_id = event.get_user_id()
    if not await get_fishing(user_id):
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
