import json

def read_json(file_path : str) -> any:
    with open(file_path) as file:
        json_object = json.loads(file.read())
        return json_object
