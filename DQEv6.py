import json
import os
import msvcrt
import sys

# ANSI 转义码用于颜色和样式
COLOR_RESET = '\033[0m'  # 重置颜色和样式
COLOR_BOLD = '\033[1m'  # 加粗
COLOR_RED = '\033[31m'  # 红色
COLOR_GREEN = '\033[32m'  # 绿色
COLOR_YELLOW = '\033[33m'  # 黄色
COLOR_BLUE = '\033[34m'  # 蓝色
COLOR_MAGENTA = '\033[35m'  # 品红色
COLOR_CYAN = '\033[36m'  # 青色

BG_GRAY = '\033[47m'  # 灰色背景
BG_BLUE = '\033[44m'  # 蓝色背景
BG_GREEN = '\033[42m'  # 绿色背景
BG_YELLOW = '\033[43m'  # 黄色背景
BG_RED = '\033[41m'  # 红色背景
BG_MAGENTA = '\033[45m'  # 品红色背景
BG_CYAN = '\033[46m'  # 青色背景

DATA_DIR = "Datas"  # 数据文件夹路径

# ANSI 转义码用于方向键
ARROW_UP = '\033[A'  # 上方向键
ARROW_DOWN = '\033[B'  # 下方向键
ARROW_LEFT = '\033[D'  # 左方向键
ARROW_RIGHT = '\033[C'  # 右方向键

def load_json(filepath):
    """加载 JSON 文件数据

    Args:
        filepath (str): JSON 文件路径

    Returns:
        dict: JSON 数据字典，如果文件未找到或解码失败则返回 None
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:  # 以 UTF-8 编码读取文件
            return json.load(f)  # 解析 JSON 数据
    except FileNotFoundError:
        print(f"{COLOR_RED}错误: 文件未找到: {filepath}{COLOR_RESET}")  # 打印红色错误信息，提示文件未找到
        return None  # 返回 None 表示加载失败
    except json.JSONDecodeError:
        print(f"{COLOR_RED}错误: JSON解码错误: {filepath}{COLOR_RESET}")  # 打印红色错误信息，提示 JSON 解码错误
        return None  # 返回 None 表示加载失败

def save_json(filepath, data):
    """保存数据到 JSON 文件

    Args:
        filepath (str): JSON 文件路径
        data (dict): 要保存的 JSON 数据字典
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:  # 以 UTF-8 编码写入文件
            json.dump(data, f, indent=4, ensure_ascii=False)  # 将数据以 JSON 格式写入，缩进为 4，不转义 ASCII 字符
        print(f"{COLOR_GREEN}文件已保存: {filepath}{COLOR_RESET}")  # 打印绿色提示信息，表示文件保存成功
    except Exception as e:
        print(f"{COLOR_RED}错误: 保存文件失败: {filepath} - {e}{COLOR_RESET}")  # 打印红色错误信息，提示文件保存失败及异常信息

def shorten_id(id_str):
    """缩短 ID 字符串，保留前四位和后三位，中间用 '...' 代替

    Args:
        id_str (str): 要缩短的 ID 字符串

    Returns:
        str: 缩短后的 ID 字符串，如果 ID 为空则返回 "N/A"
    """
    if not id_str:
        return "N/A"  # 如果 ID 字符串为空，返回 "N/A"
    if len(id_str) <= 7:
        return id_str  # 如果 ID 字符串长度小于等于 7，则不缩短，直接返回
    return f"{id_str[:4]}...{id_str[-3:]}"  # 返回缩短后的 ID 字符串，格式为 前四位...后三位

def discover_files(client_id):
    """根据 ClientID 发现所有相关的 JSON 文件路径

    Args:
        client_id (str): 客户端 ID

    Returns:
        dict: 文件路径字典，键为文件类型，值为文件路径
    """
    base_filename = f"{client_id}.json"  # 构造基础文件名，使用 client_id
    manifest_path = os.path.join(DATA_DIR, "Manifests", base_filename)  # 清单文件路径
    class_plans_path = os.path.join(DATA_DIR, "ClassPlans", base_filename)  # 课表计划文件路径
    default_settings_path = os.path.join(DATA_DIR, "DefaultSettings", base_filename)  # 默认设置文件路径
    policies_path = os.path.join(DATA_DIR, "Policies", base_filename)  # 策略文件路径
    subjects_source_path = os.path.join(DATA_DIR, "SubjectsSource", base_filename)  # 科目源文件路径
    time_layouts_source_path = os.path.join(DATA_DIR, "TimeLayouts", base_filename)  # 时间布局源文件路径

    return {  # 返回文件路径字典
        "manifest": manifest_path,
        "class_plans": class_plans_path,
        "default_settings": default_settings_path,
        "policies": policies_path,
        "subjects_source": subjects_source_path,
        "time_layouts_source": time_layouts_source_path,
    }

def display_main_menu():
    """显示主菜单"""
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏，Windows 使用 'cls'，其他系统使用 'clear'
    print(f"\n{COLOR_BOLD}{BG_CYAN} 主菜单 {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的主菜单标题
    print(f"{COLOR_BOLD}请选择要编辑的文件 (使用数字键):{COLOR_RESET}")  # 提示用户选择文件类型
    print("1. 课表计划 (ClassPlans)")  # 选项 1：编辑课表计划
    print("2. 默认设置 (DefaultSettings)")  # 选项 2：编辑默认设置
    print("3. 清单 (Manifests)")  # 选项 3：查看清单
    print("4. 策略 (Policies)")  # 选项 4：查看策略
    print("5. 科目 (SubjectsSource)")  # 选项 5：编辑科目
    print("0. 退出")  # 选项 0：退出程序

def get_subject_name(subjects_data, subject_id):
    """根据科目 ID 获取科目名称

    Args:
        subjects_data (dict): 科目数据字典
        subject_id (str): 科目 ID

    Returns:
        str: 科目名称，如果找不到则返回 "未知科目"
    """
    if subjects_data and 'Subjects' in subjects_data and subject_id in subjects_data['Subjects']:  # 检查数据是否存在且包含科目信息
        return subjects_data['Subjects'][subject_id].get('Name', '未知科目')  # 返回科目名称，如果 Name 字段不存在则返回 "未知科目"
    return "未知科目"  # 如果找不到科目信息，返回 "未知科目"

def get_time_layout_name(time_layouts_data, time_layout_id):
    """根据时间布局 ID 获取时间布局名称

    Args:
        time_layouts_data (dict): 时间布局数据字典
        time_layout_id (str): 时间布局 ID

    Returns:
        str: 时间布局名称，如果找不到则返回 "未知时间布局"
    """
    if time_layouts_data and 'TimeLayouts' in time_layouts_data and time_layout_id in time_layouts_data['TimeLayouts']:  # 检查数据是否存在且包含时间布局信息
        return time_layouts_data['TimeLayouts'][time_layout_id].get('Name', '未知时间布局')  # 返回时间布局名称，如果 Name 字段不存在则返回 "未知时间布局"
    return "未知时间布局"  # 如果找不到时间布局信息，返回 "未知时间布局"

def display_class_plans(data, subjects_data, time_layouts_data, filename, plan_index):
    """显示单个课表计划的详细信息

    Args:
        data (dict): 课表计划数据字典
        subjects_data (dict): 科目数据字典
        time_layouts_data (dict): 时间布局数据字典
        filename (str): 文件名
        plan_index (int): 要显示的课表计划索引
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"{COLOR_BOLD}{BG_YELLOW} 课表计划 - {filename} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的课表计划标题
    if not data or 'ClassPlans' not in data:  # 检查课表数据是否存在
        print(f"{COLOR_RED}没有课表数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息，提示没有课表数据
        return  # 退出函数

    plan_ids = list(data['ClassPlans'].keys())  # 获取课表计划 ID 列表
    if not plan_ids:  # 检查是否有课表计划
        print(f"{COLOR_CYAN}没有课表计划。{COLOR_RESET}")  # 打印青色提示信息，提示没有课表计划
        return  # 退出函数

    if plan_index < 0 or plan_index >= len(plan_ids):  # 检查 plan_index 是否越界
        plan_index = 0  # 如果越界，重置为 0，显示第一个课表计划

    plan_id = plan_ids[plan_index]  # 获取当前要显示的课表计划 ID
    display_plan = data['ClassPlans'][plan_id]  # 获取课表计划数据

    weekday_str = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][display_plan.get('TimeRule', {}).get('WeekDay', 0)] if 'WeekDay' in display_plan.get('TimeRule', {}) else "N/A"  # 获取星期字符串
    time_layout_name = get_time_layout_name(time_layouts_data, display_plan.get('TimeLayoutId', ''))  # 获取时间布局名称

    print(f"ID: {shorten_id(plan_id)}")  # 打印缩短的课表计划 ID
    print(f"名称: {display_plan.get('Name', '')}")  # 打印课表计划名称
    print(f"时间布局: {time_layout_name} ({shorten_id(display_plan.get('TimeLayoutId', ''))})")  # 打印时间布局名称和缩短的 ID
    print(f"星期: {weekday_str}")  # 打印星期
    print(f"启用: {'是' if display_plan.get('IsEnabled', False) else '否'}")  # 打印是否启用

    print(f"\n课程:")  # 打印课程标题
    if 'Classes' in display_plan and display_plan['Classes']:  # 检查是否有课程列表
        for class_item in display_plan['Classes']:  # 遍历课程列表
            subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', ''))  # 获取科目名称
            subject_display = f"- 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"  # 构造科目显示字符串
            print(f"  {subject_display}, 更改课: {'是' if class_item.get('IsChangedClass', False) else '否'}, 启用: {'是' if class_item.get('IsActive', False) else '否'}")  # 打印课程详细信息
    else:
        print(f"  {COLOR_CYAN}没有课程。{COLOR_RESET}")  # 打印青色提示信息，提示没有课程

    print("-" * 30)  # 打印分隔线
    print(f"课表计划: {plan_index + 1}/{len(plan_ids)}")  # 打印当前课表计划索引和总数
    print("{COLOR_BOLD}操作:{COLOR_RESET} (方向键 ↑↓ 切换课表, 'e' 编辑, 'b' 返回主菜单, '0' 退出)")  # 打印操作提示

def display_default_settings(data, filename):
    """显示默认设置信息

    Args:
        data (dict): 默认设置数据字典
        filename (str): 文件名
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 默认设置 - {filename} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的默认设置标题
    if not data:  # 检查默认设置数据是否存在
        print(f"{COLOR_RED}没有默认设置数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息，提示没有默认设置数据
        return  # 退出函数

    print(f"  名称: {data.get('Name', '')}")  # 打印默认设置名称
    print(f"  是否启用 Overlay ClassPlan: {'是' if data.get('IsOverlayClassPlanEnabled', False) else '否'}")  # 打印是否启用 Overlay ClassPlan
    print(f"  Overlay ClassPlan ID: {shorten_id(data.get('OverlayClassPlanId', 'N/A'))}")  # 打印 Overlay ClassPlan ID，并缩短显示
    print(f"  Temp ClassPlan ID: {shorten_id(data.get('TempClassPlanId', 'N/A'))}")  # 打印 Temp ClassPlan ID，并缩短显示
    print(f"  Selected ClassPlan Group ID: {shorten_id(data.get('SelectedClassPlanGroupId', 'N/A'))}")  # 打印 Selected ClassPlan Group ID，并缩短显示
    print(f"  Is Active: {'是' if data.get('IsActive', False) else '否'}")  # 打印是否启用
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")  # 打印操作提示

def display_manifests(data, filename):
    """显示清单信息

    Args:
        data (dict): 清单数据字典
        filename (str): 文件名
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 清单 - {filename} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的清单标题
    if not data:  # 检查清单数据是否存在
        print(f"{COLOR_RED}没有清单数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息，提示没有清单数据
        return  # 退出函数

    print(f"  服务器类型 (ServerKind): {data.get('ServerKind', 'N/A')}")  # 打印服务器类型
    print(f"  组织名称 (OrganizationName): {data.get('OrganizationName', 'N/A')}")  # 打印组织名称

    print(f"\n  {COLOR_BOLD}数据源:{COLOR_RESET}")  # 打印数据源标题
    for key, source in data.items():  # 遍历数据源
        if key.endswith("Source"):  # 筛选以 "Source" 结尾的键
            print(f"    {key}:")  # 打印数据源类型
            print(f"      值 (Value): {source.get('Value', 'N/A')}")  # 打印数据源值
            print(f"      版本 (Version): {source.get('Version', 'N/A')}")  # 打印数据源版本
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")  # 打印操作提示

def display_policies(data, filename):
    """显示策略信息

    Args:
        data (dict): 策略数据字典
        filename (str): 文件名
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 策略 - {filename} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的策略标题
    if not data:  # 检查策略数据是否存在
        print(f"{COLOR_RED}没有策略数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息，提示没有策略数据
        return  # 退出函数

    for key, value in data.items():  # 遍历策略项
        print(f"  {key}: {'是' if value else '否'}")  # 打印策略项和对应的值（是否启用）
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")  # 打印操作提示

def display_subjects_source(data, filename, subject_index):
    """显示单个科目的详细信息

    Args:
        data (dict): 科目数据字典
        filename (str): 文件名
        subject_index (int): 要显示的科目索引
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 科目 - {filename} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的科目标题
    if not data or 'Subjects' not in data:  # 检查科目数据是否存在
        print(f"{COLOR_RED}没有科目数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息，提示没有科目数据
        return  # 退出函数

    subject_ids = list(data['Subjects'].keys())  # 获取科目 ID 列表
    if not subject_ids:  # 检查是否有科目
        print(f"{COLOR_CYAN}没有科目。{COLOR_RESET}")  # 打印青色提示信息，提示没有科目
        return  # 退出函数

    if subject_index < 0 or subject_index >= len(subject_ids):  # 检查 subject_index 是否越界
        subject_index = 0  # 如果越界，重置为 0，显示第一个科目

    subject_id = subject_ids[subject_index]  # 获取当前要显示的科目 ID
    subject_data = data['Subjects'][subject_id]  # 获取科目数据

    print(f"科目 ID: {shorten_id(subject_id)}")  # 打印缩短的科目 ID
    print(f"名称: {subject_data.get('Name', '')}")  # 打印科目名称
    print(f"首字母: {subject_data.get('Initial', '')}")  # 打印科目首字母
    print(f"教师名称: {subject_data.get('TeacherName', '')}")  # 打印教师名称
    print(f"户外课: {'是' if subject_data.get('IsOutDoor', False) else '否'}")  # 打印是否户外课
    print(f"启用: {'是' if subject_data.get('IsActive', False) else '否'}")  # 打印是否启用

    print("-" * 30)  # 打印分隔线
    print(f"科目: {subject_index + 1}/{len(subject_ids)}")  # 打印当前科目索引和总数
    print("{COLOR_BOLD}操作:{COLOR_RESET} (方向键 ↑↓ 切换科目, 'e' 编辑, 'b' 返回主菜单, '0' 退出)")  # 打印操作提示

def edit_class_plans_menu(files, client_data, subjects_data, time_layouts_data):
    """课表计划编辑菜单"""
    plan_index = 0  # 初始课表计划索引
    plan_ids = list(client_data['class_plans']['ClassPlans'].keys())  # 获取课表计划 ID 列表
    if not plan_ids:  # 如果没有课表计划
        print(f"{COLOR_CYAN}没有课表计划可以编辑。{COLOR_RESET}")  # 打印青色提示信息
        msvcrt.getwch()  # 等待按键
        return  # 退出函数

    while True:
        if plan_index >= len(plan_ids):  # 索引越界检查，防止删除后索引失效
            plan_index = 0  # 重置为第一个
        if plan_index < 0:  # 索引越界检查，防止删除后索引失效
            plan_index = len(plan_ids) - 1 if plan_ids else 0  # 重置为最后一个或 0

        display_class_plans(client_data['class_plans'], subjects_data, time_layouts_data, os.path.basename(files['class_plans']), plan_index)  # 显示当前课表计划
        key_stroke = msvcrt.getwch()  # 获取用户按键

        if key_stroke == 'e':  # 如果按下 'e' 键
            selected_plan_id = plan_ids[plan_index]  # 获取当前选中的课表计划 ID
            edit_class_plan_details(files, client_data, subjects_data, time_layouts_data, selected_plan_id)  # 进入课表计划详情编辑菜单
            plan_ids = list(client_data['class_plans']['ClassPlans'].keys())  # 编辑后更新课表计划 ID 列表，以防课表计划被删除
        elif key_stroke == 'b':  # 如果按下 'b' 键
            return  # 返回上一级菜单（主菜单）
        elif key_stroke == '0':  # 如果按下 '0' 键
            exit_program()  # 退出程序
        elif key_stroke == ARROW_UP:  # 如果按下上方向键
            plan_index = max(0, plan_index - 1)  # 索引减一，切换到上一个课表计划
        elif key_stroke == ARROW_DOWN:  # 如果按下下方向键
            plan_index = min(len(plan_ids) - 1, plan_index + 1)  # 索引加一，切换到下一个课表计划
        elif key_stroke == '\xe0':  # 扩展键（方向键、F 功能键等）引导符
            extended_key = msvcrt.getwch()  # 读取扩展键的实际键值
            if extended_key == 'H':  # 上箭头
                plan_index = max(0, plan_index - 1)  # 切换到上一个课表计划
            elif extended_key == 'P':  # 下箭头
                plan_index = min(len(plan_ids) - 1, plan_index + 1)  # 切换到下一个课表计划
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示无效选项

def edit_specific_class_plan(files, client_data, subjects_data, time_layouts_data, selected_plan_index):
    """编辑特定课表计划 (不再需要，直接在 edit_class_plans_menu 中编辑当前选中的)"""
    pass  # 此函数已不再需要，编辑操作直接在 edit_class_plans_menu 中进行

def edit_class_plan_details(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑课表计划详情菜单"""
    while True:
        plan_data = client_data['class_plans']['ClassPlans'][plan_id]  # 获取当前课表计划数据
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课表计划: {plan_data.get('Name', '')} - {shorten_id(plan_id)} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的编辑课表计划标题
        print("1. 编辑名称")  # 选项 1：编辑课表计划名称
        print("2. 编辑时间规则")  # 选项 2：编辑时间规则
        print("3. 编辑课程")  # 选项 3：编辑课程列表
        print("b. 返回课表计划菜单")  # 选项 b：返回课表计划菜单
        print("0. 退出")  # 选项 0：退出程序

        choice = msvcrt.getwch()  # 获取用户按键

        if choice == '1':  # 如果按下 '1' 键
            new_name = input("  输入新的课表计划名称: ")  # 获取新的课表计划名称输入
            client_data['class_plans']['ClassPlans'][plan_id]['Name'] = new_name  # 更新课表计划名称
            save_json(files['class_plans'], client_data['class_plans'])  # 保存修改到 JSON 文件
        elif choice == '2':  # 如果按下 '2' 键
            edit_time_rule(plan_data)  # 进入时间规则编辑菜单
            save_json(files['class_plans'], client_data['class_plans'])  # 保存修改到 JSON 文件
        elif choice == '3':  # 如果按下 '3' 键
            edit_classes_in_plan(files, client_data, subjects_data, time_layouts_data, plan_id)  # 进入课程列表编辑菜单
        elif choice == 'b':  # 如果按下 'b' 键
            return  # 返回上一级菜单（课表计划菜单）
        elif choice == '0':  # 如果按下 '0' 键
            exit_program()  # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示无效选项

def edit_time_rule(plan_data):
    """编辑课表计划的时间规则"""
    time_rule = plan_data.setdefault('TimeRule', {})  # 获取或创建 TimeRule 字典，如果不存在则创建

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑时间规则 {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的编辑时间规则标题
        weekday_str = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][time_rule.get('WeekDay', 0)] if 'WeekDay' in time_rule else "N/A"  # 获取当前星期字符串
        print(f"  当前星期: {weekday_str} (编号: {time_rule.get('WeekDay', 0)})")  # 打印当前星期和编号
        print(f"  当前 WeekCountDiv: {time_rule.get('WeekCountDiv', 0)}")  # 打印当前 WeekCountDiv
        print(f"  当前 WeekCountDivTotal: {time_rule.get('WeekCountDivTotal', 2)}")  # 打印当前 WeekCountDivTotal
        print(f"  是否启用: {'是' if time_rule.get('IsActive', False) else '否'}")  # 打印当前是否启用状态

        print("1. 编辑星期 (0-6, 0=星期日)")  # 选项 1：编辑星期
        print("2. 编辑 WeekCountDiv")  # 选项 2：编辑 WeekCountDiv
        print("3. 编辑 WeekCountDivTotal")  # 选项 3：编辑 WeekCountDivTotal
        print("4. 编辑是否启用")  # 选项 4：编辑是否启用
        print("b. 返回课表计划详情菜单")  # 选项 b：返回课表计划详情菜单
        print("0. 退出")  # 选项 0：退出程序

        choice = msvcrt.getwch()  # 获取用户按键

        if choice == '1':  # 如果按下 '1' 键
            try:
                weekday = int(input("  输入新的星期编号 (0-6): "))  # 获取新的星期编号输入
                if 0 <= weekday <= 6:  # 验证星期编号是否在有效范围内
                    time_rule['WeekDay'] = weekday  # 更新星期编号
                else:
                    print(f"{COLOR_RED}星期编号超出范围 (0-6)。{COLOR_RESET}")  # 打印红色错误信息，提示编号超出范围
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}")  # 打印红色错误信息，提示输入无效
        elif choice == '2':  # 如果按下 '2' 键
            try:
                week_div = int(input("  输入新的 WeekCountDiv: "))  # 获取新的 WeekCountDiv 输入
                time_rule['WeekCountDiv'] = week_div  # 更新 WeekCountDiv
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}")  # 打印红色错误信息，提示输入无效
        elif choice == '3':  # 如果按下 '3' 键
            try:
                week_div_total = int(input("  输入新的 WeekCountDivTotal: "))  # 获取新的 WeekCountDivTotal 输入
                time_rule['WeekCountDivTotal'] = week_div_total  # 更新 WeekCountDivTotal
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}")  # 打印红色错误信息，提示输入无效
        elif choice == '4':  # 如果按下 '4' 键
            is_active_input = input("  是否启用 (yes/no): ").lower()  # 获取是否启用的输入 (yes/no)
            time_rule['IsActive'] = is_active_input == 'yes'  # 更新是否启用状态
        elif choice == 'b':  # 如果按下 'b' 键
            return  # 返回上一级菜单（课表计划详情菜单）
        elif choice == '0':  # 如果按下 '0' 键
            exit_program()  # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示无效选项

def edit_classes_in_plan(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑课表计划中的课程菜单"""
    while True:
        plan_data = client_data['class_plans']['ClassPlans'][plan_id]  # 获取当前课表计划数据
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课表计划课程: {plan_data.get('Name', '')} - {shorten_id(plan_id)} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的编辑课表计划课程标题

        if 'Classes' in plan_data and plan_data['Classes']:  # 检查是否有课程列表
            for i, class_item in enumerate(plan_data['Classes']):  # 遍历课程列表并显示课程信息
                subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', ''))  # 获取科目名称
                subject_display = f"- {i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"  # 构造科目显示字符串
                print(f"    {subject_display}, 更改课: {'是' if class_item.get('IsChangedClass', False) else '否'}, 启用: {'是' if class_item.get('IsActive', False) else '否'}")  # 打印课程详细信息
        else:
            print(f"    {COLOR_CYAN}没有课程。{COLOR_RESET}")  # 打印青色提示信息，提示没有课程

        print("\n课程编辑选项:")  # 打印课程编辑选项标题
        print("a. 添加课程")  # 选项 a：添加课程
        print("e. 编辑课程")  # 选项 e：编辑课程
        print("d. 删除课程")  # 选项 d：删除课程
        print("b. 返回课表计划详情菜单")  # 选项 b：返回课表计划详情菜单
        print("0. 退出")  # 选项 0：退出程序

        choice = msvcrt.getwch()  # 获取用户按键

        if choice == 'a':  # 如果按下 'a' 键
            add_class_to_plan(files, client_data, plan_id)  # 进入添加课程流程
        elif choice == 'e':  # 如果按下 'e' 键
            edit_specific_class(files, client_data, subjects_data, time_layouts_data, plan_id)  # 进入编辑特定课程流程
        elif choice == 'd':  # 如果按下 'd' 键
            delete_class_from_plan(files, client_data, plan_id)  # 进入删除课程流程
        elif choice == 'b':  # 如果按下 'b' 键
            return  # 返回上一级菜单（课表计划详情菜单）
        elif choice == '0':  # 如果按下 '0' 键
            exit_program()  # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示无效选项

def add_class_to_plan(files, client_data, plan_id):
    """添加课程到课表计划"""
    subject_id = input("  输入要添加的科目 ID: ")  # 获取要添加的科目 ID 输入
    new_class = {  # 创建新的课程字典
        "SubjectId": subject_id,  # 科目 ID
        "IsChangedClass": False,  # 默认为非更改课
        "AttachedObjects": {},  # 初始为空的附加对象字典
        "IsActive": False  # 默认为未启用
    }
    client_data['class_plans']['ClassPlans'][plan_id]['Classes'].append(new_class)  # 将新课程添加到课表计划的课程列表中
    save_json(files['class_plans'], client_data['class_plans'])  # 保存修改到 JSON 文件
    print(f"{COLOR_GREEN}课程已添加。{COLOR_RESET}")  # 打印绿色提示信息，表示课程添加成功

def edit_specific_class(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑特定课程菜单"""
    plan_data = client_data['class_plans']['ClassPlans'][plan_id]  # 获取当前课表计划数据
    if not plan_data.get('Classes'):  # 检查课表计划是否有课程
        print(f"{COLOR_RED}该课表计划没有课程可以编辑。{COLOR_RESET}")  # 打印红色错误信息，提示没有课程可编辑
        return  # 退出函数

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 选择要编辑的课程编号 {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的选择编辑课程编号标题
        for i, class_item in enumerate(plan_data['Classes']):  # 遍历课程列表并显示课程选项
            subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', ''))  # 获取科目名称
            subject_display = f"{i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"  # 构造科目显示字符串
            print(f"    {subject_display}")  # 打印课程选项

        try:
            class_index = int(input("  输入课程编号选择编辑: ")) - 1  # 获取用户输入的课程编号并转换为索引（从 0 开始）
            if 0 <= class_index < len(plan_data['Classes']):  # 验证课程编号是否在有效范围内
                selected_class = plan_data['Classes'][class_index]  # 获取选中的课程数据
                break  # 跳出循环，进入课程详情编辑
            else:
                print(f"{COLOR_RED}课程编号超出范围，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示编号超出范围
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号。{COLOR_RESET}")  # 打印红色错误信息，提示输入无效

    if selected_class:  # 如果成功选中课程
        edit_class_details(files, client_data, subjects_data, plan_id, selected_class, class_index)  # 进入课程详情编辑菜单

def edit_class_details(files, client_data, subjects_data, plan_id, selected_class, class_index):
    """编辑课程详情菜单"""
    while True:
        subject_name = get_subject_name(subjects_data, selected_class.get('SubjectId', ''))  # 获取科目名称
        subject_display = f"{subject_name} ({shorten_id(selected_class.get('SubjectId', 'N/A'))})"  # 构造科目显示字符串
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课程详情: {subject_display} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的编辑课程详情标题
        print("1. 编辑科目 ID")  # 选项 1：编辑科目 ID
        print("2. 编辑是否更改课")  # 选项 2：编辑是否更改课
        print("3. 编辑是否启用")  # 选项 3：编辑是否启用
        print("b. 返回课程列表菜单")  # 选项 b：返回课程列表菜单
        print("0. 退出")  # 选项 0：退出程序

        choice = msvcrt.getwch()  # 获取用户按键

        if choice == '1':  # 如果按下 '1' 键
            new_subject_id = input("  输入新的科目 ID: ")  # 获取新的科目 ID 输入
            selected_class['SubjectId'] = new_subject_id  # 更新课程的科目 ID
            save_json(files['class_plans'], client_data['class_plans'])  # 保存修改到 JSON 文件
        elif choice == '2':  # 如果按下 '2' 键
            is_changed_input = input("  是否更改课 (yes/no): ").lower()  # 获取是否更改课的输入 (yes/no)
            selected_class['IsChangedClass'] = is_changed_input == 'yes'  # 更新课程是否为更改课
            save_json(files['class_plans'], client_data['class_plans'])  # 保存修改到 JSON 文件
        elif choice == '3':  # 如果按下 '3' 键
            is_active_input = input("  是否启用 (yes/no): ").lower()  # 获取是否启用的输入 (yes/no)
            selected_class['IsActive'] = is_active_input == 'yes'  # 更新课程是否启用
            save_json(files['class_plans'], client_data['class_plans'])  # 保存修改到 JSON 文件
        elif choice == 'b':  # 如果按下 'b' 键
            return  # 返回上一级菜单（课程列表菜单）
        elif choice == '0':  # 如果按下 '0' 键
            exit_program()  # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示无效选项

def delete_class_from_plan(files, client_data, plan_id):
    """从课表计划中删除课程"""
    plan_data = client_data['class_plans']['ClassPlans'][plan_id]  # 获取当前课表计划数据
    if not plan_data.get('Classes'):  # 检查课表计划是否有课程
        print(f"{COLOR_RED}该课表计划没有课程可以删除。{COLOR_RESET}")  # 打印红色错误信息，提示没有课程可删除
        return  # 退出函数

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 选择要删除的课程编号 {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的选择删除课程编号标题
        for i, class_item in enumerate(plan_data['Classes']):  # 遍历课程列表并显示课程选项
            subject_name = get_subject_name(client_data['subjects_source'], class_item.get('SubjectId', ''))  # 获取科目名称
            subject_display = f"{i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"  # 构造科目显示字符串
            print(f"    {subject_display}")  # 打印课程选项

        print("b. 返回课程列表菜单")  # 选项 b：返回课程列表菜单
        print("0. 退出")  # 选项 0：退出程序

        try:
            class_index_input = input("  输入课程编号删除 (或 'b' 返回): ")  # 获取要删除的课程编号输入
            if class_index_input.lower() == 'b':  # 如果输入 'b'
                return  # 返回上一级菜单（课程列表菜单）
            class_index = int(class_index_input) - 1  # 将输入转换为课程索引（从 0 开始）

            if 0 <= class_index < len(plan_data['Classes']):  # 验证课程编号是否在有效范围内
                del plan_data['Classes'][class_index]  # 从课程列表中删除课程
                save_json(files['class_plans'], client_data['class_plans'])  # 保存修改到 JSON 文件
                print(f"{COLOR_GREEN}课程已删除。{COLOR_RESET}")  # 打印绿色提示信息，表示课程删除成功
                return  # 返回课程列表菜单
            else:
                print(f"{COLOR_RED}课程编号超出范围，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示编号超出范围
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号或 'b' 返回。{COLOR_RESET}")  # 打印红色错误信息，提示输入无效
        except Exception as e:
            print(f"{COLOR_RED}删除课程出错: {e}{COLOR_RESET}")  # 打印红色错误信息，提示删除课程出错及异常信息
            return  # 退出函数

def edit_subjects_source_menu(files, client_data):
    """科目编辑菜单"""
    subject_index = 0  # 初始科目索引
    subject_ids = list(client_data['subjects_source']['Subjects'].keys())  # 获取科目 ID 列表
    if not subject_ids:  # 如果没有科目
        print(f"{COLOR_CYAN}没有科目可以编辑。{COLOR_RESET}")  # 打印青色提示信息，提示没有科目可编辑
        msvcrt.getwch()  # 等待按键
        return  # 退出函数

    while True:
        if subject_index >= len(subject_ids):  # 索引越界检查，防止删除后索引失效
            subject_index = 0  # 重置为第一个
        if subject_index < 0:  # 索引越界检查，防止删除后索引失效
            subject_index = len(subject_ids) - 1 if subject_ids else 0  # 重置为最后一个或 0

        display_subjects_source(client_data['subjects_source'], os.path.basename(files['subjects_source']), subject_index)  # 显示当前科目信息
        key_stroke = msvcrt.getwch()  # 获取用户按键

        if key_stroke == 'e':  # 如果按下 'e' 键
            selected_subject_id = subject_ids[subject_index]  # 获取当前选中的科目 ID
            edit_subject_details(files, client_data, selected_subject_id)  # 进入科目详情编辑菜单
            subject_ids = list(client_data['subjects_source']['Subjects'].keys())  # 编辑后更新科目 ID 列表，以防科目被删除
        elif key_stroke == 'b':  # 如果按下 'b' 键
            return  # 返回上一级菜单（主菜单）
        elif key_stroke == '0':  # 如果按下 '0' 键
            exit_program()  # 退出程序
        elif key_stroke == ARROW_UP:  # 如果按下上方向键
            subject_index = max(0, subject_index - 1)  # 索引减一，切换到上一个科目
        elif key_stroke == ARROW_DOWN:  # 如果按下下方向键
            subject_index = min(len(subject_ids) - 1, subject_index + 1)  # 索引加一，切换到下一个科目
        elif key_stroke == '\xe0':  # 扩展键（方向键、F 功能键等）引导符
            extended_key = msvcrt.getwch()  # 读取扩展键的实际键值
            if extended_key == 'H':  # 上箭头
                subject_index = max(0, subject_index - 1)  # 切换到上一个科目
            elif extended_key == 'P':  # 下箭头
                subject_index = min(len(subject_ids) - 1, subject_index + 1)  # 切换到下一个科目
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示无效选项

def edit_specific_subject(files, client_data, page_index):
    """编辑特定科目 (不再需要，直接在 edit_subjects_source_menu 中编辑当前选中的)"""
    pass  # 此函数已不再需要，编辑操作直接在 edit_subjects_source_menu 中进行

def edit_subject_details(files, client_data, subject_id):
    """编辑科目详情菜单"""
    while True:
        subject_data = client_data['subjects_source']['Subjects'][subject_id]  # 获取当前科目数据
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑科目: {subject_data.get('Name', '')} - {shorten_id(subject_id)} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的编辑科目标题
        print("1. 编辑名称")  # 选项 1：编辑科目名称
        print("2. 编辑首字母")  # 选项 2：编辑科目首字母
        print("3. 编辑教师名称")  # 选项 3：编辑教师名称
        print("4. 编辑是否户外课")  # 选项 4：编辑是否户外课属性
        print("5. 编辑是否启用")  # 选项 5：编辑是否启用属性
        print("b. 返回科目菜单")  # 选项 b：返回科目菜单
        print("0. 退出")  # 选项 0：退出程序

        choice = msvcrt.getwch()  # 获取用户按键

        if choice == '1':  # 如果按下 '1' 键
            new_name = input("  输入新的科目名称: ")  # 获取新的科目名称输入
            client_data['subjects_source']['Subjects'][subject_id]['Name'] = new_name  # 更新科目名称
            save_json(files['subjects_source'], client_data['subjects_source'])  # 保存修改到 JSON 文件
        elif choice == '2':  # 如果按下 '2' 键
            new_initial = input("  输入新的科目首字母: ")  # 获取新的科目首字母输入
            client_data['subjects_source']['Subjects'][subject_id]['Initial'] = new_initial  # 更新科目首字母
            save_json(files['subjects_source'], client_data['subjects_source'])  # 保存修改到 JSON 文件
        elif choice == '3':  # 如果按下 '3' 键
            new_teacher_name = input("  输入新的教师名称: ")  # 获取新的教师名称输入
            client_data['subjects_source']['Subjects'][subject_id]['TeacherName'] = new_teacher_name  # 更新教师名称
            save_json(files['subjects_source'], client_data['subjects_source'])  # 保存修改到 JSON 文件
        elif choice == '4':  # 如果按下 '4' 键
            is_outdoor_input = input("  是否户外课 (yes/no): ").lower()  # 获取是否户外课的输入 (yes/no)
            client_data['subjects_source']['Subjects'][subject_id]['IsOutDoor'] = is_outdoor_input == 'yes'  # 更新是否户外课属性
            save_json(files['subjects_source'], client_data['subjects_source'])  # 保存修改到 JSON 文件
        elif choice == '5':  # 如果按下 '5' 键
            is_active_input = input("  是否启用 (yes/no): ").lower()  # 获取是否启用的输入 (yes/no)
            client_data['subjects_source']['Subjects'][subject_id]['IsActive'] = is_active_input == 'yes'  # 更新是否启用属性
            save_json(files['subjects_source'], client_data['subjects_source'])  # 保存修改到 JSON 文件
        elif choice == 'b':  # 如果按下 'b' 键
            return  # 返回上一级菜单（科目菜单）
        elif choice == '0':  # 如果按下 '0' 键
            exit_program()  # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示无效选项

def get_client_data(client_id):
    """加载客户端的所有数据文件"""
    files = discover_files(client_id)  # 获取客户端所有文件路径
    client_data = {}  # 初始化客户端数据字典
    client_data['manifest'] = load_json(files['manifest'])  # 加载清单文件数据
    client_data['class_plans'] = load_json(files['class_plans'])  # 加载课表计划文件数据
    client_data['default_settings'] = load_json(files['default_settings'])  # 加载默认设置文件数据
    client_data['policies'] = load_json(files['policies'])  # 加载策略文件数据
    client_data['subjects_source'] = load_json(files['subjects_source'])  # 加载科目源文件数据
    client_data['time_layouts_source'] = load_json(files['time_layouts_source'])  # 加载时间布局源文件数据

    return files, client_data  # 返回文件路径字典和客户端数据字典

def exit_program():
    """退出程序"""
    print(f"{COLOR_BOLD}{COLOR_GREEN}程序已退出。{COLOR_RESET}")  # 打印绿色提示信息，表示程序退出
    sys.exit(0)  # 退出 Python 解释器

def main():
    """主程序入口"""
    if len(sys.argv) != 2:  # 检查命令行参数数量
        print(f"{COLOR_RED}用法: python DatasQuickEditor.py <ClientID>{COLOR_RESET}")  # 打印红色错误信息，提示用法
        return  # 退出程序

    client_id = sys.argv[1]  # 获取命令行参数中的 ClientID
    files, client_data = get_client_data(client_id)  # 加载客户端数据

    if not client_data['class_plans'] or not client_data['default_settings'] or not client_data['manifest'] or not client_data['policies'] or not client_data['subjects_source']:  # 检查关键数据是否加载成功
        print(f"{COLOR_RED}加载数据文件失败，请检查 ClientID '{client_id}' 的文件是否存在且完整。{COLOR_RESET}")  # 打印红色错误信息，提示数据文件加载失败
        return  # 退出程序

    subjects_data = client_data['subjects_source']  # 获取科目数据
    time_layouts_data = client_data['time_layouts_source']  # 获取时间布局数据

    while True:
        display_main_menu()  # 显示主菜单
        choice = msvcrt.getwch()  # 获取用户按键

        if choice == '1':  # 如果按下 '1' 键
            edit_class_plans_menu(files, client_data, subjects_data, time_layouts_data)  # 进入课表计划编辑菜单
        elif choice == '2':  # 如果按下 '2' 键
            display_default_settings(client_data['default_settings'], os.path.basename(files['default_settings']))  # 显示默认设置
        elif choice == '3':  # 如果按下 '3' 键
            display_manifests(client_data['manifest'], os.path.basename(files['manifest']))  # 显示清单
        elif choice == '4':  # 如果按下 '4' 键
            display_policies(client_data['policies'], os.path.basename(files['policies']))  # 显示策略
        elif choice == '5':  # 如果按下 '5' 键
            edit_subjects_source_menu(files, client_data)  # 进入科目编辑菜单
        elif choice == '0':  # 如果按下 '0' 键
            exit_program()  # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息，提示无效选项

if __name__ == "__main__":
    if os.name != 'nt':  # 检查操作系统是否为 Windows
        print(f"{COLOR_RED}警告: msvcrt 模块是 Windows 独有的，可能在非 Windows 系统上无法正常工作。{COLOR_RESET}")  # 打印红色警告信息，提示 msvcrt 模块的平台限制
    main()  # 调用主程序入口函数
