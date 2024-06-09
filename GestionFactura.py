import csv
import datetime

class GestionFactura:
    FACTURAS_FILE = 'facturas.csv'

    def __init__(self, sistema_pos):
        self.sistema_pos = sistema_pos

    def generar_factura(self, id_cliente, id_producto, cantidad_vender, producto):
        producto_info = self.obtener_producto_info(id_producto)
        if producto_info:
            total_factura = float(producto_info['precioVenta']) * int(cantidad_vender)
            fecha_factura = datetime.datetime.now().strftime('%Y-%m-%d')
            factura_data = [self.obtener_id_factura(), id_cliente, fecha_factura, total_factura, producto_info['nombre']]
            self.agregar_factura(factura_data)

    def obtener_producto_info(self, id_producto):
        productos = self.sistema_pos.leer_csv(self.sistema_pos.PRODUCTOS_FILE)
        for producto in productos:
            if producto['idProducto'] == id_producto:
                return producto
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
