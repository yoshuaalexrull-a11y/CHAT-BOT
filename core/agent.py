import yaml

class Agent:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

def load_agents_config(filepath):
    """Carga la configuracion de agentes desde un archivo YAML."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file).get('agents', [])
