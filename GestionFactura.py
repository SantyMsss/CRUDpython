import csv
import datetime

class GestionFactura:
    FACTURAS_FILE = 'facturas.csv'
    CLIENTES_FILE = 'clientes.csv'
    PRODUCTOS_FILE = 'productos.csv'

    def __init__(self, sistema_pos):
        self.sistema_pos = sistema_pos

    def generar_factura(self, id_cliente, detalles_productos, total_venta):
        # Obtener información del cliente
        cliente_info = self.obtener_cliente_info(id_cliente)
        if not cliente_info:
            print("Error: Cliente no encontrado.")
            return

        # Generar factura en formato CSV
        id_factura = self.obtener_id_factura()
        fecha_factura = datetime.datetime.now().strftime('%Y-%m-%d')

        # Agregar factura al archivo CSV
        self.agregar_factura([id_factura, cliente_info['nombre'], cliente_info['documento'], fecha_factura, total_venta])

        # Devolver los detalles de la factura
        return id_factura, cliente_info, detalles_productos, total_venta

    def obtener_cliente_info(self, documento_cliente):
        clientes = self.sistema_pos.leer_csv(self.CLIENTES_FILE)
        for cliente in clientes:
            if cliente['documento'] == documento_cliente:
                return cliente
        return None

    def agregar_factura(self, factura_data):
        with open(self.FACTURAS_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(factura_data)

    def obtener_id_factura(self):
        facturas = self.sistema_pos.leer_csv(self.FACTURAS_FILE)
        if facturas:
            return int(facturas[-1]['idFactura']) + 1
        else:
            return 1
