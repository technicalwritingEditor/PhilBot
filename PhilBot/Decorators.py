import json

def read_write_JSON(filePath):
    "A decorator for reading and then writing a json file"

    def decorator(func):
        def wrapper(*args):
            new_file_path = filePath.replace("*id*", args[0])
            with open(new_file_path, 'r') as f:
                JSON_file = json.load(f)
            f.close()

            JSON_file = func(*args, JSON_file)

            with open(new_file_path, 'w') as f:
                json.dump(JSON_file, f)
            f.close()
        return wrapper
    return decorator
