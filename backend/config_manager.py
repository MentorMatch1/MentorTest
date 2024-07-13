import json
import os

CONFIG_FILE = "config.json"


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_config(key, default=None):
    config = load_config()
    return config.get(key, default)


def update_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)
