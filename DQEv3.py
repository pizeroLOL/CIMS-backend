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
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{COLOR_RED}错误: 文件未找到: {filepath}{COLOR_RESET}")  # 打印红色错误信息
        return None
    except json.JSONDecodeError:
        print(f"{COLOR_RED}错误: JSON解码错误: {filepath}{COLOR_RESET}")  # 打印红色错误信息
        return None

def save_json(filepath, data):
    """保存数据到 JSON 文件

    Args:
        filepath (str): JSON 文件路径
        data (dict): 要保存的 JSON 数据字典
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"{COLOR_GREEN}文件已保存: {filepath}{COLOR_RESET}")  # 打印绿色成功信息
    except Exception as e:
        print(f"{COLOR_RED}错误: 保存文件失败: {filepath} - {e}{COLOR_RESET}")  # 打印红色错误信息

def shorten_id(id_str):
    """缩短 ID 字符串，保留前四位和后三位，中间用 '...' 代替

    Args:
        id_str (str): 要缩短的 ID 字符串

    Returns:
        str: 缩短后的 ID 字符串
    """
    if not id_str:
        return "N/A"  # 如果 ID 为空，则返回 "N/A"
    if len(id_str) <= 7:
        return id_str  # 如果 ID 长度小于等于 7，则不缩短
    return f"{id_str[:4]}...{id_str[-3:]}"  # 返回缩短后的 ID 字符串

def discover_files(client_id):
    """根据 ClientID 发现所有相关的 JSON 文件路径

    Args:
        client_id (str): 客户端 ID

    Returns:
        dict: 文件路径字典
    """
    base_filename = f"{client_id}.json"  # 基础文件名
    manifest_path = os.path.join(DATA_DIR, "Manifests", base_filename)  # 清单文件路径
    class_plans_path = os.path.join(DATA_DIR, "ClassPlans", base_filename)  # 课表计划文件路径
    default_settings_path = os.path.join(DATA_DIR, "DefaultSettings", base_filename)  # 默认设置文件路径
    policies_path = os.path.join(DATA_DIR, "Policies", base_filename)  # 策略文件路径
    subjects_source_path = os.path.join(DATA_DIR, "SubjectsSource", base_filename)  # 科目源文件路径
    time_layouts_source_path = os.path.join(DATA_DIR, "TimeLayouts", base_filename)  # 时间布局源文件路径

    return {
        "manifest": manifest_path,
        "class_plans": class_plans_path,
        "default_settings": default_settings_path,
        "policies": policies_path,
        "subjects_source": subjects_source_path,
        "time_layouts_source": time_layouts_source_path,
    }

def display_main_menu():
    """显示主菜单"""
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_CYAN} 主菜单 {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的主菜单标题
    print(f"{COLOR_BOLD}请选择要编辑的文件 (使用数字键):{COLOR_RESET}")  # 提示信息
    print("1. 课表计划 (ClassPlans)")  # 菜单选项 1
    print("2. 默认设置 (DefaultSettings)")  # 菜单选项 2
    print("3. 清单 (Manifests)")  # 菜单选项 3
    print("4. 策略 (Policies)")  # 菜单选项 4
    print("5. 科目 (SubjectsSource)")  # 菜单选项 5
    print("0. 退出")  # 菜单选项 0

def get_subject_name(subjects_data, subject_id):
    """根据科目 ID 获取科目名称

    Args:
        subjects_data (dict): 科目数据字典
        subject_id (str): 科目 ID

    Returns:
        str: 科目名称，如果找不到则返回 "未知科目"
    """
    if subjects_data and 'Subjects' in subjects_data and subject_id in subjects_data['Subjects']:
        return subjects_data['Subjects'][subject_id].get('Name', '未知科目')  # 返回科目名称，如果不存在则返回 "未知科目"
    return "未知科目"  # 如果科目数据为空或找不到科目，则返回 "未知科目"

def get_time_layout_name(time_layouts_data, time_layout_id):
    """根据时间布局 ID 获取时间布局名称

    Args:
        time_layouts_data (dict): 时间布局数据字典
        time_layout_id (str): 时间布局 ID

    Returns:
        str: 时间布局名称，如果找不到则返回 "未知时间布局"
    """
    if time_layouts_data and 'TimeLayouts' in time_layouts_data and time_layout_id in time_layouts_data['TimeLayouts']:
        return time_layouts_data['TimeLayouts'][time_layout_id].get('Name', '未知时间布局')  # 返回时间布局名称，如果不存在则返回 "未知时间布局"
    return "未知时间布局"  # 如果时间布局数据为空或找不到时间布局，则返回 "未知时间布局"

def display_class_plans(data, subjects_data, time_layouts_data, filename, page_index=0, items_per_page=5):
    """分页显示课表计划列表

    Args:
        data (dict): 课表计划数据字典
        subjects_data (dict): 科目数据字典
        time_layouts_data (dict): 时间布局数据字典
        filename (str): 文件名
        page_index (int): 当前页索引，默认为 0
        items_per_page (int): 每页显示的条目数，默认为 5
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"{COLOR_BOLD}{BG_YELLOW} 课表计划 - {filename} (页 {page_index + 1}) {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的标题和页码
    if not data or 'ClassPlans' not in data:
        print(f"{COLOR_RED}没有课表数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息
        return

    plan_ids = list(data['ClassPlans'].keys())  # 获取课表计划 ID 列表
    if not plan_ids:
        print(f"{COLOR_CYAN}没有课表计划。{COLOR_RESET}")  # 打印青色提示信息
        return

    start_index = page_index * items_per_page  # 计算起始索引
    end_index = min(start_index + items_per_page, len(plan_ids))  # 计算结束索引

    for i in range(start_index, end_index):
        plan_id = plan_ids[i]  # 获取当前页的课表计划 ID
        display_plan = data['ClassPlans'][plan_id]  # 获取课表计划数据
        prefix = "  "  # 前缀空格
        suffix = ""  # 后缀

        weekday_str = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][display_plan.get('TimeRule', {}).get('WeekDay', 0)] if 'WeekDay' in display_plan.get('TimeRule', {}) else "N/A"  # 获取星期字符串
        time_layout_name = get_time_layout_name(time_layouts_data, display_plan.get('TimeLayoutId', ''))  # 获取时间布局名称

        print(f"{prefix}ID: {shorten_id(plan_id)}{suffix}")  # 打印缩短后的课表计划 ID
        print(f"{prefix}名称: {display_plan.get('Name', '')}{suffix}")  # 打印课表计划名称
        print(f"{prefix}时间布局: {time_layout_name} ({shorten_id(display_plan.get('TimeLayoutId', ''))}){suffix}")  # 打印时间布局名称和缩短后的 ID
        print(f"{prefix}星期: {weekday_str}{suffix}")  # 打印星期
        print(f"{prefix}启用: {'是' if display_plan.get('IsEnabled', False) else '否'}{suffix}")  # 打印是否启用

        print(f"{prefix}课程:{suffix}")  # 打印课程标题
        if 'Classes' in display_plan and display_plan['Classes']:
            for class_item in display_plan['Classes']:
                subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', ''))  # 获取科目名称
                subject_display = f"- 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"  # 科目显示字符串，包含科目名称和缩短后的 ID
                print(f"{prefix}  {subject_display}, 更改课: {'是' if class_item.get('IsChangedClass', False) else '否'}, 启用: {'是' if class_item.get('IsActive', False) else '否'}{suffix}")  # 打印课程信息
        else:
            print(f"{prefix}  {COLOR_CYAN}没有课程。{COLOR_RESET}{suffix}")  # 打印没有课程的提示信息
        print() # 课表计划之间增加空行

    print("-" * 30)  # 分页线
    print(f"页: {page_index + 1}/{ (len(plan_ids) + items_per_page - 1) // items_per_page}")  # 打印页码信息
    print("{COLOR_BOLD}操作:{COLOR_RESET} (方向键 ← → 翻页, 'e' 编辑, 'b' 返回主菜单, '0' 退出)")  # 操作提示

def display_default_settings(data, filename):
    """显示默认设置信息

    Args:
        data (dict): 默认设置数据字典
        filename (str): 文件名
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 默认设置 - {filename} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的标题
    if not data:
        print(f"{COLOR_RED}没有默认设置数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息
        return

    print(f"  名称: {data.get('Name', '')}")  # 打印名称
    print(f"  是否启用 Overlay ClassPlan: {'是' if data.get('IsOverlayClassPlanEnabled', False) else '否'}")  # 打印是否启用 Overlay ClassPlan
    print(f"  Overlay ClassPlan ID: {shorten_id(data.get('OverlayClassPlanId', 'N/A'))}")  # 打印缩短后的 Overlay ClassPlan ID
    print(f"  Temp ClassPlan ID: {shorten_id(data.get('TempClassPlanId', 'N/A'))}")  # 打印缩短后的 Temp ClassPlan ID
    print(f"  Selected ClassPlan Group ID: {shorten_id(data.get('SelectedClassPlanGroupId', 'N/A'))}")  # 打印缩短后的 Selected ClassPlan Group ID
    print(f"  Is Active: {'是' if data.get('IsActive', False) else '否'}")  # 打印是否启用
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")  # 操作提示

def display_manifests(data, filename):
    """显示清单信息

    Args:
        data (dict): 清单数据字典
        filename (str): 文件名
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 清单 - {filename} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的标题
    if not data:
        print(f"{COLOR_RED}没有清单数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息
        return

    print(f"  服务器类型 (ServerKind): {data.get('ServerKind', 'N/A')}")  # 打印服务器类型
    print(f"  组织名称 (OrganizationName): {data.get('OrganizationName', 'N/A')}")  # 打印组织名称

    print(f"\n  {COLOR_BOLD}数据源:{COLOR_RESET}")  # 打印数据源标题
    for key, source in data.items():
        if key.endswith("Source"):
            print(f"    {key}:")  # 打印数据源类型
            print(f"      值 (Value): {source.get('Value', 'N/A')}")  # 打印数据源值
            print(f"      版本 (Version): {source.get('Version', 'N/A')}")  # 打印数据源版本
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")  # 操作提示

def display_policies(data, filename):
    """显示策略信息

    Args:
        data (dict): 策略数据字典
        filename (str): 文件名
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 策略 - {filename} {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的标题
    if not data:
        print(f"{COLOR_RED}没有策略数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息
        return

    for key, value in data.items():
        print(f"  {key}: {'是' if value else '否'}")  # 打印策略项和值
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")  # 操作提示

def display_subjects_source(data, filename, page_index=0, items_per_page=10):
    """分页显示科目列表

    Args:
        data (dict): 科目数据字典
        filename (str): 文件名
        page_index (int): 当前页索引，默认为 0
        items_per_page (int): 每页显示的条目数，默认为 10
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 科目 - {filename} (页 {page_index + 1}) {COLOR_RESET}{COLOR_RESET}")  # 打印带背景色的标题和页码
    if not data or 'Subjects' not in data:
        print(f"{COLOR_RED}没有科目数据或数据格式错误。{COLOR_RESET}")  # 打印红色错误信息
        return

    subject_ids = list(data['Subjects'].keys())  # 获取科目 ID 列表
    if not subject_ids:
        print(f"{COLOR_CYAN}没有科目。{COLOR_RESET}")  # 打印青色提示信息
        return

    start_index = page_index * items_per_page  # 计算起始索引
    end_index = min(start_index + items_per_page, len(subject_ids))  # 计算结束索引

    for i in range(start_index, end_index):
        subject_id = subject_ids[i]  # 获取当前页的科目 ID
        subject_data = data['Subjects'][subject_id]  # 获取科目数据
        prefix = "  "  # 前缀空格
        suffix = ""  # 后缀

        print(f"{prefix}科目 ID: {shorten_id(subject_id)}{suffix}")  # 打印缩短后的科目 ID
        print(f"{prefix}名称: {subject_data.get('Name', '')}{suffix}")  # 打印科目名称
        print(f"{prefix}首字母: {subject_data.get('Initial', '')}{suffix}")  # 打印科目首字母
        print(f"{prefix}教师名称: {subject_data.get('TeacherName', '')}{suffix}")  # 打印教师名称
        print(f"{prefix}户外课: {'是' if subject_data.get('IsOutDoor', False) else '否'}{suffix}")  # 打印是否户外课
        print(f"{prefix}启用: {'是' if subject_data.get('IsActive', False) else '否'}{suffix}")  # 打印是否启用
        print() # 科目之间增加空行

    print("-" * 30)  # 分页线
    print(f"页: {page_index + 1}/{ (len(subject_ids) + items_per_page - 1) // items_per_page}")  # 打印页码信息
    print("{COLOR_BOLD}操作:{COLOR_RESET} (方向键 ← → 翻页, 'e' 编辑, 'b' 返回主菜单, '0' 退出)")  # 操作提示

def edit_class_plans_menu(files, client_data, subjects_data, time_layouts_data):
    """课表计划编辑菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        subjects_data (dict): 科目数据字典
        time_layouts_data (dict): 时间布局数据字典
    """
    page_index = 0  # 初始化页索引
    while True:
        display_class_plans(client_data['class_plans'], subjects_data, time_layouts_data, os.path.basename(files['class_plans']), page_index)  # 显示课表计划列表
        key_stroke = msvcrt.getwch()  # 获取用户输入

        if key_stroke == 'e':
            edit_specific_class_plan(files, client_data, subjects_data, time_layouts_data, page_index)  # 编辑特定课表计划
        elif key_stroke == 'b':
            return  # 返回主菜单
        elif key_stroke == '0':
            exit_program()  # 退出程序
        elif key_stroke == ARROW_LEFT:
            page_index = max(0, page_index - 1)  # 上一页
        elif key_stroke == ARROW_RIGHT:
            max_pages = (len(client_data['class_plans']['ClassPlans']) + 5 - 1) // 5 # 假设 items_per_page 是 5
            page_index = min(max_pages - 1, page_index + 1) # 下一页
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")  # 打印红色错误信息

def edit_specific_class_plan(files, client_data, subjects_data, time_layouts_data, page_index):
    """编辑特定课表计划的菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        subjects_data (dict): 科目数据字典
        time_layouts_data (dict): 时间布局数据字典
        page_index (int): 当前页索引
    """
    plan_ids_on_page = list(client_data['class_plans']['ClassPlans'].keys())[page_index * 5 : (page_index + 1) * 5] # 假设 items_per_page 是 5
    if not plan_ids_on_page:
        print(f"{COLOR_RED}当前页没有课表计划可以编辑。{COLOR_RESET}") # 红色错误信息
        msvcrt.getwch() # 等待按键
        return

    print("\n  请选择要编辑的课表计划 ID (输入显示的ID):") # 提示信息
    for i, plan_id in enumerate(plan_ids_on_page):
        plan_name = client_data['class_plans']['ClassPlans'][plan_id].get('Name', '无名称') # 获取课表计划名称
        print(f"  {i+1}. {plan_name} - {shorten_id(plan_id)}") # 打印选项和缩短后的 ID

    while True:
        selected_id_input = input("  输入要编辑的课表计划ID (或 'b' 返回): ").strip() # 获取用户输入
        if selected_id_input.lower() == 'b':
            return # 返回课表计划菜单
        selected_plan_id = None
        for plan_id_on_page in plan_ids_on_page:
            if shorten_id(plan_id_on_page) == selected_id_input: # 比较缩短后的 ID
                selected_plan_id = plan_id_on_page
                break
        if selected_plan_id:
            edit_class_plan_details(files, client_data, subjects_data, time_layouts_data, selected_plan_id) # 编辑课表计划详情
            return
        else:
            print(f"{COLOR_RED}输入的ID无效，请重试或输入 'b' 返回。{COLOR_RESET}") # 红色错误信息

def edit_class_plan_details(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑课表计划详情菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        subjects_data (dict): 科目数据字典
        time_layouts_data (dict): 时间布局数据字典
        plan_id (str): 要编辑的课表计划 ID
    """
    while True:
        plan_data = client_data['class_plans']['ClassPlans'][plan_id] # 获取课表计划数据
        os.system('cls' if os.name == 'nt' else 'clear') # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课表计划: {plan_data.get('Name', '')} - {shorten_id(plan_id)} {COLOR_RESET}{COLOR_RESET}") # 打印带背景色的标题和缩短后的 ID
        print("1. 编辑名称") # 菜单选项 1
        print("2. 编辑时间规则") # 菜单选项 2
        print("3. 编辑课程") # 菜单选项 3
        print("b. 返回课表计划菜单") # 菜单选项 b
        print("0. 退出") # 菜单选项 0

        choice = msvcrt.getwch() # 获取用户输入

        if choice == '1':
            new_name = input("  输入新的课表计划名称: ") # 获取新的课表计划名称
            client_data['class_plans']['ClassPlans'][plan_id]['Name'] = new_name # 更新课表计划名称
            save_json(files['class_plans'], client_data['class_plans']) # 保存 JSON 文件
        elif choice == '2':
            edit_time_rule(plan_data) # 编辑时间规则
            save_json(files['class_plans'], client_data['class_plans']) # 保存 JSON 文件
        elif choice == '3':
            edit_classes_in_plan(files, client_data, subjects_data, time_layouts_data, plan_id) # 编辑课程
        elif choice == 'b':
            return # 返回课表计划菜单
        elif choice == '0':
            exit_program() # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}") # 打印红色错误信息

def edit_time_rule(plan_data):
    """编辑时间规则菜单

    Args:
        plan_data (dict): 课表计划数据字典
    """
    time_rule = plan_data.setdefault('TimeRule', {})  # 获取或设置 TimeRule，确保存在

    while True:
        os.system('cls' if os.name == 'nt' else 'clear') # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑时间规则 {COLOR_RESET}{COLOR_RESET}") # 打印带背景色的标题
        weekday_str = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][time_rule.get('WeekDay', 0)] if 'WeekDay' in time_rule else "N/A" # 获取星期字符串
        print(f"  当前星期: {weekday_str} (编号: {time_rule.get('WeekDay', 0)})") # 打印当前星期
        print(f"  当前 WeekCountDiv: {time_rule.get('WeekCountDiv', 0)}") # 打印当前 WeekCountDiv
        print(f"  当前 WeekCountDivTotal: {time_rule.get('WeekCountDivTotal', 2)}") # 打印当前 WeekCountDivTotal
        print(f"  是否启用: {'是' if time_rule.get('IsActive', False) else '否'}") # 打印是否启用

        print("1. 编辑星期 (0-6, 0=星期日)") # 菜单选项 1
        print("2. 编辑 WeekCountDiv") # 菜单选项 2
        print("3. 编辑 WeekCountDivTotal") # 菜单选项 3
        print("4. 编辑是否启用") # 菜单选项 4
        print("b. 返回课表计划详情菜单") # 菜单选项 b
        print("0. 退出") # 菜单选项 0

        choice = msvcrt.getwch() # 获取用户输入

        if choice == '1':
            try:
                weekday = int(input("  输入新的星期编号 (0-6): ")) # 获取新的星期编号
                if 0 <= weekday <= 6:
                    time_rule['WeekDay'] = weekday # 更新星期编号
                else:
                    print(f"{COLOR_RED}星期编号超出范围 (0-6)。{COLOR_RESET}") # 打印红色错误信息
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}") # 打印红色错误信息
        elif choice == '2':
            try:
                week_div = int(input("  输入新的 WeekCountDiv: ")) # 获取新的 WeekCountDiv
                time_rule['WeekCountDiv'] = week_div # 更新 WeekCountDiv
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}") # 打印红色错误信息
        elif choice == '3':
            try:
                week_div_total = int(input("  输入新的 WeekCountDivTotal: ")) # 获取新的 WeekCountDivTotal
                time_rule['WeekCountDivTotal'] = week_div_total # 更新 WeekCountDivTotal
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}") # 打印红色错误信息
        elif choice == '4':
            is_active_input = input("  是否启用 (yes/no): ").lower() # 获取是否启用的输入
            time_rule['IsActive'] = is_active_input == 'yes' # 更新是否启用
        elif choice == 'b':
            return # 返回课表计划详情菜单
        elif choice == '0':
            exit_program() # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}") # 打印红色错误信息

def edit_classes_in_plan(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑课表计划中的课程菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        subjects_data (dict): 科目数据字典
        time_layouts_data (dict): 时间布局数据字典
        plan_id (str): 课表计划 ID
    """
    while True:
        plan_data = client_data['class_plans']['ClassPlans'][plan_id] # 获取课表计划数据
        os.system('cls' if os.name == 'nt' else 'clear') # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课表计划课程: {plan_data.get('Name', '')} - {shorten_id(plan_id)} {COLOR_RESET}{COLOR_RESET}") # 打印带背景色的标题和缩短后的 ID

        if 'Classes' in plan_data and plan_data['Classes']:
            for i, class_item in enumerate(plan_data['Classes']):
                subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', '')) # 获取科目名称
                subject_display = f"- {i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})" # 科目显示字符串，包含科目名称和缩短后的 ID
                print(f"    {subject_display}, 更改课: {'是' if class_item.get('IsChangedClass', False) else '否'}, 启用: {'是' if class_item.get('IsActive', False) else '否'}") # 打印课程信息
        else:
            print(f"    {COLOR_CYAN}没有课程。{COLOR_RESET}") # 打印没有课程的提示信息

        print("\n课程编辑选项:") # 课程编辑选项标题
        print("a. 添加课程") # 菜单选项 a
        print("e. 编辑课程") # 菜单选项 e
        print("d. 删除课程") # 菜单选项 d
        print("b. 返回课表计划详情菜单") # 菜单选项 b
        print("0. 退出") # 菜单选项 0

        choice = msvcrt.getwch() # 获取用户输入

        if choice == 'a':
            add_class_to_plan(files, client_data, plan_id) # 添加课程
        elif choice == 'e':
            edit_specific_class(files, client_data, subjects_data, time_layouts_data, plan_id) # 编辑特定课程
        elif choice == 'd':
            delete_class_from_plan(files, client_data, plan_id) # 删除课程
        elif choice == 'b':
            return # 返回课表计划详情菜单
        elif choice == '0':
            exit_program() # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}") # 打印红色错误信息

def add_class_to_plan(files, client_data, plan_id):
    """添加课程到课表计划

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        plan_id (str): 课表计划 ID
    """
    subject_id = input("  输入要添加的科目 ID: ") # 获取要添加的科目 ID
    new_class = {
        "SubjectId": subject_id,
        "IsChangedClass": False,
        "AttachedObjects": {},
        "IsActive": False
    }
    client_data['class_plans']['ClassPlans'][plan_id]['Classes'].append(new_class) # 添加新课程到课表计划
    save_json(files['class_plans'], client_data['class_plans']) # 保存 JSON 文件
    print(f"{COLOR_GREEN}课程已添加。{COLOR_RESET}") # 打印绿色成功信息

def edit_specific_class(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑特定课程菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        subjects_data (dict): 科目数据字典
        time_layouts_data (dict): 时间布局数据字典
        plan_id (str): 课表计划 ID
    """
    plan_data = client_data['class_plans']['ClassPlans'][plan_id] # 获取课表计划数据
    if not plan_data.get('Classes'):
        print(f"{COLOR_RED}该课表计划没有课程可以编辑。{COLOR_RESET}") # 打印红色错误信息
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear') # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 选择要编辑的课程编号 {COLOR_RESET}{COLOR_RESET}") # 打印带背景色的标题
        for i, class_item in enumerate(plan_data['Classes']):
            subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', '')) # 获取科目名称
            subject_display = f"{i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})" # 科目显示字符串，包含科目名称和缩短后的 ID
            print(f"    {subject_display}") # 打印课程选项

        try:
            class_index = int(input("  输入课程编号选择编辑: ")) - 1 # 获取要编辑的课程编号
            if 0 <= class_index < len(plan_data['Classes']):
                selected_class = plan_data['Classes'][class_index] # 获取选中的课程数据
                break
            else:
                print(f"{COLOR_RED}课程编号超出范围，请重试。{COLOR_RESET}") # 打印红色错误信息
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号。{COLOR_RESET}") # 打印红色错误信息

    if selected_class:
        edit_class_details(files, client_data, subjects_data, plan_id, selected_class, class_index) # 编辑课程详情

def edit_class_details(files, client_data, subjects_data, plan_id, selected_class, class_index):
    """编辑课程详情菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        subjects_data (dict): 科目数据字典
        plan_id (str): 课表计划 ID
        selected_class (dict): 选中的课程数据字典
        class_index (int): 课程在列表中的索引
    """
    while True:
        subject_name = get_subject_name(subjects_data, selected_class.get('SubjectId', '')) # 获取科目名称
        subject_display = f"{subject_name} ({shorten_id(selected_class.get('SubjectId', 'N/A'))})" # 科目显示字符串，包含科目名称和缩短后的 ID
        os.system('cls' if os.name == 'nt' else 'clear') # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课程详情: {subject_display} {COLOR_RESET}{COLOR_RESET}") # 打印带背景色的标题和科目显示字符串
        print("1. 编辑科目 ID") # 菜单选项 1
        print("2. 编辑是否更改课") # 菜单选项 2
        print("3. 编辑是否启用") # 菜单选项 3
        print("b. 返回课程列表菜单") # 菜单选项 b
        print("0. 退出") # 菜单选项 0

        choice = msvcrt.getwch() # 获取用户输入

        if choice == '1':
            new_subject_id = input("  输入新的科目 ID: ") # 获取新的科目 ID
            selected_class['SubjectId'] = new_subject_id # 更新科目 ID
            save_json(files['class_plans'], client_data['class_plans']) # 保存 JSON 文件
        elif choice == '2':
            is_changed_input = input("  是否更改课 (yes/no): ").lower() # 获取是否更改课的输入
            selected_class['IsChangedClass'] = is_changed_input == 'yes' # 更新是否更改课
            save_json(files['class_plans'], client_data['class_plans']) # 保存 JSON 文件
        elif choice == '3':
            is_active_input = input("  是否启用 (yes/no): ").lower() # 获取是否启用的输入
            selected_class['IsActive'] = is_active_input == 'yes' # 更新是否启用
            save_json(files['class_plans'], client_data['class_plans']) # 保存 JSON 文件
        elif choice == 'b':
            return # 返回课程列表菜单
        elif choice == '0':
            exit_program() # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}") # 打印红色错误信息

def delete_class_from_plan(files, client_data, plan_id):
    """从课表计划中删除课程

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        plan_id (str): 课表计划 ID
    """
    plan_data = client_data['class_plans']['ClassPlans'][plan_id] # 获取课表计划数据
    if not plan_data.get('Classes'):
        print(f"{COLOR_RED}该课表计划没有课程可以删除。{COLOR_RESET}") # 打印红色错误信息
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear') # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 选择要删除的课程编号 {COLOR_RESET}{COLOR_RESET}") # 打印带背景色的标题
        for i, class_item in enumerate(plan_data['Classes']):
            subject_name = get_subject_name(client_data['subjects_source'], class_item.get('SubjectId', '')) # 获取科目名称
            subject_display = f"{i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})" # 科目显示字符串，包含科目名称和缩短后的 ID
            print(f"    {subject_display}") # 打印课程选项

        print("b. 返回课程列表菜单") # 菜单选项 b
        print("0. 退出") # 菜单选项 0

        try:
            class_index_input = input("  输入课程编号删除 (或 'b' 返回): ") # 获取要删除的课程编号输入
            if class_index_input.lower() == 'b':
                return # 返回课程列表菜单
            class_index = int(class_index_input) - 1 # 将输入转换为课程索引

            if 0 <= class_index < len(plan_data['Classes']):
                del plan_data['Classes'][class_index] # 从课程列表中删除课程
                save_json(files['class_plans'], client_data['class_plans']) # 保存 JSON 文件
                print(f"{COLOR_GREEN}课程已删除。{COLOR_RESET}") # 打印绿色成功信息
                return  # 返回课程列表菜单
            else:
                print(f"{COLOR_RED}课程编号超出范围，请重试。{COLOR_RESET}") # 打印红色错误信息
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号或 'b' 返回。{COLOR_RESET}") # 打印红色错误信息
        except Exception as e:
            print(f"{COLOR_RED}删除课程出错: {e}{COLOR_RESET}") # 打印红色错误信息
            return

def edit_subjects_source_menu(files, client_data, page_index=0):
    """科目编辑菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        page_index (int): 当前页索引，默认为 0
    """
    while True:
        display_subjects_source(client_data['subjects_source'], os.path.basename(files['subjects_source']), page_index) # 显示科目列表
        key_stroke = msvcrt.getwch() # 获取用户输入

        if key_stroke == 'e':
            edit_specific_subject(files, client_data, page_index) # 编辑特定科目
        elif key_stroke == 'b':
            return # 返回主菜单
        elif key_stroke == '0':
            exit_program() # 退出程序
        elif key_stroke == ARROW_LEFT:
            page_index = max(0, page_index - 1) # 上一页
        elif key_stroke == ARROW_RIGHT:
            max_pages = (len(client_data['subjects_source']['Subjects']) + 10 - 1) // 10 # 假设 items_per_page 是 10
            page_index = min(max_pages - 1, page_index + 1) # 下一页
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}") # 打印红色错误信息

def edit_specific_subject(files, client_data, page_index):
    """编辑特定科目的菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        page_index (int): 当前页索引
    """
    subject_ids_on_page = list(client_data['subjects_source']['Subjects'].keys())[page_index * 10 : (page_index + 1) * 10] # 假设 items_per_page 是 10
    if not subject_ids_on_page:
        print(f"{COLOR_RED}当前页没有科目可以编辑。{COLOR_RESET}") # 打印红色错误信息
        msvcrt.getwch() # 等待按键
        return

    print("\n  请选择要编辑的科目 ID (输入显示的ID):") # 提示信息
    for i, subject_id in enumerate(subject_ids_on_page):
        subject_name = client_data['subjects_source']['Subjects'][subject_id].get('Name', '无名称') # 获取科目名称
        print(f"  {i+1}. {subject_name} - {shorten_id(subject_id)}") # 打印选项和缩短后的 ID

    while True:
        selected_id_input = input("  输入要编辑的科目ID (或 'b' 返回): ").strip() # 获取用户输入
        if selected_id_input.lower() == 'b':
            return # 返回科目菜单
        selected_subject_id = None
        for subject_id_on_page in subject_ids_on_page:
            if shorten_id(subject_id_on_page) == selected_id_input: # 比较缩短后的 ID
                selected_subject_id = subject_id_on_page
                break
        if selected_subject_id:
            edit_subject_details(files, client_data, selected_subject_id) # 编辑科目详情
            return
        else:
            print(f"{COLOR_RED}输入的ID无效，请重试或输入 'b' 返回。{COLOR_RESET}") # 打印红色错误信息

def edit_subject_details(files, client_data, subject_id):
    """编辑科目详情菜单

    Args:
        files (dict): 文件路径字典
        client_data (dict): 客户端数据字典
        subject_id (str): 要编辑的科目 ID
    """
    while True:
        subject_data = client_data['subjects_source']['Subjects'][subject_id] # 获取科目数据
        os.system('cls' if os.name == 'nt' else 'clear') # 清屏
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑科目: {subject_data.get('Name', '')} - {shorten_id(subject_id)} {COLOR_RESET}{COLOR_RESET}") # 打印带背景色的标题和缩短后的 ID
        print("1. 编辑名称") # 菜单选项 1
        print("2. 编辑首字母") # 菜单选项 2
        print("3. 编辑教师名称") # 菜单选项 3
        print("4. 编辑是否户外课") # 菜单选项 4
        print("5. 编辑是否启用") # 菜单选项 5
        print("b. 返回科目菜单") # 菜单选项 b
        print("0. 退出") # 菜单选项 0

        choice = msvcrt.getwch() # 获取用户输入

        if choice == '1':
            new_name = input("  输入新的科目名称: ") # 获取新的科目名称
            client_data['subjects_source']['Subjects'][subject_id]['Name'] = new_name # 更新科目名称
            save_json(files['subjects_source'], client_data['subjects_source']) # 保存 JSON 文件
        elif choice == '2':
            new_initial = input("  输入新的科目首字母: ") # 获取新的科目首字母
            client_data['subjects_source']['Subjects'][subject_id]['Initial'] = new_initial # 更新科目首字母
            save_json(files['subjects_source'], client_data['subjects_source']) # 保存 JSON 文件
        elif choice == '3':
            new_teacher_name = input("  输入新的教师名称: ") # 获取新的教师名称
            client_data['subjects_source']['Subjects'][subject_id]['TeacherName'] = new_teacher_name # 更新教师名称
            save_json(files['subjects_source'], client_data['subjects_source']) # 保存 JSON 文件
        elif choice == '4':
            is_outdoor_input = input("  是否户外课 (yes/no): ").lower() # 获取是否户外课的输入
            client_data['subjects_source']['Subjects'][subject_id]['IsOutDoor'] = is_outdoor_input == 'yes' # 更新是否户外课
            save_json(files['subjects_source'], client_data['subjects_source']) # 保存 JSON 文件
        elif choice == '5':
            is_active_input = input("  是否启用 (yes/no): ").lower() # 获取是否启用的输入
            client_data['subjects_source']['Subjects'][subject_id]['IsActive'] = is_active_input == 'yes' # 更新是否启用
            save_json(files['subjects_source'], client_data['subjects_source']) # 保存 JSON 文件
        elif choice == 'b':
            return # 返回科目菜单
        elif choice == '0':
            exit_program() # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}") # 打印红色错误信息

def get_client_data(client_id):
    """加载客户端的所有数据文件

    Args:
        client_id (str): 客户端 ID

    Returns:
        tuple: 文件路径字典和客户端数据字典
    """
    files = discover_files(client_id) # 发现文件路径
    client_data = {} # 初始化客户端数据字典
    client_data['manifest'] = load_json(files['manifest']) # 加载清单数据
    client_data['class_plans'] = load_json(files['class_plans']) # 加载课表计划数据
    client_data['default_settings'] = load_json(files['default_settings']) # 加载默认设置数据
    client_data['policies'] = load_json(files['policies']) # 加载策略数据
    client_data['subjects_source'] = load_json(files['subjects_source']) # 加载科目源数据
    client_data['time_layouts_source'] = load_json(files['time_layouts_source']) # 加载时间布局源数据

    return files, client_data # 返回文件路径字典和客户端数据字典

def exit_program():
    """退出程序"""
    print(f"{COLOR_BOLD}{COLOR_GREEN}程序已退出。{COLOR_RESET}") # 打印绿色退出信息
    sys.exit(0) # 退出程序

def main():
    """主程序入口"""
    if len(sys.argv) != 2:
        print(f"{COLOR_RED}用法: python DatasQuickEditor.py <ClientID>{COLOR_RESET}") # 打印红色用法信息
        return

    client_id = sys.argv[1] # 获取客户端 ID
    files, client_data = get_client_data(client_id) # 加载客户端数据

    if not client_data['class_plans'] or not client_data['default_settings'] or not client_data['manifest'] or not client_data['policies'] or not client_data['subjects_source']:
        print(f"{COLOR_RED}加载数据文件失败，请检查 ClientID '{client_id}' 的文件是否存在且完整。{COLOR_RESET}") # 打印红色错误信息
        return

    subjects_data = client_data['subjects_source'] # 获取科目数据，修复 NameError
    time_layouts_data = client_data['time_layouts_source'] # 获取时间布局数据

    while True:
        display_main_menu() # 显示主菜单
        choice = msvcrt.getwch() # 获取用户输入

        if choice == '1': # ClassPlans
            edit_class_plans_menu(files, client_data, subjects_data, time_layouts_data) # 进入课表计划编辑菜单
        elif choice == '2': # DefaultSettings
            display_default_settings(client_data['default_settings'], os.path.basename(files['default_settings'])) # 显示默认设置
        elif choice == '3': # Manifests
            display_manifests(client_data['manifest'], os.path.basename(files['manifest'])) # 显示清单
        elif choice == '4': # Policies
            display_policies(client_data['policies'], os.path.basename(files['policies'])) # 显示策略
        elif choice == '5': # SubjectsSource
            edit_subjects_source_menu(files, client_data) # 进入科目编辑菜单
        elif choice == '0':
            exit_program() # 退出程序
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}") # 打印红色错误信息

if __name__ == "__main__":
    if os.name != 'nt':
        print(f"{COLOR_RED}警告: msvcrt 模块是 Windows 独有的，可能在非 Windows 系统上无法正常工作。{COLOR_RESET}") # 打印红色警告信息
    main() # 调用主程序入口
