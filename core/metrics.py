import time

class MetricsTracker:
    def __init__(self):
        self.global_tokens = 0
        self.total_llamadas = 0
        self.latencias = []
        self.resultados_pruebas = []
        self.start_time = time.time()

    def registrar_llamada(self, tokens, latencia):
        self.total_llamadas += 1
        if tokens is not None:
            self.global_tokens += tokens
        self.latencias.append(latencia)

    def registrar_resultado(self, caso, exito, agente, **kwargs):
        resultado = {
            "caso": caso,
            "exito": exito,
            "agente": agente
        }
        resultado.update(kwargs)
        self.resultados_pruebas.append(resultado)

    def imprimir_reporte(self, modelo):
        """Imprime el reporte de metricas del sistema."""
        end_time = time.time()
        tiempo_total = end_time - self.start_time
        latencia_promedio = sum(self.latencias) / len(self.latencias) if self.latencias else 0

        print("\n" + "=" * 65)
        print("            REPORTE DE METRICAS DEL SISTEMA")
        print("=" * 65)
        print(f"  Tiempo total de ejecucion    : {tiempo_total:.2f} segundos")
        print(f"  Tokens totales consumidos    : {self.global_tokens} tokens")
        print(f"  Llamadas totales al modelo   : {self.total_llamadas}")
        print(f"  Latencia promedio por llamada: {latencia_promedio:.2f} segundos")
        if self.latencias:
            print(f"  Latencia minima              : {min(self.latencias):.2f}s")
            print(f"  Latencia maxima              : {max(self.latencias):.2f}s")
        if self.resultados_pruebas:
            tasa_exito = sum(1 for r in self.resultados_pruebas if r["exito"]) / len(self.resultados_pruebas) * 100
            print(f"  Tasa de exito                : {tasa_exito:.0f}% ({sum(1 for r in self.resultados_pruebas if r['exito'])}/{len(self.resultados_pruebas)} pruebas)")
        print(f"  Topologia de Arquitectura    : Delegacion Jerarquica (Swarm)")
        print(f"  Protocolo de Estado          : MCP (Model Context Protocol) via JSON")
        print(f"  Modelo utilizado             : {modelo}")
        if self.resultados_pruebas:
            print("-" * 65)
            print("  RESULTADOS POR CASO DE PRUEBA:")
            print("-" * 65)
            for r in self.resultados_pruebas:
                estado = "PASS" if r["exito"] else "FAIL"
                print(f"    [{estado}] {r['caso']} (agente: {r['agente']})")
        print("=" * 65)
