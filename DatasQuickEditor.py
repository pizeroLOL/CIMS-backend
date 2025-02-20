import json
import os
import msvcrt

# ANSI escape codes for colors and styles
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"
ANSI_MAGENTA = "\033[35m"
ANSI_CYAN = "\033[36m"

DATA_DIR = "Datas"
FILE_NAMES = {
    "1": "ClassPlans",
    "2": "DefaultSettings",
    "3": "Manifests",
    "4": "Policies",
    "5": "SubjectsSource",
}
FILE_EXT = ".json"
EXAMPLE_UUID = "26077a30-7859-49c0-aab3-9e04c3ffa270" # Using the provided example UUID


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def colored_text(text, color_code):
    return f"{color_code}{text}{ANSI_RESET}"

def bold_text(text):
    return colored_text(text, ANSI_BOLD)

def red_text(text):
    return colored_text(text, ANSI_RED)

def green_text(text):
    return colored_text(text, ANSI_GREEN)

def yellow_text(text):
    return colored_text(text, ANSI_YELLOW)

def blue_text(text):
    return colored_text(text, ANSI_BLUE)

def magenta_text(text):
    return colored_text(text, ANSI_MAGENTA)

def cyan_text(text):
    return colored_text(text, ANSI_CYAN)


def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(red_text(f"Error: File not found at {file_path}"))
        return None
    except json.JSONDecodeError:
        print(red_text(f"Error: Invalid JSON format in {file_path}"))
        return None

def save_json_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(green_text(f"Successfully saved changes to {file_path}"))
        return True
    except Exception as e:
        print(red_text(f"Error saving to {file_path}: {e}"))
        return False

def display_main_menu():
    clear_screen()
    print(bold_text("===== Datas Quick Editor ====="))
    print(f"Editing files for UUID: {cyan_text(EXAMPLE_UUID)}")
    print("Choose a file to edit:")
    for key, name in FILE_NAMES.items():
        print(f"  {bold_text(key)}. {name}{FILE_EXT}")
    print(f"  {bold_text('0')}. Exit")
    print("Enter your choice (0-5): ", end="")

def display_file_content(data, indent=2):
    if isinstance(data, dict):
        for key, value in data.items():
            print(" " * indent + bold_text(f"{key}:"), end=" ")
            if isinstance(value, (dict, list)):
                print() # Newline for nested structures
                display_file_content(value, indent + 4)
            else:
                print(value)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                display_file_content(item, indent + 2)
            else:
                print(" " * indent + str(item))
    else:
        print(data)

def edit_dict_recursive(data, path=""):
    if not isinstance(data, dict):
        print(red_text("Error: Cannot edit non-dictionary data directly."))
        return False

    while True:
        clear_screen()
        print(bold_text(f"===== Editing Path: {path} ====="))
        display_file_content(data)

        keys = list(data.keys())
        print("\nChoose an option:")
        for i, key in enumerate(keys):
            print(f"  {bold_text(str(i+1))}. Edit/View: {key}")
        print(f"  {bold_text('a')}. Add new entry (dict only)") # Only if current level is dict
        print(f"  {bold_text('d')}. Delete entry (dict only)") # Only if current level is dict
        print(f"  {bold_text('0')}. Back")
        print("Enter your choice: ", end="")

        choice = msvcrt.getwch()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(keys):
                selected_key = keys[index]
                if isinstance(data[selected_key], (dict, list)):
                    if not edit_dict_recursive(data[selected_key], path + "/" + selected_key):
                        return False # User wants to go back up
                else:
                    new_value = input(f"Enter new value for '{selected_key}' (current: {data[selected_key]}): ")
                    data[selected_key] = new_value
            elif choice == '0':
                return True # Go back to previous menu
            else:
                print(red_text("Invalid choice."))
                msvcrt.getwch() # Wait for key press

        elif choice.lower() == 'a' and isinstance(data, dict):
            new_key = input("Enter new key name: ")
            if new_key in data:
                print(red_text("Key already exists."))
            else:
                value_type_choice = input("Enter value type (string/number/boolean/dict/list): ").lower()
                if value_type_choice == 'string':
                    data[new_key] = ""
                elif value_type_choice == 'number':
                    data[new_key] = 0
                elif value_type_choice == 'boolean':
                    data[new_key] = False
                elif value_type_choice == 'dict':
                    data[new_key] = {}
                elif value_type_choice == 'list':
                    data[new_key] = []
                else:
                    print(red_text("Invalid value type. Defaulting to string."))
                    data[new_key] = ""

        elif choice.lower() == 'd' and isinstance(data, dict):
             keys_to_delete = list(data.keys()) # Get fresh keys in case dict changed
             if not keys_to_delete:
                 print(red_text("No entries to delete."))
             else:
                print("Select entry to delete:")
                for i, key in enumerate(keys_to_delete):
                    print(f"  {bold_text(str(i+1))}. Delete: {key}")
                delete_choice = input("Enter choice (or 0 to cancel): ")
                if delete_choice.isdigit():
                    delete_index = int(delete_choice) - 1
                    if 0 <= delete_index < len(keys_to_delete):
                        key_to_delete = keys_to_delete[delete_index]
                        del data[key_to_delete]
                        print(green_text(f"Entry '{key_to_delete}' deleted."))
                    elif delete_choice == '0':
                        pass # Cancelled
                    else:
                        print(red_text("Invalid delete choice."))
                else:
                    print(red_text("Invalid input."))

        elif choice == '0':
            return True # User wants to go back up
        else:
            print(red_text("Invalid choice."))
        msvcrt.getwch() # Wait for key press


def edit_list_recursive(data, path=""):
    if not isinstance(data, list):
        print(red_text("Error: Cannot edit non-list data as list."))
        return False

    while True:
        clear_screen()
        print(bold_text(f"===== Editing List Path: {path} ====="))
        display_file_content(data)

        print("\nChoose an option:")
        for i in range(len(data)):
            print(f"  {bold_text(str(i+1))}. Edit/View item at index {i}")
        print(f"  {bold_text('a')}. Add new item")
        print(f"  {bold_text('d')}. Delete item")
        print(f"  {bold_text('0')}. Back")
        print("Enter your choice: ", end="")

        choice = msvcrt.getwch()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(data):
                selected_item = data[index]
                if isinstance(selected_item, dict):
                    if not edit_dict_recursive(selected_item, path + f"[{index}]"):
                        return False # User wants to go back up
                elif isinstance(selected_item, list):
                    if not edit_list_recursive(selected_item, path + f"[{index}]"):
                        return False # User wants to go back up
                else:
                    new_value = input(f"Enter new value for item at index {index} (current: {selected_item}): ")
                    data[index] = new_value
            elif choice == '0':
                return True # Go back to previous menu
            else:
                print(red_text("Invalid choice."))
                msvcrt.getwch() # Wait for key press

        elif choice.lower() == 'a':
            value_type_choice = input("Enter new item type (string/number/boolean/dict/list): ").lower()
            if value_type_choice == 'string':
                data.append("")
            elif value_type_choice == 'number':
                data.append(0)
            elif value_type_choice == 'boolean':
                data.append(False)
            elif value_type_choice == 'dict':
                data.append({})
            elif value_type_choice == 'list':
                data.append([])
            else:
                print(red_text("Invalid value type. Defaulting to string."))
                data.append("")

        elif choice.lower() == 'd':
            if not data:
                print(red_text("No items to delete."))
            else:
                print("Select item index to delete:")
                for i in range(len(data)):
                    print(f"  {bold_text(str(i+1))}. Delete item at index {i}")
                delete_choice = input("Enter choice (or 0 to cancel): ")
                if delete_choice.isdigit():
                    delete_index = int(delete_choice) - 1
                    if 0 <= delete_index < len(data):
                        del data[delete_index]
                        print(green_text(f"Item at index {delete_index} deleted."))
                    elif delete_choice == '0':
                        pass # Cancelled
                    else:
                        print(red_text("Invalid delete choice."))
                else:
                    print(red_text("Invalid input."))

        elif choice == '0':
            return True # User wants to go back up
        else:
            print(red_text("Invalid choice."))
        msvcrt.getwch() # Wait for key press


def edit_file(file_key):
    file_name = FILE_NAMES[file_key] + FILE_EXT
    file_path = os.path.join(DATA_DIR, FILE_NAMES[file_key], EXAMPLE_UUID + FILE_EXT)
    data = load_json_file(file_path)
    if data is None:
        return

    while True:
        clear_screen()
        print(bold_text(f"===== Editing {file_name} ====="))
        display_file_content(data)

        print("\nChoose an action:")
        print(f"  {bold_text('e')}. Edit content")
        print(f"  {bold_text('s')}. Save changes")
        print(f"  {bold_text('r')}. Reload from file (discard changes)")
        print(f"  {bold_text('0')}. Back to Main Menu")
        print("Enter your choice: ", end="")

        action_choice = msvcrt.getwch()

        if action_choice.lower() == 'e':
            if isinstance(data, dict):
                edit_dict_recursive(data)
            elif isinstance(data, list):
                edit_list_recursive(data)
            else:
                print(red_text("Cannot edit content directly for this file structure."))
                msvcrt.getwch() # Wait for key press

        elif action_choice.lower() == 's':
            if save_json_file(file_path, data):
                pass # Success message already shown in save_json_file
            msvcrt.getwch() # Wait for key press

        elif action_choice.lower() == 'r':
            data = load_json_file(file_path) # Reload data, overwriting changes
            if data:
                print(yellow_text("File reloaded, changes discarded."))
            msvcrt.getwch() # Wait for key press

        elif action_choice == '0':
            return # Back to main menu

        else:
            print(red_text("Invalid action."))
            msvcrt.getwch() # Wait for key press


if __name__ == "__main__":
    while True:
        display_main_menu()
        choice = msvcrt.getwch()

        if choice in FILE_NAMES:
            edit_file(choice)
        elif choice == '0':
            print(green_text("Exiting editor."))
            break
        else:
            print(red_text("Invalid choice. Please try again."))
            msvcrt.getwch() # Wait for key press
