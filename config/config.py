import json

def load_config(file_path='config.json'):
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config