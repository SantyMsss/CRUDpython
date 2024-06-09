import csv
import datetime

class GestionFactura:
    FACTURAS_FILE = 'facturas.csv'

    def __init__(self, sistema_pos):
        self.sistema_pos = sistema_pos

    def generar_factura(self, id_cliente, id_producto, cantidad_vender, producto):
        producto_info = self.obtener_producto_info(id_producto)
        if producto_info:
            cantidad_vendida = int(cantidad_vender)
            precio_unitario = float(producto_info['precioVenta'])
            total_factura = precio_unitario * cantidad_vendida
            fecha_factura = datetime.datetime.now().strftime('%Y-%m-%d')
            # Incluir nombre del producto, cantidad vendida y precio unitario en la factura
            factura_data = [
                self.obtener_id_factura(),
                id_cliente,
                fecha_factura,
                total_factura,
                producto_info['nombre'],
                cantidad_vendida,
                precio_unitario
            ]
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
