import json
import time

class SharedMemory:
    def __init__(self):
        self.data = {
            "cliente_perfil": {
                "nombre": "Invitado",
                "presupuesto": None,
                "preferencias": []
            },
            "consulta_stock": {
                "producto_interes": None,
                "marca_preferida": None,
                "stock_confirmado": False,
                "garantia_informada": False,
                "entrega_coordinada": False
            },
            "sistema": {
                "agente_activo": "agente_ventas",
                "historial_resumen": "",
                "timestamp_inicio": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
        }

    def set_active_agent(self, agent_name: str):
        self.data["sistema"]["agente_activo"] = agent_name

    def get_active_agent(self) -> str:
        return self.data["sistema"]["agente_activo"]

    def registrar_presupuesto(self, presupuesto: float):
        self.data["cliente_perfil"]["presupuesto"] = presupuesto

    def registrar_preferencia(self, preferencia: str):
        if preferencia not in self.data["cliente_perfil"]["preferencias"]:
            self.data["cliente_perfil"]["preferencias"].append(preferencia)

    def registrar_producto_interes(self, producto: str):
        self.data["consulta_stock"]["producto_interes"] = producto

    def registrar_marca_preferida(self, marca: str):
        self.data["consulta_stock"]["marca_preferida"] = marca

    def confirmar_stock(self, confirmado: bool):
        self.data["consulta_stock"]["stock_confirmado"] = confirmado

    def informar_garantia(self, informado: bool):
        self.data["consulta_stock"]["garantia_informada"] = informado

    def coordinar_entrega(self, coordinada: bool):
        self.data["consulta_stock"]["entrega_coordinada"] = coordinada

    def to_dict(self) -> dict:
        return self.data

    def load_from_dict(self, source_dict: dict):
        if source_dict:
            self.data.update(source_dict)

    def to_json_str(self) -> str:
        return json.dumps(self.data, indent=2, ensure_ascii=False)
