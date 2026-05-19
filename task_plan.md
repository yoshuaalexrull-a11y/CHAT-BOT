# Plan de Tareas: Proceso TO-BE de Gestión de Pedidos Veltri Tecnologic

1. **Recepción del Pedido:**
   - El cliente contacta a la empresa solicitando una tarjeta gráfica RTX 4060.
   - El **Agente de Ventas** (Especialista en Ventas y Atención) recibe la solicitud.

2. **Solicitud de Pago:**
   - El **Agente de Ventas** solicita al cliente que realice el pago mediante la aplicación Yape y envíe la captura de pantalla como comprobante de la transacción.

3. **Recepción de Comprobante y Transferencia:**
   - El cliente proporciona la captura de pantalla de Yape.
   - El **Agente de Ventas** confirma la recepción, recopila los datos necesarios y transfiere el flujo de atención, junto con la información del pedido, al **Agente de Inventario**.

4. **Validación de Stock y Aprobación de Pago:**
   - El **Agente de Inventario** (Gestor de Inventario Automatizado) toma el control de la operación.
   - Simula la validación de disponibilidad de stock para la tarjeta gráfica RTX 4060 en los almacenes.
   - Aprueba el pago internamente basándose en la validación de la transferencia realizada en el paso anterior.

5. **Emisión de Documentos y Alertas (Cierre del Proceso):**
   - El **Agente de Inventario** emite la boleta de venta electrónica (simulada) correspondiente a la compra del cliente.
   - Genera y emite una alerta de *picking* (preparación de pedido) dirigida al personal de almacén para iniciar el proceso de despacho físico del producto.
