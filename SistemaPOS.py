import csv
import datetime
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from GestionFactura import GestionFactura
from InformeAnalisis import InformesAnalisis



class SistemaPOS:
    CLIENTES_FILE = 'clientes.csv'
    PRODUCTOS_FILE = 'productos.csv'
    FACTURAS_FILE = 'facturas.csv'

    def __init__(self):
        self.inicializar_archivos()
        self.root = tk.Tk()
        self.root.title("Sistema de Punto de Venta")
        self.root.geometry("450x400")  # Tamaño de la ventana principal
        self.root.configure(bg='light blue')
        self.configurar_interfaz()
        self.gestion_factura = GestionFactura(self) 
        self.root.mainloop()
        self.inicializar_archivos() 
       
      
        

    def inicializar_archivos(self):
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


    def leer_csv(self, file_path):
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def escribir_csv(self, file_path, data, fieldnames):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def guardar_csv(self, file_path, data):
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def agregar_cliente(self, nombre, fecha_nacimiento, documento):
        try:
            
            # Validación de datos
           fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date() # Verificar que la fecha sea válida
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, introduce una fecha de nacimiento válida. Error: {e}")
            return

        clientes = self.leer_csv(self.CLIENTES_FILE)

        for cliente in clientes:
            if cliente['documento'] == documento:
                messagebox.showerror("Error", "Documento duplicado.")
                return

        id_cliente = 1
        if clientes:
            id_cliente = int(clientes[-1]['idCliente']) + 1

        nuevo_cliente = {
            'idCliente': id_cliente,
            'nombre': nombre,
            'fechaNacimiento': fecha_nacimiento.strftime('%Y-%m-%d'),  
            'documento': documento
        }

        clientes.append(nuevo_cliente)
        self.escribir_csv(self.CLIENTES_FILE, clientes, ['idCliente', 'nombre', 'fechaNacimiento', 'documento'])
        messagebox.showinfo("Información", "Cliente agregado exitosamente.")

    def actualizar_cliente(self, id_cliente, nuevo_nombre, nueva_fecha_nacimiento, nuevo_documento):
        try:
            # Validación de datos
            nueva_fecha_nacimiento = datetime.datetime.strptime(nueva_fecha_nacimiento, '%Y-%m-%d').date() # Convertir la cadena de fecha en un objeto datetime
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, introduce una fecha de nacimiento válida. Error: {e}")
            return

        clientes = self.leer_csv(self.CLIENTES_FILE)
        for cliente in clientes:
            if cliente['idCliente'] == id_cliente:
                cliente['nombre'] = nuevo_nombre
                cliente['fechaNacimiento'] = nueva_fecha_nacimiento.strftime('%Y-%m-%d') # Formatear la fecha como una cadena
                cliente['documento'] = nuevo_documento
                break
        self.escribir_csv(self.CLIENTES_FILE, clientes, ['idCliente', 'nombre', 'fechaNacimiento', 'documento'])
      


    def eliminar_cliente(self, id_cliente):
        clientes = self.leer_csv(self.CLIENTES_FILE)
        clientes_actualizados = [cliente for cliente in clientes if cliente['idCliente'] != id_cliente]
        self.escribir_csv(self.CLIENTES_FILE, clientes_actualizados, ['idCliente', 'nombre', 'fechaNacimiento', 'documento'])
        messagebox.showinfo("Información", f"Cliente con ID {id_cliente} eliminado exitosamente.")

    def configurar_interfaz(self):
        
        tk.Label(self.root, text="TIENDA LA QUINTA", font=("Georgia", 16)).pack(pady=10)
        tk.Button(self.root, bg='black', fg='white', text="Gestión de Clientes", command=self.abrir_gestion_clientes, width=20, height=2).pack(pady=10)
        tk.Button(self.root, bg='black', fg='white', text="Gestión de Productos", command=self.abrir_gestion_productos, width=20, height=2).pack(pady=10)
        tk.Button(self.root, bg='black', fg='white', text="Gestión de Facturas", command=self.abrir_gestion_crudFactura, width=20, height=2).pack(pady=10)
        tk.Button(self.root, bg='black', fg='white', text="Generar Informes", command=self.abrir_gestion_informes, width=20, height=2).pack(pady=10)
        tk.Label(self.root, text="Desarrollado por: Alejandro Lopez Ramirez \n 2359618 - Univalle ", font=("Courier", 11)).pack(pady=10)


        

    def abrir_gestion_clientes(self):
        from GestionClientes import GestionClientes
        GestionClientes(self)
    
    def abrir_gestion_productos(self):
        from GestionProductos import GestionProductos
        GestionProductos(self)
    
    def abrir_gestion_informes(self):
        self.InformeAnalisis = InformesAnalisis(self)
        

    


    def agregar_producto(self, nombre, cantidad, costo_compra, precio_venta, fecha_vencimiento):
        try:
            cantidad = int(cantidad)
            costo_compra = float(costo_compra)
            precio_venta = float(precio_venta)
            fecha_vencimiento = datetime.datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()  # Verificar y convertir la fecha
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, introduce valores válidos. Error: {e}")
            return

        if cantidad < 0:
            messagebox.showerror("Error", "La cantidad no puede ser negativa.")
            return

        productos = self.leer_csv(self.PRODUCTOS_FILE)

        id_producto = 1
        if productos:
            id_producto = int(productos[-1]['idProducto']) + 1

        nuevo_producto = {
            'idProducto': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'costoCompra': costo_compra,
            'precioVenta': precio_venta,
            'fechaVencimiento': fecha_vencimiento.strftime('%Y-%m-%d')
        }

        productos.append(nuevo_producto)
        self.escribir_csv(self.PRODUCTOS_FILE, productos, ['idProducto', 'nombre', 'cantidad', 'costoCompra', 'precioVenta', 'fechaVencimiento'])


    def ventana_eliminar_producto(self):
        seleccion = self.tree.selection()
        if seleccion:
            confirmar_eliminacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar el producto seleccionado?")
            if confirmar_eliminacion:
                id_producto = self.tree.item(seleccion[0])['text']  # Obtener el ID del producto seleccionado
                self.eliminar_producto(id_producto)
                messagebox.showinfo("Información", "Producto eliminado exitosamente.")
                self.actualizar_lista_productos()
        else:
            messagebox.showerror("Error", "Por favor, selecciona un producto para eliminar.")

    def actualizar_producto(self, id_producto, nuevo_nombre, nueva_cantidad, nuevo_costo_compra, nuevo_precio_venta, nueva_fecha_vencimiento):
        try:
            nueva_cantidad = int(nueva_cantidad)
            nuevo_costo_compra = float(nuevo_costo_compra)
            nuevo_precio_venta = float(nuevo_precio_venta)
            nueva_fecha_vencimiento = datetime.datetime.strptime(nueva_fecha_vencimiento, '%Y-%m-%d').date()  # Verificar y convertir la fecha
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, introduce valores válidos. Error: {e}")
            return

        productos = self.leer_csv(self.PRODUCTOS_FILE)
        for producto in productos:
            if producto['idProducto'] == id_producto:
                producto['nombre'] = nuevo_nombre
                producto['cantidad'] = nueva_cantidad
                producto['costoCompra'] = nuevo_costo_compra
                producto['precioVenta'] = nuevo_precio_venta
                producto['fechaVencimiento'] = nueva_fecha_vencimiento.strftime('%Y-%m-%d')
                break
        self.escribir_csv(self.PRODUCTOS_FILE, productos, ['idProducto', 'nombre', 'cantidad', 'costoCompra', 'precioVenta', 'fechaVencimiento'])
    
    
    def eliminar_producto(self, id_producto):
        productos = self.leer_csv(SistemaPOS.PRODUCTOS_FILE)
        productos_actualizados = [producto for producto in productos if producto['idProducto'] != id_producto]
        self.escribir_csv(SistemaPOS.PRODUCTOS_FILE, productos_actualizados, ['idProducto', 'nombre', 'cantidad', 'costoCompra', 'precioVenta', 'fechaVencimiento'])



    def agregar_factura(self, id_factura, id_cliente, fecha_factura, total_factura, nombre_producto, cantidad_vendida, precio_unitario):
        try:
            # Validar los datos
            fecha_factura = datetime.datetime.strptime(fecha_factura, '%Y-%m-%d').date()
            total_factura = float(total_factura)
            cantidad_vendida = int(cantidad_vendida)
            precio_unitario = float(precio_unitario)
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, introduce datos válidos. Error: {e}")
            return

        # Leer las facturas existentes
        facturas = self.leer_csv(self.FACTURAS_FILE)

        # Obtener el siguiente ID de factura
        if facturas:
            id_factura = int(facturas[-1]['idFactura']) + 1

        # Crear la nueva factura
        nueva_factura = {
            'idFactura': id_factura,
            'idCliente': id_cliente,
            'fechaFactura': fecha_factura.strftime('%Y-%m-%d'),
            'totalFactura': total_factura,
            'nombreProducto': nombre_producto,
            'cantidadVendida': cantidad_vendida,
            'precioUnitario': precio_unitario
        }

        # Agregar la factura al archivo CSV
        facturas.append(nueva_factura)
        self.guardar_csv(self.FACTURAS_FILE, facturas)
        

    def actualizar_factura(self, id_factura, nueva_fecha_factura, nuevo_total_factura):
        try:
            # Validar los datos
            nueva_fecha_factura = datetime.datetime.strptime(nueva_fecha_factura, '%Y-%m-%d').date()
            nuevo_total_factura = float(nuevo_total_factura)
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, introduce datos válidos. Error: {e}")
            return

        # Leer las facturas existentes
        facturas = self.leer_csv(self.FACTURAS_FILE)

        # Actualizar la factura
        for factura in facturas:
            if factura['idFactura'] == id_factura:
                factura['fechaFactura'] = nueva_fecha_factura.strftime('%Y-%m-%d')
                factura['totalFactura'] = nuevo_total_factura
                break

        # Guardar los cambios
        self.guardar_csv(self.FACTURAS_FILE, facturas)
       

    def eliminar_factura(self, id_factura):
        # Leer las facturas existentes
        facturas = self.leer_csv(self.FACTURAS_FILE)

        # Eliminar la factura
        facturas_actualizadas = [factura for factura in facturas if factura['idFactura'] != id_factura]
        self.escribir_csv(SistemaPOS.FACTURAS_FILE, facturas_actualizadas, ['idFactura', 'idCliente', 'fechaFactura', 'totalFactura', 'nombreProducto', 'cantidadVendida', 'precioUnitario'])
        
        

    def abrir_gestion_crudFactura(self):
        from CrudFacturas import CrudFacturas
        CrudFacturas(self)

    

    
    
    def ventana_visualizar_csv(self, file_path):
        def cerrar_ventana():
            ventana.destroy()

        ventana = tk.Toplevel()
        ventana.title("Visualizar CSV")
        ventana.geometry("600x400")  # Tamaño de la ventana para visualizar el CSV

        # Crear Treeview
        tree = ttk.Treeview(ventana)
        tree.pack(expand=True, fill="both")

        # Leer el contenido del archivo CSV y cargarlo en una lista
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            csv_content = list(reader)

        # Configurar columnas y agregar filas
        if csv_content:
            columns = csv_content[0]
            tree["columns"] = columns
            tree.heading("#0", text="ID")  # Columna oculta para IDs
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

        # Agregar filas
        for i, row in enumerate(csv_content[1:], start=1):  # Empezar desde la segunda fila
            tree.insert("", "end", text=i, values=row)

        # Botón para cerrar la ventana
        tk.Button(ventana, text="Cerrar", command=cerrar_ventana).pack(pady=10)
        
        


      
if __name__ == "__main__":
    SistemaPOS()
    


