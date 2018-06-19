import os
import json
import Helpers
import Decorators

data_path = "Data/" + "*id*" + "/CommandConfig.json"


def get_command(id, command):
     with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        JSON_file = json.load(f)
     f.close()
     return JSON_file[command]


def get_commands(id):
    "Gets CommandConig for server(id)."
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        JSON_file = json.load(f)
    f.close()
    return JSON_file


