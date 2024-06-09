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
        self.agregar_factura(id_factura, id_cliente, fecha_factura, total_venta, detalles_productos)

        # Devolver los detalles de la factura
        return id_factura, cliente_info, detalles_productos, total_venta

    def obtener_cliente_info(self, documento_cliente):
        clientes = self.sistema_pos.leer_csv(self.CLIENTES_FILE)
        for cliente in clientes:
            if cliente['documento'] == documento_cliente:
                return cliente
        return None

    def agregar_factura(self, id_factura, id_cliente, fecha_factura, total_factura, detalles_factura):
        nombre_archivo = "facturas.csv"
        
        # Abrir el archivo en modo de adición (append) y crear un objeto escritor CSV
        with open(nombre_archivo, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Escribir cada detalle de la factura en una fila separada
            for detalle in detalles_factura:
                nombre_producto = detalle['Producto']
                cantidad_vendida = detalle['Cantidad']
                precio_unitario = detalle['Precio Unitario']
                writer.writerow([id_factura, id_cliente, fecha_factura, total_factura, nombre_producto, cantidad_vendida, precio_unitario])

        print("Los detalles de la factura se han guardado en el archivo:", nombre_archivo)

    def obtener_id_factura(self):
        facturas = self.sistema_pos.leer_csv(self.FACTURAS_FILE)
        if facturas:
            return int(facturas[-1]['idFactura']) + 1
        else:
            return 1
