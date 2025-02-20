import json
import os
import msvcrt
import sys

# ANSI 转义码用于颜色和样式
COLOR_RESET = '\033[0m'
COLOR_BOLD = '\033[1m'
COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_BLUE = '\033[34m'
COLOR_MAGENTA = '\033[35m'
COLOR_CYAN = '\033[36m'

BG_GRAY = '\033[47m'
BG_BLUE = '\033[44m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_RED = '\033[41m'
BG_MAGENTA = '\033[45m'
BG_CYAN = '\033[46m'

DATA_DIR = "Datas"  # 数据文件夹路径

# ANSI 转义码用于方向键
ARROW_UP = '\033[A'
ARROW_DOWN = '\033[B'
ARROW_LEFT = '\033[D'
ARROW_RIGHT = '\033[C'

def load_json(filepath):
    """加载 JSON 文件数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{COLOR_RED}错误: 文件未找到: {filepath}{COLOR_RESET}")
        return None
    except json.JSONDecodeError:
        print(f"{COLOR_RED}错误: JSON解码错误: {filepath}{COLOR_RESET}")
        return None

def save_json(filepath, data):
    """保存数据到 JSON 文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"{COLOR_GREEN}文件已保存: {filepath}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_RED}错误: 保存文件失败: {filepath} - {e}{COLOR_RESET}")

def shorten_id(id_str):
    """缩短 ID 字符串"""
    if not id_str:
        return "N/A"
    if len(id_str) <= 7:
        return id_str
    return f"{id_str[:4]}...{id_str[-3:]}"

def discover_files(client_id):
    """根据 ClientID 发现所有相关的 JSON 文件路径"""
    base_filename = f"{client_id}.json"
    manifest_path = os.path.join(DATA_DIR, "Manifests", base_filename)
    class_plans_path = os.path.join(DATA_DIR, "ClassPlans", base_filename)
    default_settings_path = os.path.join(DATA_DIR, "DefaultSettings", base_filename)
    policies_path = os.path.join(DATA_DIR, "Policies", base_filename)
    subjects_source_path = os.path.join(DATA_DIR, "SubjectsSource", base_filename)
    time_layouts_source_path = os.path.join(DATA_DIR, "TimeLayouts", base_filename)

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
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{COLOR_BOLD}{BG_CYAN} 主菜单 {COLOR_RESET}{COLOR_RESET}")
    print(f"{COLOR_BOLD}请选择要编辑的文件 (使用数字键):{COLOR_RESET}")
    print("1. 课表计划 (ClassPlans)")
    print("2. 默认设置 (DefaultSettings)")
    print("3. 清单 (Manifests)")
    print("4. 策略 (Policies)")
    print("5. 科目 (SubjectsSource)")
    print("0. 退出")

def get_subject_name(subjects_data, subject_id):
    """根据科目 ID 获取科目名称"""
    if subjects_data and 'Subjects' in subjects_data and subject_id in subjects_data['Subjects']:
        return subjects_data['Subjects'][subject_id].get('Name', '未知科目')
    return "未知科目"

def get_time_layout_name(time_layouts_data, time_layout_id):
    """根据时间布局 ID 获取时间布局名称"""
    if time_layouts_data and 'TimeLayouts' in time_layouts_data and time_layout_id in time_layouts_data['TimeLayouts']:
        return time_layouts_data['TimeLayouts'][time_layout_id].get('Name', '未知时间布局')
    return "未知时间布局"

def display_class_plans(data, subjects_data, time_layouts_data, filename, plan_index):
    """显示单个课表计划的详细信息"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COLOR_BOLD}{BG_YELLOW} 课表计划 - {filename} {COLOR_RESET}{COLOR_RESET}")
    if not data or 'ClassPlans' not in data:
        print(f"{COLOR_RED}没有课表数据或数据格式错误。{COLOR_RESET}")
        return

    plan_ids = list(data['ClassPlans'].keys())
    if not plan_ids:
        print(f"{COLOR_CYAN}没有课表计划。{COLOR_RESET}")
        return

    if plan_index < 0 or plan_index >= len(plan_ids):
        plan_index = 0 # Reset index if out of bounds, should not happen in normal flow but for safety

    plan_id = plan_ids[plan_index]
    display_plan = data['ClassPlans'][plan_id]

    weekday_str = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][display_plan.get('TimeRule', {}).get('WeekDay', 0)] if 'WeekDay' in display_plan.get('TimeRule', {}) else "N/A"
    time_layout_name = get_time_layout_name(time_layouts_data, display_plan.get('TimeLayoutId', ''))

    print(f"ID: {shorten_id(plan_id)}")
    print(f"名称: {display_plan.get('Name', '')}")
    print(f"时间布局: {time_layout_name} ({shorten_id(display_plan.get('TimeLayoutId', ''))})")
    print(f"星期: {weekday_str}")
    print(f"启用: {'是' if display_plan.get('IsEnabled', False) else '否'}")

    print(f"\n课程:")
    if 'Classes' in display_plan and display_plan['Classes']:
        for class_item in display_plan['Classes']:
            subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', ''))
            subject_display = f"- 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"
            print(f"  {subject_display}, 更改课: {'是' if class_item.get('IsChangedClass', False) else '否'}, 启用: {'是' if class_item.get('IsActive', False) else '否'}")
    else:
        print(f"  {COLOR_CYAN}没有课程。{COLOR_RESET}")

    print("-" * 30)
    print(f"课表计划: {plan_index + 1}/{len(plan_ids)}")
    print("{COLOR_BOLD}操作:{COLOR_RESET} (方向键 ↑↓ 切换课表, 'e' 编辑, 'b' 返回主菜单, '0' 退出)")

def display_default_settings(data, filename):
    """显示默认设置信息"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 默认设置 - {filename} {COLOR_RESET}{COLOR_RESET}")
    if not data:
        print(f"{COLOR_RED}没有默认设置数据或数据格式错误。{COLOR_RESET}")
        return

    print(f"  名称: {data.get('Name', '')}")
    print(f"  是否启用 Overlay ClassPlan: {'是' if data.get('IsOverlayClassPlanEnabled', False) else '否'}")
    print(f"  Overlay ClassPlan ID: {shorten_id(data.get('OverlayClassPlanId', 'N/A'))}")
    print(f"  Temp ClassPlan ID: {shorten_id(data.get('TempClassPlanId', 'N/A'))}")
    print(f"  Selected ClassPlan Group ID: {shorten_id(data.get('SelectedClassPlanGroupId', 'N/A'))}")
    print(f"  Is Active: {'是' if data.get('IsActive', False) else '否'}")
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")

def display_manifests(data, filename):
    """显示清单信息"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 清单 - {filename} {COLOR_RESET}{COLOR_RESET}")
    if not data:
        print(f"{COLOR_RED}没有清单数据或数据格式错误。{COLOR_RESET}")
        return

    print(f"  服务器类型 (ServerKind): {data.get('ServerKind', 'N/A')}")
    print(f"  组织名称 (OrganizationName): {data.get('OrganizationName', 'N/A')}")

    print(f"\n  {COLOR_BOLD}数据源:{COLOR_RESET}")
    for key, source in data.items():
        if key.endswith("Source"):
            print(f"    {key}:")
            print(f"      值 (Value): {source.get('Value', 'N/A')}")
            print(f"      版本 (Version): {source.get('Version', 'N/A')}")
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")

def display_policies(data, filename):
    """显示策略信息"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 策略 - {filename} {COLOR_RESET}{COLOR_RESET}")
    if not data:
        print(f"{COLOR_RED}没有策略数据或数据格式错误。{COLOR_RESET}")
        return

    for key, value in data.items():
        print(f"  {key}: {'是' if value else '否'}")
    print("\n{COLOR_BOLD}操作:{COLOR_RESET} ('b' 返回主菜单, '0' 退出)")

def display_subjects_source(data, filename, subject_index):
    """显示单个科目的详细信息"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{COLOR_BOLD}{BG_YELLOW} 科目 - {filename} {COLOR_RESET}{COLOR_RESET}")
    if not data or 'Subjects' not in data:
        print(f"{COLOR_RED}没有科目数据或数据格式错误。{COLOR_RESET}")
        return

    subject_ids = list(data['Subjects'].keys())
    if not subject_ids:
        print(f"{COLOR_CYAN}没有科目。{COLOR_RESET}")
        return

    if subject_index < 0 or subject_index >= len(subject_ids):
        subject_index = 0 # Reset index if out of bounds

    subject_id = subject_ids[subject_index]
    subject_data = data['Subjects'][subject_id]

    print(f"科目 ID: {shorten_id(subject_id)}")
    print(f"名称: {subject_data.get('Name', '')}")
    print(f"首字母: {subject_data.get('Initial', '')}")
    print(f"教师名称: {subject_data.get('TeacherName', '')}")
    print(f"户外课: {'是' if subject_data.get('IsOutDoor', False) else '否'}")
    print(f"启用: {'是' if subject_data.get('IsActive', False) else '否'}")

    print("-" * 30)
    print(f"科目: {subject_index + 1}/{len(subject_ids)}")
    print("{COLOR_BOLD}操作:{COLOR_RESET} (方向键 ↑↓ 切换科目, 'e' 编辑, 'b' 返回主菜单, '0' 退出)")


def edit_class_plans_menu(files, client_data, subjects_data, time_layouts_data):
    """课表计划编辑菜单"""
    plan_index = 0 # Start with the first plan
    while True:
        display_class_plans(client_data['class_plans'], subjects_data, time_layouts_data, os.path.basename(files['class_plans']), plan_index)
        key_stroke = msvcrt.getwch()

        if key_stroke == 'e':
            plan_ids = list(client_data['class_plans']['ClassPlans'].keys())
            selected_plan_id = plan_ids[plan_index]
            edit_class_plan_details(files, client_data, subjects_data, time_layouts_data, selected_plan_id)
        elif key_stroke == 'b':
            return
        elif key_stroke == '0':
            exit_program()
        elif key_stroke == ARROW_UP:
            plan_index = max(0, plan_index - 1) # Move to previous plan
        elif key_stroke == ARROW_DOWN:
            plan_ids = list(client_data['class_plans']['ClassPlans'].keys())
            plan_index = min(len(plan_ids) - 1, plan_index + 1) # Move to next plan
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def edit_specific_class_plan(files, client_data, subjects_data, time_layouts_data, selected_plan_index):
    """编辑特定课表计划 (不再需要，直接在 edit_class_plans_menu 中编辑当前选中的)"""
    pass # This function is now redundant as edit happens directly in menu

def edit_class_plan_details(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑课表计划详情菜单"""
    while True:
        plan_data = client_data['class_plans']['ClassPlans'][plan_id]
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课表计划: {plan_data.get('Name', '')} - {shorten_id(plan_id)} {COLOR_RESET}{COLOR_RESET}")
        print("1. 编辑名称")
        print("2. 编辑时间规则")
        print("3. 编辑课程")
        print("b. 返回课表计划菜单")
        print("0. 退出")

        choice = msvcrt.getwch()

        if choice == '1':
            new_name = input("  输入新的课表计划名称: ")
            client_data['class_plans']['ClassPlans'][plan_id]['Name'] = new_name
            save_json(files['class_plans'], client_data['class_plans'])
        elif choice == '2':
            edit_time_rule(plan_data)
            save_json(files['class_plans'], client_data['class_plans'])
        elif choice == '3':
            edit_classes_in_plan(files, client_data, subjects_data, time_layouts_data, plan_id)
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def edit_time_rule(plan_data):
    """编辑时间规则菜单"""
    time_rule = plan_data.setdefault('TimeRule', {})

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑时间规则 {COLOR_RESET}{COLOR_RESET}")
        weekday_str = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][time_rule.get('WeekDay', 0)] if 'WeekDay' in time_rule else "N/A"
        print(f"  当前星期: {weekday_str} (编号: {time_rule.get('WeekDay', 0)})")
        print(f"  当前 WeekCountDiv: {time_rule.get('WeekCountDiv', 0)}")
        print(f"  当前 WeekCountDivTotal: {time_rule.get('WeekCountDivTotal', 2)}")
        print(f"  是否启用: {'是' if time_rule.get('IsActive', False) else '否'}")

        print("1. 编辑星期 (0-6, 0=星期日)")
        print("2. 编辑 WeekCountDiv")
        print("3. 编辑 WeekCountDivTotal")
        print("4. 编辑是否启用")
        print("b. 返回课表计划详情菜单")
        print("0. 退出")

        choice = msvcrt.getwch()

        if choice == '1':
            try:
                weekday = int(input("  输入新的星期编号 (0-6): "))
                if 0 <= weekday <= 6:
                    time_rule['WeekDay'] = weekday
                else:
                    print(f"{COLOR_RED}星期编号超出范围 (0-6)。{COLOR_RESET}")
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}")
        elif choice == '2':
            try:
                week_div = int(input("  输入新的 WeekCountDiv: "))
                time_rule['WeekCountDiv'] = week_div
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}")
        elif choice == '3':
            try:
                week_div_total = int(input("  输入新的 WeekCountDivTotal: "))
                time_rule['WeekCountDivTotal'] = week_div_total
            except ValueError:
                print(f"{COLOR_RED}无效的输入，请输入数字。{COLOR_RESET}")
        elif choice == '4':
            is_active_input = input("  是否启用 (yes/no): ").lower()
            time_rule['IsActive'] = is_active_input == 'yes'
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def edit_classes_in_plan(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑课表计划中的课程菜单"""
    while True:
        plan_data = client_data['class_plans']['ClassPlans'][plan_id]
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课表计划课程: {plan_data.get('Name', '')} - {shorten_id(plan_id)} {COLOR_RESET}{COLOR_RESET}")

        if 'Classes' in plan_data and plan_data['Classes']:
            for i, class_item in enumerate(plan_data['Classes']):
                subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', ''))
                subject_display = f"- {i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"
                print(f"    {subject_display}, 更改课: {'是' if class_item.get('IsChangedClass', False) else '否'}, 启用: {'是' if class_item.get('IsActive', False) else '否'}")
        else:
            print(f"    {COLOR_CYAN}没有课程。{COLOR_RESET}")

        print("\n课程编辑选项:")
        print("a. 添加课程")
        print("e. 编辑课程")
        print("d. 删除课程")
        print("b. 返回课表计划详情菜单")
        print("0. 退出")

        choice = msvcrt.getwch()

        if choice == 'a':
            add_class_to_plan(files, client_data, plan_id)
        elif choice == 'e':
            edit_specific_class(files, client_data, subjects_data, time_layouts_data, plan_id)
        elif choice == 'd':
            delete_class_from_plan(files, client_data, plan_id)
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def add_class_to_plan(files, client_data, plan_id):
    """添加课程到课表计划"""
    subject_id = input("  输入要添加的科目 ID: ")
    new_class = {
        "SubjectId": subject_id,
        "IsChangedClass": False,
        "AttachedObjects": {},
        "IsActive": False
    }
    client_data['class_plans']['ClassPlans'][plan_id]['Classes'].append(new_class)
    save_json(files['class_plans'], client_data['class_plans'])
    print(f"{COLOR_GREEN}课程已添加。{COLOR_RESET}")

def edit_specific_class(files, client_data, subjects_data, time_layouts_data, plan_id):
    """编辑特定课程菜单"""
    plan_data = client_data['class_plans']['ClassPlans'][plan_id]
    if not plan_data.get('Classes'):
        print(f"{COLOR_RED}该课表计划没有课程可以编辑。{COLOR_RESET}")
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR_BOLD}{BG_YELLOW} 选择要编辑的课程编号 {COLOR_RESET}{COLOR_RESET}")
        for i, class_item in enumerate(plan_data['Classes']):
            subject_name = get_subject_name(subjects_data, class_item.get('SubjectId', ''))
            subject_display = f"{i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"
            print(f"    {subject_display}")

        try:
            class_index = int(input("  输入课程编号选择编辑: ")) - 1
            if 0 <= class_index < len(plan_data['Classes']):
                selected_class = plan_data['Classes'][class_index]
                break
            else:
                print(f"{COLOR_RED}课程编号超出范围，请重试。{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号。{COLOR_RESET}")

    if selected_class:
        edit_class_details(files, client_data, subjects_data, plan_id, selected_class, class_index)

def edit_class_details(files, client_data, subjects_data, plan_id, selected_class, class_index):
    """编辑课程详情菜单"""
    while True:
        subject_name = get_subject_name(subjects_data, selected_class.get('SubjectId', ''))
        subject_display = f"{subject_name} ({shorten_id(selected_class.get('SubjectId', 'N/A'))})"
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑课程详情: {subject_display} {COLOR_RESET}{COLOR_RESET}")
        print("1. 编辑科目 ID")
        print("2. 编辑是否更改课")
        print("3. 编辑是否启用")
        print("b. 返回课程列表菜单")
        print("0. 退出")

        choice = msvcrt.getwch()

        if choice == '1':
            new_subject_id = input("  输入新的科目 ID: ")
            selected_class['SubjectId'] = new_subject_id
            save_json(files['class_plans'], client_data['class_plans'])
        elif choice == '2':
            is_changed_input = input("  是否更改课 (yes/no): ").lower()
            selected_class['IsChangedClass'] = is_changed_input == 'yes'
            save_json(files['class_plans'], client_data['class_plans'])
        elif choice == '3':
            is_active_input = input("  是否启用 (yes/no): ").lower()
            selected_class['IsActive'] = is_active_input == 'yes'
            save_json(files['class_plans'], client_data['class_plans'])
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def delete_class_from_plan(files, client_data, plan_id):
    """从课表计划中删除课程"""
    plan_data = client_data['class_plans']['ClassPlans'][plan_id]
    if not plan_data.get('Classes'):
        print(f"{COLOR_RED}该课表计划没有课程可以删除。{COLOR_RESET}")
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR_BOLD}{BG_YELLOW} 选择要删除的课程编号 {COLOR_RESET}{COLOR_RESET}")
        for i, class_item in enumerate(plan_data['Classes']):
            subject_name = get_subject_name(client_data['subjects_source'], class_item.get('SubjectId', ''))
            subject_display = f"{i+1}. 科目: {subject_name} ({shorten_id(class_item.get('SubjectId', 'N/A'))})"
            print(f"    {subject_display}")

        print("b. 返回课程列表菜单")
        print("0. 退出")

        try:
            class_index_input = input("  输入课程编号删除 (或 'b' 返回): ")
            if class_index_input.lower() == 'b':
                return
            class_index = int(class_index_input) - 1

            if 0 <= class_index < len(plan_data['Classes']):
                del plan_data['Classes'][class_index]
                save_json(files['class_plans'], client_data['class_plans'])
                print(f"{COLOR_GREEN}课程已删除。{COLOR_RESET}")
                return
            else:
                print(f"{COLOR_RED}课程编号超出范围，请重试。{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号或 'b' 返回。{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_RED}删除课程出错: {e}{COLOR_RESET}")
            return

def edit_subjects_source_menu(files, client_data):
    """科目编辑菜单"""
    subject_index = 0 # Start with the first subject
    while True:
        display_subjects_source(client_data['subjects_source'], os.path.basename(files['subjects_source']), subject_index)
        key_stroke = msvcrt.getwch()

        if key_stroke == 'e':
            subject_ids = list(client_data['subjects_source']['Subjects'].keys())
            selected_subject_id = subject_ids[subject_index]
            edit_subject_details(files, client_data, selected_subject_id)
        elif key_stroke == 'b':
            return
        elif key_stroke == '0':
            exit_program()
        elif key_stroke == ARROW_UP:
            subject_index = max(0, subject_index - 1) # Previous subject
        elif key_stroke == ARROW_DOWN:
            subject_ids = list(client_data['subjects_source']['Subjects'].keys())
            subject_index = min(len(subject_ids) - 1, subject_index + 1) # Next subject
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def edit_specific_subject(files, client_data, page_index):
    """编辑特定科目 (不再需要，直接在 edit_subjects_source_menu 编辑当前选中的)"""
    pass # Redundant function

def edit_subject_details(files, client_data, subject_id):
    """编辑科目详情菜单"""
    while True:
        subject_data = client_data['subjects_source']['Subjects'][subject_id]
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR_BOLD}{BG_YELLOW} 编辑科目: {subject_data.get('Name', '')} - {shorten_id(subject_id)} {COLOR_RESET}{COLOR_RESET}")
        print("1. 编辑名称")
        print("2. 编辑首字母")
        print("3. 编辑教师名称")
        print("4. 编辑是否户外课")
        print("5. 编辑是否启用")
        print("b. 返回科目菜单")
        print("0. 退出")

        choice = msvcrt.getwch()

        if choice == '1':
            new_name = input("  输入新的科目名称: ")
            client_data['subjects_source']['Subjects'][subject_id]['Name'] = new_name
            save_json(files['subjects_source'], client_data['subjects_source'])
        elif choice == '2':
            new_initial = input("  输入新的科目首字母: ")
            client_data['subjects_source']['Subjects'][subject_id]['Initial'] = new_initial
            save_json(files['subjects_source'], client_data['subjects_source'])
        elif choice == '3':
            new_teacher_name = input("  输入新的教师名称: ")
            client_data['subjects_source']['Subjects'][subject_id]['TeacherName'] = new_teacher_name
            save_json(files['subjects_source'], client_data['subjects_source'])
        elif choice == '4':
            is_outdoor_input = input("  是否户外课 (yes/no): ").lower()
            client_data['subjects_source']['Subjects'][subject_id]['IsOutDoor'] = is_outdoor_input == 'yes'
            save_json(files['subjects_source'], client_data['subjects_source'])
        elif choice == '5':
            is_active_input = input("  是否启用 (yes/no): ").lower()
            client_data['subjects_source']['Subjects'][subject_id]['IsActive'] = is_active_input == 'yes'
            save_json(files['subjects_source'], client_data['subjects_source'])
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def get_client_data(client_id):
    """加载客户端的所有数据文件"""
    files = discover_files(client_id)
    client_data = {}
    client_data['manifest'] = load_json(files['manifest'])
    client_data['class_plans'] = load_json(files['class_plans'])
    client_data['default_settings'] = load_json(files['default_settings'])
    client_data['policies'] = load_json(files['policies'])
    client_data['subjects_source'] = load_json(files['subjects_source'])
    client_data['time_layouts_source'] = load_json(files['time_layouts_source'])

    return files, client_data

def exit_program():
    """退出程序"""
    print(f"{COLOR_BOLD}{COLOR_GREEN}程序已退出。{COLOR_RESET}")
    sys.exit(0)

def main():
    """主程序入口"""
    if len(sys.argv) != 2:
        print(f"{COLOR_RED}用法: python DatasQuickEditor.py <ClientID>{COLOR_RESET}")
        return

    client_id = sys.argv[1]
    files, client_data = get_client_data(client_id)

    if not client_data['class_plans'] or not client_data['default_settings'] or not client_data['manifest'] or not client_data['policies'] or not client_data['subjects_source']:
        print(f"{COLOR_RED}加载数据文件失败，请检查 ClientID '{client_id}' 的文件是否存在且完整。{COLOR_RESET}")
        return

    subjects_data = client_data['subjects_source']
    time_layouts_data = client_data['time_layouts_source']

    while True:
        display_main_menu()
        choice = msvcrt.getwch()

        if choice == '1': # ClassPlans
            edit_class_plans_menu(files, client_data, subjects_data, time_layouts_data)
        elif choice == '2': # DefaultSettings
            display_default_settings(client_data['default_settings'], os.path.basename(files['default_settings']))
        elif choice == '3': # Manifests
            display_manifests(client_data['manifest'], os.path.basename(files['manifest']))
        elif choice == '4': # Policies
            display_policies(client_data['policies'], os.path.basename(files['policies']))
        elif choice == '5': # SubjectsSource
            edit_subjects_source_menu(files, client_data)
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

if __name__ == "__main__":
    if os.name != 'nt':
        print(f"{COLOR_RED}警告: msvcrt 模块是 Windows 独有的，可能在非 Windows 系统上无法正常工作。{COLOR_RESET}")
    main()
