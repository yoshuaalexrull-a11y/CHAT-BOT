class AgentNode:
    def __init__(self, agent):
        self.agent = agent
        self.connections = {}  # target_agent_name -> condition_desc

class AgentGraph:
    def __init__(self):
        self.nodes = {}

    def add_agent(self, agent):
        """Agrega un nodo de agente al grafo."""
        self.nodes[agent.name] = AgentNode(agent)

    def add_transition(self, from_agent_name: str, to_agent_name: str, condition_desc: str = ""):
        """Agrega una arista o transición permitida entre dos agentes."""
        if from_agent_name in self.nodes and to_agent_name in self.nodes:
            self.nodes[from_agent_name].connections[to_agent_name] = condition_desc
        else:
            raise KeyError(f"Agente {from_agent_name} o {to_agent_name} no existe en el grafo.")

    def get_agent(self, agent_name: str):
        """Obtiene la instancia del agente."""
        if agent_name in self.nodes:
            return self.nodes[agent_name].agent
        return None

    def get_transitions(self, agent_name: str) -> dict:
        """Obtiene las transiciones de salida permitidas para un agente."""
        if agent_name in self.nodes:
            return self.nodes[agent_name].connections
        return {}

    def print_topology(self):
        """Imprime la topología del grafo en consola."""
        print("\n" + "=" * 65)
        print("          TOPOLOGÍA DE RED MULTIAGENTE (AGENT GRAPH)")
        print("=" * 65)
        for name, node in self.nodes.items():
            print(f"  Nodo Agent: [{name}]")
            for target, cond in node.connections.items():
                print(f"    --> Delegación a: [{target}] | Condición: \"{cond}\"")
        print("=" * 65 + "\n")
