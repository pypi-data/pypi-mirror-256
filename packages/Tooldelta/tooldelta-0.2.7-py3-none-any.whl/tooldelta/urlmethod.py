import requests, time, os, platform
from .color_print import Print

def _pretty_kb(n):
        if n >= 1048576:
            return f"{round(n / 1048576, 2)}M"
        elif n >= 1024:
            return f"{round(n / 1024, 2)}K"
        else:
            return f"{round(n, 1)}"

def download_file(f_url: str, f_dir: str):
    res = requests.get(f_url, stream=True, timeout=10)
    filesize = int(res.headers["content-length"])
    if filesize < 256:
        if "404" in res.text:
            raise requests.RequestException("下载失败: 返回 404")
        Print.print_war(f"下载 {f_url} 的文件警告: 文件大小异常, 不到 0.256KB")
    nowsize = 0
    succ = False
    lastime = time.time()
    useSpeed = 0
    try:
        with open(f_dir + ".tmp", "wb") as dwnf:
            for chk in res.iter_content(chunk_size=8192):
                nowtime = time.time()
                if nowtime != lastime:
                    useSpeed = 1024 / (nowtime - lastime)

                prgs = nowsize / filesize
                _tmp = int(prgs * 20)
                bar = Print.colormode_replace(
                    "§f" + " " * _tmp + "§b" + " " * (20 - _tmp) + "§r ", 7
                )
                Print.print_with_info(
                    f"{bar} {round(nowsize / 1024, 2)}KB / {round(filesize / 1024, 2)}KB ({_pretty_kb(useSpeed)}B/s)    ",
                    "§a 下载 §r",
                    end = "\r",
                    need_log = False
                )
                nowsize += len(chk)
                lastime = nowtime

                if chk:
                    dwnf.write(chk)
                    dwnf.flush()
        succ = True
    finally:
        if succ:
            os.rename(f_dir + ".tmp", f_dir)
        else:
            os.remove(f_dir + ".tmp")


def get_free_port(start=8080, end=65535):
    if platform.uname()[0] == "Windows":
        for port in range(start, end):
            r = os.popen(f'netstat -aon|findstr ":{port}"', "r")
            if r.read() == "":
                return port
            else:
                Print.print_war(f"端口 {port} 正被占用, 跳过")
    else:
        for port in range(start, end):
            r = os.popen(f'netstat -aon|grep ":{port}"', "r")
            if r.read() == "":
                return port
            else:
                Print.print_war(f"端口 {port} 正被占用, 跳过")
    raise Exception(f"未找到空闲端口({start}~{end})")
