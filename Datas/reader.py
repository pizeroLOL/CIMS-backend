import json
import os

class Resources:
    def __init__(self, path, name=None):
        self.path = path
        self.name = name if name is not None else path
        self.file_list = [f[:-5] for f in os.listdir(f"Datas/{self.path}")]

    def refresh(self) -> list[str]:
        self.file_list = [f[:-5] for f in os.listdir(f"Datas/{self.path}")]
        return self.file_list

    def read_file(self, name: str) -> dict:
        if name not in self.file_list:
            for n in self.file_list:
                if n in name or name in n:
                    raise FileNotFoundError(f"{self.name} '{name}' not found. Did you mean '{n}'? or refresh file list.")
            raise FileNotFoundError(f"{self.name} '{name}' not found, or refresh file list.")
        else:
            with open(f"Datas/{self.path}/{name}.json") as f:
                return json.load(f)

    def write_file(self, name: str, data: dict) -> None:
        if name not in self.file_list:
            raise FileNotFoundError(f"ClassPlan {name} not found, or refresh file list.")
        else:
            with open(f"Datas/{self.path}/{name}.json") as f:
                with open(f"Datas/{self.path}/{name}.json.bak", "w") as b:
                    b.write(f.read())
                    b.close()
            with open(f"Datas/{self.path}/{name}.json", "w") as f:
                json.dump(data, f)

    def __repr__(self):
        return f"{self.name}[" + ", ".join(self.file_list) + "]"

    def __str__(self):
        return f"{self.name}[" + ", ".join(self.file_list) + "]"

    def __iter__(self):
        for item in self.file_list:
            yield item, f"Datas/{self.path}/{item}.json"

    def __getitem__(self, item):
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
SubjectSource = Resources("SubjectSource", "SubjectSource")
TimeLayouts = Resources("TimeLayouts", "TimeLayouts")
