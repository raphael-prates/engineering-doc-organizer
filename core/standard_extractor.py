import re
import json
import os

def receive_input(input_data):
    if isinstance(input_data, str):
        return input_data
    elif isinstance(input_data, bytes):
        return input_data.decode('utf-8')
    
def extract_pattern(text):
    results = re.findall(r'[A-Z0-9]+(?:[-._][A-Z0-9]+)+(?:\.rev[A-Z0-9]+)?', text)
    if results:
        return results
    return None

def save_standard(pattern, name):
    data = {"name": name, "pattern": pattern}
    with open(f'config/standards/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def list_standards():
    folder = 'config/standards'
    files = os.listdir(folder)
    return [f.replace('.json','') for f in files if f.endswith('.json')]

def delete_standard(name):
    os.remove(f'config/standards/{name}.json')

def load_standard(name):
    with open(f'config/standards/{name}.json', 'r', encoding='utf-8') as f:
        return json.load(f)