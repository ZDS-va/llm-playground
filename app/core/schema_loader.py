import json
import os
from jsonschema import validate, ValidationError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_schema(name: str):
    schema_path = os.path.join(BASE_DIR, "schemas", f"{name}.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return schema


def validate_json_with_schema(data: dict, schema: dict):
    try:
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)
