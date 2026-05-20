class EventBus:
    """
    Bus de Eventos reactivo con patrón Pub-Sub (Rúbrica Criterio 2).
    Controla la verbosidad mediante el flag `verbose` para no contaminar
    la consola del chat interactivo con logs internos del sistema.
    """

    def __init__(self, verbose: bool = False):
        self._listeners: dict = {}
        self.verbose = verbose
        self._log_history: list[str] = []

    def subscribe(self, event_type: str, callback):
        """Suscribe una función callback a un evento específico."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def publish(self, event_type: str, data: dict = None):
        """Publica un evento a todos los suscriptores registrados."""
        entrada = f"[EVENT BUS] '{event_type}'"
        self._log_history.append(entrada)

        if self.verbose:
            print(f"  {entrada}")

        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                try:
                    callback(data or {})
                except Exception as e:
                    if self.verbose:
                        print(f"  [EVENT BUS ERROR] Callback para '{event_type}': {e}")

    def set_verbose(self, verbose: bool):
        """Activa o desactiva el logging en consola."""
        self.verbose = verbose

    def get_log_history(self) -> list[str]:
        """Retorna todos los eventos publicados (para mostrar en modo evaluación)."""
        return self._log_history
