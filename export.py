import json

def export_to_json(data, filename="exported.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)