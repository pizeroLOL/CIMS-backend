import msvcrt
import sys
import os
import json
from string import whitespace

# columns, lines = os.get_terminal_size()

BLACK_CHARACTER = "\033[30m"
RED_CHARACTER = "\033[31m"
GREEN_CHARACTER = "\033[32m"
YELLOW_CHARACTER = "\033[33m"
BLUE_CHARACTER = "\033[34m"
MAGENTA_CHARACTER = "\033[35m"
CYAN_CHARACTER = "\033[36m"
WHITE_CHARACTER = "\033[37m"

BLACK_BACKGROUND = "\033[40m"
RED_BACKGROUND = "\033[41m"
GREEN_BACKGROUND = "\033[42m"
YELLOW_BACKGROUND = "\033[43m"
BLUE_BACKGROUND = "\033[44m"
MAGENTA_BACKGROUND = "\033[45m"
CYAN_BACKGROUND = "\033[46m"
WHITE_BACKGROUND = "\033[47m"

BRIGHT_BLACK_CHARACTER = "\033[90m"
BRIGHT_RED_CHARACTER = "\033[91m"
BRIGHT_GREEN_CHARACTER = "\033[92m"
BRIGHT_YELLOW_CHARACTER = "\033[93m"
BRIGHT_BLUE_CHARACTER = "\033[94m"
BRIGHT_MAGENTA_CHARACTER = "\033[95m"
BRIGHT_CYAN_CHARACTER = "\033[96m"
BRIGHT_WHITE_CHARACTER = "\033[97m"

BRIGHT_BLACK_BACKGROUND = "\033[100m"
BRIGHT_RED_BACKGROUND = "\033[101m"
BRIGHT_GREEN_BACKGROUND = "\033[102m"
BRIGHT_YELLOW_BACKGROUND = "\033[103m"
BRIGHT_BLUE_BACKGROUND = "\033[104m"
BRIGHT_MAGENTA_BACKGROUND = "\033[105m"
BRIGHT_CYAN_BACKGROUND = "\033[106m"
BRIGHT_WHITE_BACKGROUND = "\033[107m"

RESET = "\033[0m"

HIGHLIGHT = "\033[1m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"

FRAME = "\033[51m"
ENCIRCLE = "\033[52m"
OVERLINE = "\033[53m"

MOVE_UP = lambda n: "\033[%dA" % n
MOVE_DOWN = lambda n: "\033[%dB" % n
MOVE_LEFT = lambda n: "\033[%dC" % n
MOVE_RIGHT = lambda n: "\033[%dD" % n

SET_MOUSE_PLACE = lambda y, x: "\033[{};{}H".format(y, x)

CLEAR = "\033[2J"

CLEAR_LINE_AFTER = "\033[K"

MOUSE_DISAPPEAR = "\033?25l"
MOUSE_APPEAR = "\033?25h"

print(f"{CLEAR}{SET_MOUSE_PLACE(0,0)}Loading Server...")


def list_clients():
    with open("Datas/clients.json", "r") as clients_file:
        return "\n".join([f"[{uid}]{id}" for uid, id in json.load(clients_file)])

commands = [
    {
        "command": "ListClients",
        "params": [],
        "function": list_clients
    },
    # {
    #     "command": "GetClientStatus",
    #     "params": [
    #         {
    #             "choices": "ClientIDs",
    #             "param": "ClineID"
    #         }
    #     ]
    # }
]


print(CLEAR)


def process_command_line(inputs:list[bytes], place:int) -> str:
    if not (b"(" in inputs or b")" in inputs):
        for command in commands:
            if command["command"].startswith("".join([i.decode("utf-8") for i in inputs])):
                return f"{CLEAR}{SET_MOUSE_PLACE(0, 0)}{"".join([i.decode("utf-8") for i in inputs])}{
                WHITE_BACKGROUND + BLACK_CHARACTER}{command["command"][len(inputs):]}{BLACK_BACKGROUND + WHITE_CHARACTER}{SET_MOUSE_PLACE(0, place + 1)}"
        return f"{CLEAR}{SET_MOUSE_PLACE(0, 0)}{"".join([i.decode("utf-8") for i in inputs])}{WHITE_BACKGROUND + BLACK_CHARACTER}???{BLACK_BACKGROUND + WHITE_CHARACTER}{SET_MOUSE_PLACE(0 ,place + 1)}"
    return ""


def command() -> list[bytes]:
    inputs:list[bytes] = []
    place:int = 0
    while True:
        match msvcrt.getch():
            case b"\r":
                return inputs

            case b"\xe0":
                match msvcrt.getch():
                    case b"K":
                        if place == 0:
                            pass
                        else:
                            place -= 1

                    case b"M":
                        if place == len(inputs):
                            pass
                        else:
                            place += 1

                    case b"G":
                        place = 0

                    case b"O":
                        place = len(inputs)

                    case b"S":
                        if place == len(inputs):
                            pass
                        else:
                            del inputs[place]

            case b"\x08":
                if place == 0:
                    pass
                else:
                    del inputs[place - 1]
                    place -= 1

            case b"\x03":
                return [b"\x03"]

            case _char:
                inputs.insert(place, _char)
                place += 1

        sys.stdout.write(process_command_line(inputs, place))
        sys.stdout.flush()


if __name__ == "__main__":
    print(command())
