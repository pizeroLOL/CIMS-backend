import json
import os

class Resources:
    def __init__(self, path, name=None):
        self.path: str = path
        self.name: str = name if name is not None else path
        self.file_list: list[str] = [f[:-5] for f in os.listdir(f"Datas/{self.path}")]

    def refresh(self) -> list[str]:
        self.file_list = [f[:-5] for f in os.listdir(f"Datas/{self.path}")]
        return self.file_list

    def read_file(self, name: str) -> dict:
        self.refresh()
        if name not in self.file_list:
            for n in self.file_list:
                if n in name or name in n:
                    raise FileNotFoundError(f"{self.name} '{name}' not found. Did you mean '{n}'?")
            raise FileNotFoundError(f"{self.name} '{name}' not found.")
        else:
            with open(f"Datas/{self.path}/{name}.json", encoding="utf-8") as f:
                return json.load(f)

    def write_file(self, name: str, data: dict) -> None:
        self.refresh()
        if name not in self.file_list:
            raise FileNotFoundError(f"{self.name} {name} not found.")
        else:
            with open(f"Datas/{self.path}/{name}.json") as f:
                with open(f"Datas/{self.path}/{name}.json.bak", "w") as b:
                    b.write(f.read())
                    b.close()
            with open(f"Datas/{self.path}/{name}.json", "w") as f:
                json.dump(data, f)

    def delete_file(self, name: str) -> None:
        self.refresh()
        if name not in self.file_list:
            raise FileNotFoundError(f"{self.name} {name} not found.")
        else:
            os.remove(f"Datas/{self.path}/{name}.json")
            self.refresh()
    
    def rename_file(self, name: str, new_name: str) -> None:
        self.refresh()
        if name not in self.file_list:
            raise FileNotFoundError(f"{self.name} {name} not found.")
        elif new_name not in self.file_list:
            raise FileExistsError(f"{self.name} {new_name} exists, please delete it first.")
        else:
            os.renames(f"Datas/{self.path}/{name}.json", f"Datas/{self.path}/{new_name}.json")

    def __repr__(self):
        self.refresh()
        return f"{self.name}[" + ", ".join(self.file_list) + "]"

    def __str__(self):
        self.refresh()
        return f"{self.name}[" + ", ".join(self.file_list) + "]"

    def __iter__(self):
        self.refresh()
        for item in self.file_list:
            yield item, f"Datas/{self.path}/{item}.json"

    def __getitem__(self, item):
        self.refresh()
        if item in self.file_list:
            return f"Datas/{self.path}/{item}.json"
        else:
            if item not in self.file_list:
                for n in self.file_list:
                    if n in item or item in n:
                        raise IndexError(f"{self.name} '{item}' not found. Did you mean '{n}'?")
                raise IndexError(f"{self.name} '{item}' not found.")


ClassPlans = Resources("ClassPlans", "ClassPlans")
DefaultSettings = Resources("DefaultSettings", "DefaultSettings")
Policies = Resources("Policies", "Policy")
SubjectsSource = Resources("SubjectsSource", "SubjectsSource")
TimeLayouts = Resources("TimeLayouts", "TimeLayouts")


class _ClientStatus:
    def __init__(self):
        with open("Datas/client_status.json") as f:
            self.client_status: dict[str: [dict[str: bool | float]]] = json.load(f)

    def refresh(self) -> dict[str: [dict[str: bool | float]]]:
        with open("Datas/client_status.json") as f:
            self.client_status = json.load(f)
            return self.client_status


ClientStatus = _ClientStatus()


class _Clients:
    def __init__(self):
        with open("Datas/clients.json") as f:
            self.clients: dict[str: str] = json.load(f)

    def refresh(self) -> dict[str: str]:
        with open("Datas/clients.json") as f:
            self.clients = json.load(f)
            return self.clients


Clients = _Clients()


class _ProfileConfig:
    def __init__(self):
        with open("Datas/profile_config.json") as f:
            self.profile_config: dict[str: dict[str: str]] = json.load(f)

    def refresh(self) -> dict[str: dict[str: str]]:
        with open("Datas/profile_config.json") as f:
            self.profile_config = json.load(f)
            return self.profile_config


ProfileConfig = _ProfileConfig()
