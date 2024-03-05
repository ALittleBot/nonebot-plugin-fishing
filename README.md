<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-fishing

_✨ 你甚至可以电子钓鱼 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/C14H22O/nonebot-plugin-fishing.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-fishing">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-fishing.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-fishing

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-fishing
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-fishing
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-fishing
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-fishing
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_fishing"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 说明 |
|:-----:|:----:|:----:|
| fishes | 否 | 使用`(名称, 等待时间, 权重)`的格式配置 |
| fishing_limit | 否 | 填入每次钓鱼后，限制钓鱼的秒数 |

## 🎉 使用
### 指令表
| 指令 | 范围 | 说明 |
|:-----:|:----:|:----:|
| 钓鱼 | 所有 | 放下鱼竿 |
| 统计信息 | 所有 | 查看钓鱼次数 |
| 背包 | 所有 | 查看背包 |
