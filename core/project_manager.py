import json
import os

def save_project(name, year, path):
    project = {"name": name, "year": year, "path": path}
    with open(f'config/projects/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(project, f, indent=2)
        
def list_projects():
    folder = 'config/projects'
    files = os.listdir(folder)
    return [f.replace('.json','') for f in files if f.endswith('.json')]

def delete_project(name):
    os.remove(f'config/projects/{name}.json')

def load_project(name):
    with open(f'config/projects/{name}.json', 'r', encoding='utf-8') as f:
        return json.load(f)