import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config(key):
    with open(CONFIG_PATH, 'r') as file:
        load = json.load(file)
        return load[key]

def write_config(data):
    try:
        with open(CONFIG_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to config.json: {e}", end='')