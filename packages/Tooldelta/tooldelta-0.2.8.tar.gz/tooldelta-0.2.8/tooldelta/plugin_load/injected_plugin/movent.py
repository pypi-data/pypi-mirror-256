from tooldelta.color_print import Print

frame = None
game_control = None

def check_avaliable(sth):
    if sth is None:
        raise AttributeError(f"无法使用 {sth.__class__.__name__}, 因为其还未被初始化")

def set_frame(my_frame):
    # 只有在系统启动后才能获得有效的 frame
    global frame, game_control
    frame = my_frame
    game_control = my_frame.get_game_control()

def sendcmd(*arg):
    check_avaliable(game_control)
    game_control.sendcmd(*arg)


def sendwscmd(*arg):
    check_avaliable(game_control)
    game_control.sendwscmd(*arg)


def sendwocmd(*arg):
    check_avaliable(game_control)
    game_control.sendwocmd(*arg)


def sendPacket(*arg):
    check_avaliable(game_control)
    game_control.sendPacket(*arg)


def sendPacketJson(*arg):
    # tip: 和sendPacket已经是同一个东西了
    check_avaliable(game_control)
    game_control.sendPacketJson(*arg)


def sendfbcmd(*arg):
    # 在除FastBuilder外的其他启动器上不可用
    check_avaliable(game_control)
    game_control.sendfbcmd(*arg)


def tellrawText(playername: str, title: str | None = None, text: str = ""):
    """
    发送tellraw消息
    ---
    playername:str 玩家名.
    title:str 说话人.
    text:str 内容.
    """
    if title is None:
        sendcmd(r"""/tellraw %s {"rawtext":[{"text":"§r%s"}]}""" % (playername, text))
    else:
        sendcmd(
            r"""/tellraw %s {"rawtext":[{"text":"<%s> §r%s"}]}"""
            % (
                playername,
                title,
                text,
            )
        )

def get_all_player():
    check_avaliable(game_control)
    Print.print_suc(game_control.allplayers)
    return game_control.allplayers