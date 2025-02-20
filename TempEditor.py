import json
import os
import msvcrt
import sys

# ANSI escape codes for colors and styles
COLOR_RESET = '\033[0m'
COLOR_BOLD = '\033[1m'
COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_BLUE = '\033[34m'
COLOR_MAGENTA = '\033[35m'
COLOR_CYAN = '\033[36m'

DATA_DIR = "Datas"

def load_json(filepath):
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
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"{COLOR_GREEN}文件已保存: {filepath}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_RED}错误: 保存文件失败: {filepath} - {e}{COLOR_RESET}")

def display_main_menu():
    print(f"\n{COLOR_BOLD}{COLOR_CYAN}主菜单{COLOR_RESET}")
    print(f"{COLOR_BOLD}请选择要编辑的文件:{COLOR_RESET}")
    print("1. ClassPlans (课表)")
    print("2. DefaultSettings (默认设置)")
    print("3. Manifests (清单)")
    print("4. Policies (策略)")
    print("5. SubjectsSource (科目)")
    print("0. 退出")

def display_class_plans(data, filename):
    print(f"\n{COLOR_BOLD}{COLOR_YELLOW}ClassPlans - {filename}{COLOR_RESET}")
    if not data or 'ClassPlans' not in data:
        print(f"{COLOR_RED}没有课表数据或数据格式错误。{COLOR_RESET}")
        return

    if not data['ClassPlans']:
        print(f"{COLOR_CYAN}没有课表计划。{COLOR_RESET}")
        return

    for plan_id, plan_data in data['ClassPlans'].items():
        print(f"\n  {COLOR_BOLD}课表计划 ID: {plan_id}{COLOR_RESET}")
        print(f"    名称: {plan_data.get('Name', '')}")
        print(f"    时间布局 ID: {plan_data.get('TimeLayoutId', '')}")
        time_rule = plan_data.get('TimeRule', {})
        weekday_str = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][time_rule.get('WeekDay', 0)] if 'WeekDay' in time_rule else "N/A"
        print(f"    星期: {weekday_str}")
        print(f"    是否启用: {'是' if plan_data.get('IsEnabled', False) else '否'}")

        print(f"    {COLOR_BOLD}课程:{COLOR_RESET}")
        if 'Classes' in plan_data and plan_data['Classes']:
            for i, class_item in enumerate(plan_data['Classes']):
                subject_name = get_subject_name(data, class_item.get('SubjectId', ''))
                subject_display = f"{subject_name} ({class_item.get('SubjectId', 'N/A')})" if subject_name else class_item.get('SubjectId', 'N/A')
                print(f"      {i+1}. 科目: {subject_display}, 更改课: {'是' if class_item.get('IsChangedClass', False) else '否'}, 启用: {'是' if class_item.get('IsActive', False) else '否'}")
        else:
            print(f"      {COLOR_CYAN}没有课程。{COLOR_RESET}")

def display_default_settings(data, filename):
    print(f"\n{COLOR_BOLD}{COLOR_YELLOW}DefaultSettings - {filename}{COLOR_RESET}")
    if not data:
        print(f"{COLOR_RED}没有默认设置数据或数据格式错误。{COLOR_RESET}")
        return

    print(f"  名称: {data.get('Name', '')}")
    print(f"  是否启用 Overlay ClassPlan: {'是' if data.get('IsOverlayClassPlanEnabled', False) else '否'}")
    print(f"  Overlay ClassPlan ID: {data.get('OverlayClassPlanId', 'N/A')}")
    print(f"  Temp ClassPlan ID: {data.get('TempClassPlanId', 'N/A')}")
    print(f"  Selected ClassPlan Group ID: {data.get('SelectedClassPlanGroupId', 'N/A')}")
    print(f"  Is Active: {'是' if data.get('IsActive', False) else '否'}")

def display_manifests(data, filename):
    print(f"\n{COLOR_BOLD}{COLOR_YELLOW}Manifests - {filename}{COLOR_RESET}")
    if not data:
        print(f"{COLOR_RED}没有清单数据或数据格式错误。{COLOR_RESET}")
        return

    print(f"  ServerKind: {data.get('ServerKind', 'N/A')}")
    print(f"  OrganizationName: {data.get('OrganizationName', 'N/A')}")

    print(f"\n  {COLOR_BOLD}数据源:{COLOR_RESET}")
    for key, source in data.items():
        if key.endswith("Source"):
            print(f"    {key}:")
            print(f"      Value: {source.get('Value', 'N/A')}")
            print(f"      Version: {source.get('Version', 'N/A')}")

def display_policies(data, filename):
    print(f"\n{COLOR_BOLD}{COLOR_YELLOW}Policies - {filename}{COLOR_RESET}")
    if not data:
        print(f"{COLOR_RED}没有策略数据或数据格式错误。{COLOR_RESET}")
        return

    for key, value in data.items():
        print(f"  {key}: {'是' if value else '否'}")

def display_subjects_source(data, filename):
    print(f"\n{COLOR_BOLD}{COLOR_YELLOW}SubjectsSource - {filename}{COLOR_RESET}")
    if not data or 'Subjects' not in data:
        print(f"{COLOR_RED}没有科目数据或数据格式错误。{COLOR_RESET}")
        return

    if not data['Subjects']:
        print(f"{COLOR_CYAN}没有科目。{COLOR_RESET}")
        return

    for subject_id, subject_data in data['Subjects'].items():
        print(f"\n  {COLOR_BOLD}科目 ID: {subject_id}{COLOR_RESET}")
        print(f"    名称: {subject_data.get('Name', '')}")
        print(f"    首字母: {subject_data.get('Initial', '')}")
        print(f"    教师名称: {subject_data.get('TeacherName', '')}")
        print(f"    户外课: {'是' if subject_data.get('IsOutDoor', False) else '否'}")
        print(f"    是否启用: {'是' if subject_data.get('IsActive', False) else '否'}")

def get_subject_name(data, subject_id):
    if 'SubjectsSource' in data and 'Subjects' in data['SubjectsSource'] and subject_id in data['SubjectsSource']['Subjects']:
        return data['SubjectsSource']['Subjects'][subject_id].get('Name', '')
    return None


def edit_class_plans_menu(data, filename):
    while True:
        display_class_plans(data, filename)
        print("\n  {COLOR_BOLD}课表计划编辑菜单:{COLOR_RESET}")
        print("  e. 编辑课表计划")
        print("  b. 返回主菜单")
        print("  0. 退出")

        choice = msvcrt.getwch().lower()

        if choice == 'e':
            edit_specific_class_plan(data, filename)
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def edit_specific_class_plan(data, filename):
    print("\n  {COLOR_BOLD}选择要编辑的课表计划 ID:{COLOR_RESET}")
    plan_ids = list(data['ClassPlans'].keys())
    for i, plan_id in enumerate(plan_ids):
        plan_name = data['ClassPlans'][plan_id].get('Name', '无名称')
        print(f"  {i+1}. {plan_name} - {plan_id}")

    while True:
        try:
            plan_index = int(input("  输入编号选择课表计划: ")) - 1
            if 0 <= plan_index < len(plan_ids):
                selected_plan_id = plan_ids[plan_index]
                break
            else:
                print(f"{COLOR_RED}编号超出范围，请重试。{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号。{COLOR_RESET}")

    if selected_plan_id:
        edit_class_plan_details(data, filename, selected_plan_id)


def edit_class_plan_details(data, filename, plan_id):
    while True:
        plan_data = data['ClassPlans'][plan_id]
        print(f"\n  {COLOR_BOLD}编辑课表计划: {plan_data.get('Name', '')} - {plan_id}{COLOR_RESET}")
        print("  1. 编辑名称")
        print("  2. 编辑时间规则")
        print("  3. 编辑课程")
        print("  b. 返回课表计划菜单")
        print("  0. 退出")

        choice = msvcrt.getwch().lower()

        if choice == '1':
            new_name = input("  输入新的课表计划名称: ")
            plan_data['Name'] = new_name
            save_json(get_full_path(filename), data)
        elif choice == '2':
            edit_time_rule(plan_data)
            save_json(get_full_path(filename), data)
        elif choice == '3':
            edit_classes_in_plan(data, filename, plan_id)
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def edit_time_rule(plan_data):
    time_rule = plan_data.setdefault('TimeRule', {}) # Ensure TimeRule exists

    while True:
        print("\n  {COLOR_BOLD}编辑时间规则:{COLOR_RESET}")
        weekday_str = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][time_rule.get('WeekDay', 0)] if 'WeekDay' in time_rule else "N/A"
        print(f"  当前星期: {weekday_str} (编号: {time_rule.get('WeekDay', 0)})")
        print(f"  当前 WeekCountDiv: {time_rule.get('WeekCountDiv', 0)}")
        print(f"  当前 WeekCountDivTotal: {time_rule.get('WeekCountDivTotal', 2)}")
        print(f"  是否启用: {'是' if time_rule.get('IsActive', False) else '否'}")

        print("  1. 编辑星期 (0-6, 0=星期日)")
        print("  2. 编辑 WeekCountDiv")
        print("  3. 编辑 WeekCountDivTotal")
        print("  4. 编辑是否启用")
        print("  b. 返回课表计划详情菜单")

        choice = msvcrt.getwch().lower()

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
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")


def edit_classes_in_plan(data, filename, plan_id):
    while True:
        plan_data = data['ClassPlans'][plan_id]
        print(f"\n  {COLOR_BOLD}编辑课表计划课程: {plan_data.get('Name', '')} - {plan_id}{COLOR_RESET}")

        if 'Classes' in plan_data and plan_data['Classes']:
            for i, class_item in enumerate(plan_data['Classes']):
                subject_name = get_subject_name(data, class_item.get('SubjectId', ''))
                subject_display = f"{subject_name} ({class_item.get('SubjectId', 'N/A')})" if subject_name else class_item.get('SubjectId', 'N/A')
                print(f"    {i+1}. 科目: {subject_display}, 更改课: {'是' if class_item.get('IsChangedClass', False) else '否'}, 启用: {'是' if class_item.get('IsActive', False) else '否'}")
        else:
            print(f"    {COLOR_CYAN}没有课程。{COLOR_RESET}")

        print("\n  课程编辑选项:")
        print("  a. 添加课程")
        print("  e. 编辑课程")
        print("  d. 删除课程")
        print("  b. 返回课表计划详情菜单")
        print("  0. 退出")

        choice = msvcrt.getwch().lower()

        if choice == 'a':
            add_class_to_plan(data, filename, plan_id)
        elif choice == 'e':
            edit_specific_class(data, filename, plan_id)
        elif choice == 'd':
            delete_class_from_plan(data, filename, plan_id)
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")


def add_class_to_plan(data, filename, plan_id):
    subject_id = input("  输入要添加的科目 ID: ")
    new_class = {
        "SubjectId": subject_id,
        "IsChangedClass": False,
        "AttachedObjects": {},
        "IsActive": False
    }
    data['ClassPlans'][plan_id]['Classes'].append(new_class)
    save_json(get_full_path(filename), data)
    print(f"{COLOR_GREEN}课程已添加。{COLOR_RESET}")


def edit_specific_class(data, filename, plan_id):
    plan_data = data['ClassPlans'][plan_id]
    if not plan_data.get('Classes'):
        print(f"{COLOR_RED}该课表计划没有课程可以编辑。{COLOR_RESET}")
        return

    while True:
        print("\n  {COLOR_BOLD}选择要编辑的课程编号:{COLOR_RESET}")
        for i, class_item in enumerate(plan_data['Classes']):
            subject_name = get_subject_name(data, class_item.get('SubjectId', ''))
            subject_display = f"{subject_name} ({class_item.get('SubjectId', 'N/A')})" if subject_name else class_item.get('SubjectId', 'N/A')
            print(f"    {i+1}. 科目: {subject_display}")

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
        edit_class_details(data, filename, plan_id, selected_class, class_index)


def edit_class_details(data, filename, plan_id, selected_class, class_index):
    while True:
        subject_name = get_subject_name(data, selected_class.get('SubjectId', ''))
        subject_display = f"{subject_name} ({selected_class.get('SubjectId', 'N/A')})" if subject_name else selected_class.get('SubjectId', 'N/A')
        print(f"\n  {COLOR_BOLD}编辑课程详情: {subject_display}{COLOR_RESET}")
        print("  1. 编辑科目 ID")
        print("  2. 编辑是否更改课")
        print("  3. 编辑是否启用")
        print("  b. 返回课程列表菜单")
        print("  0. 退出")

        choice = msvcrt.getwch().lower()

        if choice == '1':
            new_subject_id = input("  输入新的科目 ID: ")
            selected_class['SubjectId'] = new_subject_id
            save_json(get_full_path(filename), data)
        elif choice == '2':
            is_changed_input = input("  是否更改课 (yes/no): ").lower()
            selected_class['IsChangedClass'] = is_changed_input == 'yes'
            save_json(get_full_path(filename), data)
        elif choice == '3':
            is_active_input = input("  是否启用 (yes/no): ").lower()
            selected_class['IsActive'] = is_active_input == 'yes'
            save_json(get_full_path(filename), data)
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")


def delete_class_from_plan(data, filename, plan_id):
    plan_data = data['ClassPlans'][plan_id]
    if not plan_data.get('Classes'):
        print(f"{COLOR_RED}该课表计划没有课程可以删除。{COLOR_RESET}")
        return

    while True:
        print("\n  {COLOR_BOLD}选择要删除的课程编号:{COLOR_RESET}")
        for i, class_item in enumerate(plan_data['Classes']):
            subject_name = get_subject_name(data, class_item.get('SubjectId', ''))
            subject_display = f"{subject_name} ({class_item.get('SubjectId', 'N/A')})" if subject_name else class_item.get('SubjectId', 'N/A')
            print(f"    {i+1}. 科目: {subject_display}")

        print("  b. 返回课程列表菜单")
        print("  0. 退出")

        try:
            class_index_input = input("  输入课程编号删除 (或 'b' 返回): ")
            if class_index_input.lower() == 'b':
                return
            class_index = int(class_index_input) - 1

            if 0 <= class_index < len(plan_data['Classes']):
                del plan_data['Classes'][class_index]
                save_json(get_full_path(filename), data)
                print(f"{COLOR_GREEN}课程已删除。{COLOR_RESET}")
                return # Return to class list menu after deletion
            else:
                print(f"{COLOR_RED}课程编号超出范围，请重试。{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号或 'b' 返回。{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_RED}删除课程出错: {e}{COLOR_RESET}")
            return


def edit_subjects_source_menu(data, filename):
    while True:
        display_subjects_source(data, filename)
        print("\n  {COLOR_BOLD}科目编辑菜单:{COLOR_RESET}")
        print("  e. 编辑科目")
        print("  b. 返回主菜单")
        print("  0. 退出")

        choice = msvcrt.getwch().lower()

        if choice == 'e':
            edit_specific_subject(data, filename)
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

def edit_specific_subject(data, filename):
    print("\n  {COLOR_BOLD}选择要编辑的科目 ID:{COLOR_RESET}")
    subject_ids = list(data['Subjects'].keys())
    for i, subject_id in enumerate(subject_ids):
        subject_name = data['Subjects'][subject_id].get('Name', '无名称')
        print(f"  {i+1}. {subject_name} - {subject_id}")

    while True:
        try:
            subject_index = int(input("  输入编号选择科目: ")) - 1
            if 0 <= subject_index < len(subject_ids):
                selected_subject_id = subject_ids[subject_index]
                break
            else:
                print(f"{COLOR_RED}编号超出范围，请重试。{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_RED}无效的输入，请输入数字编号。{COLOR_RESET}")

    if selected_subject_id:
        edit_subject_details(data, filename, selected_subject_id)


def edit_subject_details(data, filename, subject_id):
    while True:
        subject_data = data['Subjects'][subject_id]
        print(f"\n  {COLOR_BOLD}编辑科目: {subject_data.get('Name', '')} - {subject_id}{COLOR_RESET}")
        print("  1. 编辑名称")
        print("  2. 编辑首字母")
        print("  3. 编辑教师名称")
        print("  4. 编辑是否户外课")
        print("  5. 编辑是否启用")
        print("  b. 返回科目菜单")
        print("  0. 退出")

        choice = msvcrt.getwch().lower()

        if choice == '1':
            new_name = input("  输入新的科目名称: ")
            subject_data['Name'] = new_name
            save_json(get_full_path(filename), data)
        elif choice == '2':
            new_initial = input("  输入新的科目首字母: ")
            subject_data['Initial'] = new_initial
            save_json(get_full_path(filename), data)
        elif choice == '3':
            new_teacher_name = input("  输入新的教师名称: ")
            subject_data['TeacherName'] = new_teacher_name
            save_json(get_full_path(filename), data)
        elif choice == '4':
            is_outdoor_input = input("  是否户外课 (yes/no): ").lower()
            subject_data['IsOutDoor'] = is_outdoor_input == 'yes'
            save_json(get_full_path(filename), data)
        elif choice == '5':
            is_active_input = input("  是否启用 (yes/no): ").lower()
            subject_data['IsActive'] = is_active_input == 'yes'
            save_json(get_full_path(filename), data)
        elif choice == 'b':
            return
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")


def get_file_id_from_filename(filename):
    return filename.replace(".json", "").split('-')[0]

def get_full_path(filename):
    file_id = get_file_id_from_filename(filename)
    return os.path.join(DATA_DIR, filename)

def exit_program():
    print(f"{COLOR_BOLD}{COLOR_GREEN}程序已退出。{COLOR_RESET}")
    sys.exit(0)

def main():
    filename = None
    data = None

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not filename.endswith(".json"):
            filename += ".json"
    else:
        print(f"{COLOR_RED}请在命令行中指定要编辑的文件名 (例如: DatasQuickEditor.py ClassPlans-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.json){COLOR_RESET}")
        return

    filepath = get_full_path(filename)
    data = load_json(filepath)
    if data is None:
        return

    # data['SubjectsSource'] = load_json(os.path.join(DATA_DIR, "SubjectsSource", filename))

    while True:
        display_main_menu()
        choice = msvcrt.getwch().lower()

        if choice == '1': # ClassPlans
            edit_class_plans_menu(data, filename)
        elif choice == '2': # DefaultSettings
            display_default_settings(data, filename) # For now, just display
        elif choice == '3': # Manifests
            display_manifests(data, filename) # For now, just display
        elif choice == '4': # Policies
            display_policies(data, filename) # For now, just display
        elif choice == '5': # SubjectsSource
            edit_subjects_source_menu(data['SubjectsSource'], filename)
        elif choice == '0':
            exit_program()
        else:
            print(f"{COLOR_RED}无效的选项，请重试。{COLOR_RESET}")

if __name__ == "__main__":
    if os.name != 'nt':
        print(f"{COLOR_RED}警告: msvcrt 模块是 Windows 独有的，可能在非 Windows 系统上无法正常工作。{COLOR_RESET}")
    main()
