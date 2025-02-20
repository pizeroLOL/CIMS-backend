import msvcrt
import sys
import os
import json
import requests

# ANSI 颜色代码
ANSI_RESET = "\033[0m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_WHITE = "\033[37m"
ANSI_BRIGHT_WHITE = "\033[97m"
ANSI_WHITE_BG_BLACK_TEXT = "\033[47m\033[30m"

CLEAR_LINE = "\033[K"
CURSOR_TO_LINE_START = "\r"
SET_CURSOR_POS = lambda row, col: f"\033[{row};{col}H"
CLEAR_SCREEN = "\033[2J"

MANAGEMENT_SERVER_URL = "http://127.0.0.1:50052"
CLIENT_IDS = []

def fetch_client_ids():
    """从管理服务器获取客户端 ID 列表。"""
    global CLIENT_IDS
    try:
        response = requests.get(f"{MANAGEMENT_SERVER_URL}/clients")
        response.raise_for_status()
        CLIENT_IDS = list(response.json().keys())
    except requests.exceptions.RequestException:
        CLIENT_IDS = []

fetch_client_ids()

def api_call(command_name, *args, **kwargs):
    """通用 API 调用函数。"""
    try:
        if command_name == "list_clients":
            response = requests.get(f"{MANAGEMENT_SERVER_URL}/clients")
        elif command_name == "get_client_status":
            response = requests.get(f"{MANAGEMENT_SERVER_URL}/clients/{args[0]}/status")
        elif command_name == "get_all_client_statuses":
            response = requests.get(f"{MANAGEMENT_SERVER_URL}/clients/status")
        elif command_name == "restart_client":
            response = requests.post(f"{MANAGEMENT_SERVER_URL}/clients/{args[0]}/restart")
        elif command_name == "send_notification":
            params = {}
            if len(args) > 0:
                params["client_uid"] = args[0]
            params.update(kwargs)
            response = requests.post(f"{MANAGEMENT_SERVER_URL}/clients/{args[0]}/notify", params=params)
        elif command_name == "update_client_data":
            response = requests.post(f"{MANAGEMENT_SERVER_URL}/clients/{args[0]}/update")
        else:
            return f"{ANSI_RED}错误：未知的 API 命令 '{command_name}'。{ANSI_RESET}"

        response.raise_for_status()
        if response.headers.get('content-type') == 'application/json':
            return json.dumps(response.json(), indent=4, ensure_ascii=False)
        else:
            return response.text

    except requests.exceptions.RequestException as e:
        return f"{ANSI_RED}错误：API 调用失败：{e}{ANSI_RESET}"
    except (ValueError, TypeError) as e:
        return f"{ANSI_RED}错误：解析参数失败：{e}{ANSI_RESET}"
    except IndexError as e:
        return f"{ANSI_RED}错误: 缺少参数: {e}{ANSI_RESET}"

COMMAND_MAP = {
    "ListClients": (api_call, []),
    "GetClientStatus": (api_call, [{"param": "client_uid", "type": "ClientID"}]),
    "GetAllClientStatus": (api_call, []),
    "RestartClient": (api_call, [{"param": "client_uid", "type": "ClientID"}]),
    "SendNotification": (api_call, [
        {"param": "client_uid", "type": "ClientID"},
        {"param": "message_mask", "type": "String"},
        {"param": "message_content", "type": "String"},
        {"param": "overlay_icon_left", "type": "Integer", "optional": True, "default": 0},
        {"param": "overlay_icon_right", "type": "Integer", "optional": True, "default": 0},
        {"param": "is_emergency", "type": "Boolean", "optional": True, "default": False},
        {"param": "is_speech_enabled", "type": "Boolean", "optional": True, "default": True},
        {"param": "is_effect_enabled", "type": "Boolean", "optional": True, "default": True},
        {"param": "is_sound_enabled", "type": "Boolean", "optional": True, "default": True},
        {"param": "is_topmost", "type": "Boolean", "optional": True, "default": True},
        {"param": "duration_seconds", "type": "Float", "optional": True, "default": 5.0},
        {"param": "repeat_counts", "type": "Integer", "optional": True, "default": 1},
    ]),
    "UpdateClientData": (api_call, [{"param": "client_uid", "type": "ClientID"}]),
    "Help": (None, []),
    "Exit": (None, []),
}


def get_suggestions(input_str):
    """获取命令和 ClientID 建议。"""
    suggestions = []
    input_str = input_str.lower()

    if '(' in input_str:
        command_name = input_str[:input_str.find('(')].strip()
        if command_name in COMMAND_MAP:
            func, params_info = COMMAND_MAP[command_name]
            if params_info:
                param_str = input_str[input_str.find('(') + 1:]
                param_index = param_str.count(',')
                if param_index < len(params_info):
                    current_param_type = params_info[param_index].get("type")
                    if current_param_type == "ClientID":
                        typed_param = param_str.split(",")[-1].strip()
                        suggestions = [cid for cid in CLIENT_IDS if cid.lower().startswith(typed_param.lower())]

    else:
        suggestions = [cmd for cmd in COMMAND_MAP if cmd.lower().startswith(input_str)]

    return suggestions


def render_prompt(input_str, suggestion="", error_mode=False):
    """渲染提示符行。"""
    prompt_prefix = ">> "
    if error_mode:
        rendered = f"{ANSI_RED}{prompt_prefix}{input_str}{ANSI_RESET}"
    elif suggestion:
        rendered = f"{prompt_prefix}{ANSI_BRIGHT_WHITE}{input_str}{ANSI_RESET}{ANSI_WHITE_BG_BLACK_TEXT}{suggestion}{ANSI_RESET}"
    else:
        rendered = f"{prompt_prefix}{ANSI_BRIGHT_WHITE}{input_str}{ANSI_RESET}"

    sys.stdout.write(CURSOR_TO_LINE_START + CLEAR_LINE + rendered)
    sys.stdout.write(SET_CURSOR_POS(1, len(prompt_prefix) + len(input_str) + 1))
    sys.stdout.flush()


def process_input(input_str):
    """处理用户输入，执行命令或显示错误。"""
    input_str = input_str.strip()
    if not input_str:
        return ""

    if input_str.lower() == "exit":
        return "Exiting..."
    elif input_str.lower() == "help":
        help_text = f"{ANSI_WHITE}可用命令：{ANSI_RESET}\n"
        for cmd_name, (func, params_info) in COMMAND_MAP.items():
            params_desc = ", ".join([p['param'] for p in params_info])
            help_text += f"  {ANSI_GREEN}{cmd_name}({params_desc}){ANSI_RESET}\n"
        return help_text

    if '(' not in input_str or ')' not in input_str:
        return f"{ANSI_RED}错误：无效的命令语法。使用 func(param1, param2, ...){ANSI_RESET}"

    command_name = input_str[:input_str.find('(')].strip()
    if command_name not in COMMAND_MAP:
        return f"{ANSI_RED}错误：未知命令 '{command_name}'。输入 Help() 获取帮助。{ANSI_RESET}"

    func, params_info = COMMAND_MAP[command_name]
    param_str = input_str[input_str.find('(') + 1:input_str.rfind(')')]
    param_values = [p.strip() for p in param_str.split(',') if p.strip()] if param_str.strip() else []

    required_params_count = len([p for p in params_info if not p.get("optional")])
    if len(param_values) < required_params_count:
         return f"{ANSI_RED}错误: 命令 '{command_name}()' 至少需要 {required_params_count} 个参数。{ANSI_RESET}"

    kwargs = {}
    args = []
    try:
        for i, param_info in enumerate(params_info):
            param_name = param_info['param']
            param_type = param_info['type']

            if i < len(param_values):
                param_value = param_values[i]
                if param_type == "Integer":
                    param_value = int(param_value)
                elif param_type == "Float":
                    param_value = float(param_value)
                elif param_type == "Boolean":
                    param_value = param_value.lower() == 'true'

                if command_name == "SendNotification" and i < 1 : # Fix for SendNotification
                    args.append(param_value)
                else:
                    kwargs[param_name] = param_value
            elif 'default' in param_info:
                kwargs[param_name] = param_info['default']
            elif not param_info.get('optional'):
                 return f"{ANSI_RED}错误：缺少必需参数 '{param_name}'。{ANSI_RESET}"

        if command_name == "SendNotification":
            return func("send_notification",*args, **kwargs)
        elif command_name in ["GetClientStatus", "RestartClient", "UpdateClientData"]:
            return func(command_name.lower().replace("client","client_"),param_values[0])
        else:
            return func(command_name.lower().replace("clients","client_"),**kwargs)

    except (ValueError, TypeError) as e:
        return f"{ANSI_RED}错误：参数类型错误：{e}{ANSI_RESET}"


def main():
    """CLI 主循环。"""
    input_buffer = []
    error_state = False
    suggestion_text = ""

    print(CLEAR_SCREEN)
    render_prompt("")

    while True:
        char_bytes = msvcrt.getch()
        char_code = char_bytes[0]

        if char_bytes == b'\r':  # Enter
            command_line = "".join(input_buffer)
            print(f"\n>> {command_line}")
            result = process_input(command_line)
            print(result + "\n")

            input_buffer = []
            suggestion_text = ""
            error_state = False
            render_prompt("")

        elif char_bytes == b'\t':  # Tab 键
            current_input = "".join(input_buffer)
            suggestions = get_suggestions(current_input)

            if suggestions:
                if '(' in current_input:  # 参数补全
                    if suggestions:
                        prefix = current_input[current_input.rfind('(') + 1:].split(',')[-1].strip() # 更精确获取参数前缀
                        matched_suggestions = [s for s in suggestions if s.lower().startswith(prefix.lower())]
                        if matched_suggestions:
                            suggestion = matched_suggestions[0][len(prefix):]
                            input_buffer.extend(list(suggestion))
                else: # 命令补全
                    suggestion = suggestions[0][len(current_input):] + "()"
                    input_buffer.extend(list(suggestion))
                    suggestion_text = "" # 清除 suggestion_text

            render_prompt("".join(input_buffer), suggestion_text, error_state)


        elif char_code == 224:  # 特殊键
            special_key = msvcrt.getch()
            if special_key == b'K':  # 左箭头
                pass
            elif special_key == b'M':  # 右箭头
                pass
            elif special_key == b'S': # Delete
                if input_buffer:
                    input_buffer.pop()
                    render_prompt("".join(input_buffer), suggestion_text, error_state)


        elif char_code == 8:  # Backspace
            if input_buffer:
                input_buffer.pop()
            suggestion_text = ""
            current_input = "".join(input_buffer)
            if not get_suggestions(current_input) and current_input and '(' not in current_input:
                error_state = True
            else:
                error_state = False
            render_prompt("".join(input_buffer), suggestion_text, error_state)


        elif char_code == 3:  # Ctrl+C
            print(f"\n{process_input('Exit()')}") # 使用 process_input 处理 Exit 命令
            break


        else:  # 普通字符
            char = char_bytes.decode('utf-8')
            input_buffer.append(char)
            current_input = "".join(input_buffer)

            if '(' not in current_input and not get_suggestions(current_input):
                error_state = True
                suggestion_text = ""
            else:
                error_state = False
                suggestions = get_suggestions(current_input)
                if suggestions and '(' not in current_input:
                     suggestion_text = suggestions[0][len(current_input):]
                else:
                    suggestion_text = ""

            render_prompt("".join(input_buffer), suggestion_text, error_state)


if __name__ == "__main__":
    main()