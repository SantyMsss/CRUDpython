    if not os.path.exists(self.CLIENTES_FILE):
            with open(self.CLIENTES_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['idCliente', 'nombre', 'fechaNacimiento', 'documento'])

        if not os.path.exists(self.PRODUCTOS_FILE):
            with open(self.PRODUCTOS_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['idProducto', 'nombre', 'cantidad', 'costoCompra', 'precioVenta', 'fechaVencimiento'])

        if not os.path.exists(self.FACTURAS_FILE):
            with open(self.FACTURAS_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['idFactura', 'idCliente', 'fechaFactura', 'totalFactura', 'nombreProducto', 'cantidadVendida', 'precioUnitario'])