import csv
from datetime import datetime
from tkinter import messagebox

class GestionFactura:
    FACTURAS_FILE = 'facturas.csv'

    def __init__(self, sistema_pos, id_cliente, productos_vendidos):
        self.sistema_pos = sistema_pos
        self.id_cliente = id_cliente
        self.productos_vendidos = productos_vendidos
        self.generar_factura()

    def generar_factura(self):
        # Obtener información del cliente
        cliente = self.obtener_info_cliente(self.id_cliente)

        # Calcular el total de la factura
        total_factura = self.calcular_total_factura()

        # Obtener el ID de la última factura
        id_factura = self.obtener_ultimo_id_factura() + 1

        # Obtener la fecha actual
        fecha_factura = datetime.now().strftime('%Y-%m-%d')

        # Crear entrada de factura
        nueva_factura = {
            'idFactura': id_factura,
            'idCliente': self.id_cliente,
            'fechaFactura': fecha_factura,
            'totalFactura': total_factura,
            'productos': self.productos_vendidos
        }

        # Agregar factura al archivo
        facturas = self.sistema_pos.leer_csv(self.FACTURAS_FILE)
        facturas.append(nueva_factura)
        self.sistema_pos.escribir_csv(self.FACTURAS_FILE, facturas, ['idFactura', 'idCliente', 'fechaFactura', 'totalFactura', 'productos'])

        # Generar factura en formato CSV
        self.generar_factura_csv(id_factura, cliente, total_factura)

        messagebox.showinfo("Información", f"Factura generada exitosamente. ID de factura: {id_factura}")

    def obtener_info_cliente(self, id_cliente):
        clientes = self.sistema_pos.leer_csv(self.sistema_pos.CLIENTES_FILE)
        return next((c for c in clientes if c['idCliente'] == id_cliente), None)

    def calcular_total_factura(self):
        total = 0
        productos = self.sistema_pos.leer_csv(self.sistema_pos.PRODUCTOS_FILE)
        for id_producto, cantidad in self.productos_vendidos.items():
            producto = next((p for p in productos if p['idProducto'] == id_producto), None)
            if producto:
                total += float(producto['precioVenta']) * cantidad
        return total

    def obtener_ultimo_id_factura(self):
        facturas = self.sistema_pos.leer_csv(self.FACTURAS_FILE)
        return int(facturas[-1]['idFactura']) if facturas else 0

    def generar_factura_csv(self, id_factura, cliente, total_factura):
        nombre_archivo = f"factura_{id_factura}.csv"
        with open(nombre_archivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Empresa Ficticia"])
            writer.writerow(["Fecha de facturación:", datetime.now().strftime('%Y-%m-%d')])
            writer.writerow(["Número de factura:", f"F-{id_factura}"])
            writer.writerow(["Información del cliente:"])
            writer.writerow(["ID Cliente:", cliente['idCliente']])
            writer.writerow(["Nombre:", cliente['nombre']])
            writer.writerow(["Fecha de nacimiento:", cliente['fechaNacimiento']])
            writer.writerow(["Documento:", cliente['documento']])
            writer.writerow([])
            writer.writerow(["Detalles de productos comprados:"])
            writer.writerow(["ID Producto", "Nombre", "Cantidad", "Precio Unitario", "Precio Total"])
            productos = self.sistema_pos.leer_csv(self.sistema_pos.PRODUCTOS_FILE)
            for id_producto, cantidad in self.productos_vendidos.items():
                producto = next((p for p in productos if p['idProducto'] == id_producto), None)
                if producto:
                    precio_unitario = producto['precioVenta']
                    precio_total = float(precio_unitario) * cantidad
                    writer.writerow([id_producto, producto['nombre'], cantidad, precio_unitario, precio_total])
            writer.writerow([])
            writer.writerow(["Total de la factura:", total_factura])
