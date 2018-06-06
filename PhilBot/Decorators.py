import json

def ReadWriteJson(filePath):
    "A decorator for reading and then writing a json file"

    def decorator(func):
        def wrapper(*args):
            newFilePath = filePath.replace("*id*", args[0])
            with open(newFilePath, 'r') as f:
                jsonFile = json.load(f)
            f.close()

            jsonFile = func(*args, jsonFile)

            with open(newFilePath, 'w') as f:
                json.dump(jsonFile, f)
            f.close()
        return wrapper
    return decorator
