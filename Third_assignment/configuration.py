import json
import os

config_path = os.path.join(os.path.dirname(__file__), 'conf', 'conf.json')

with open(config_path, 'r') as config_file:
    conf = json.load(config_file)
