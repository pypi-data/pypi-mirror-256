import asyncio
from distutils.core import setup_keywords
import os
import importlib
from re import A
import ujson as json

from tooldelta.color_print import Print

# 定义插件处理函数列表
player_message_funcs = []
player_join_funcs = []
player_left_funcs = []
repeat_funcs = {}
init_plugin_funcs = []


def player_message():
    def decorator(func):
        player_message_funcs.append(func)
        return func

    return decorator


def player_join():
    def decorator(func):
        player_join_funcs.append(func)
        return func

    return decorator


def player_left():
    def decorator(func):
        player_left_funcs.append(func)
        return func

    return decorator


def repeat(*args):
    def decorator(func):
        repeat_funcs[func] = args[0]
        return func

    return decorator


def init():
    def decorator(func):
        init_plugin_funcs.append(func)
        return func

    return decorator


# repeat_task
def repeat_task(func, time):
    while True:
        asyncio.sleep(time)
        # 防止出错
        try:
            func()
        except Exception as e:
            Print.print_err(f"repeat_task error: {e}")

async def execute_repeat():
    # 为字典每一个函数创建一个循环特定时间的任务
    for func, time in repeat_funcs.items():
        asyncio.create_task(repeat_task(func, time))  # 创建任务
    # 并发执行所有任务
    await asyncio.gather(*asyncio.all_tasks())


# 处理玩家消息并执行插件
async def execute_player_message(playername, message):
    tasks = [func(message, playername) for func in player_message_funcs]
    await asyncio.gather(*tasks)


async def execute_player_join(playername):
    tasks = [func(playername) for func in player_join_funcs]
    await asyncio.gather(*tasks)


async def execute_player_left(playername):
    tasks = [func(playername) for func in player_left_funcs]
    await asyncio.gather(*tasks)


async def load_plugin_file(file):
    # 导入插件模块
    module_name = file
    plugin_module = importlib.import_module(f"插件文件.ToolDelta注入式插件.{module_name}")
    # 获取插件元数据
    return getattr(plugin_module, "__plugin_meta__", create_plugin_metadata({"name":module_name}))

class PluginMetadata:
    def __init__(
        self,
        name,
        author,
        description,
        version,
        usage,
        homepage,
    ):
        self.name = name
        self.author = author
        self.description = description
        self.usage = usage
        self.version = version
        self.homepage = homepage


def create_plugin_metadata(metadata_dict: dict):
    """
    创建插件元数据。

    参数:
        - metadata_dict (dict): 包含插件元数据的字典.

    返回:
        PluginMetadata: 插件元数据对象.
    """
    name = metadata_dict.get("name", "未命名插件")
    version = metadata_dict.get("version", "1.0")
    description = metadata_dict.get("description", "未知插件")
    usage = metadata_dict.get("usage", "")
    author = metadata_dict.get("author", "未知")
    homepage = metadata_dict.get("homepage", "")

    return PluginMetadata(name, author, description, version, usage, homepage)

async def load_plugin(plugin_grp):
    tasks = []

    # 读取本目录下的文件夹名字
    PLUGIN_PATH = os.path.join(os.getcwd(), "插件文件", "ToolDelta注入式插件")
    for file in os.listdir(PLUGIN_PATH):
        if os.path.isdir(os.path.join(PLUGIN_PATH, file)):
            plugin_grp.injected_plugin_loaded_num += 1
            task = asyncio.create_task(load_plugin_file(file))
            tasks.append(task)

    # 并发地加载插件并收集插件元数据
    all_plugin_metadata = await asyncio.gather(*tasks)

    # 打印所有插件的元数据
    for metadata in all_plugin_metadata:
        Print.print_suc(
                f"成功载入插件 {metadata.name} 版本:{metadata.version} 作者:{metadata.author}"
        )


