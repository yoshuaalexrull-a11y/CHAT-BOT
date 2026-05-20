class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type: str, callback):
        """Suscribe una función callback a un evento específico."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def publish(self, event_type: str, data=None):
        """Publica un evento a todos los suscriptores y muestra la alerta en consola."""
        print(f"  [EVENT BUS] Evento emitido: '{event_type}'")
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"  [EVENT BUS ERROR] Error ejecutando callback para '{event_type}': {e}")
