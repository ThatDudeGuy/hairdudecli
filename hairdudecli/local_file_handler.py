import json
from pathlib import Path

DATA_PATH = Path.home() / ".local/share/hdcli.json"

# TODO:
# Could fail, need to catch it
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_local_data(values: list[str]):
    try:
        data = None
        local_data = open(DATA_PATH, "r")
        try:
            local_json: dict = json.load(local_data)
            for value in values:
                if local_json.get(value) is not None:
                    data = {value: local_json[value]}
        except Exception as e:
            print(f"Failed to get_local_data: {e}")
        local_data.close()
    except FileNotFoundError:
        return None
    finally:
        return data

def save_local_data(key_values: list[tuple]): # 2 tuple
    try:
        local_data = open(DATA_PATH, "r")
    except FileNotFoundError:
        local_data = open(DATA_PATH, "w")
        local_data.close()
    
    local_data = open(DATA_PATH, "r")
    local_json = {}
    try:
        local_json = json.load(local_data)
        local_data.close()
    except Exception as e:
        print("No user file found. Proceeding to create it...")

    local_data = open(DATA_PATH, "w")
    for kv in key_values:
        local_json[kv[0]] = kv[1]

    local_data.write(json.dumps(local_json))
    local_data.close()
