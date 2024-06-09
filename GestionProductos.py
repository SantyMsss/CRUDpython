import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import csv
import SistemaPOS
from GestionFactura import GestionFactura  # Importa la clase GestionFactura

class GestionProductos:
    PRODUCTOS_FILE = 'productos.csv'

    def __init__(self, sistema_pos):
        self.sistema_pos = sistema_pos
        self.root = tk.Toplevel()
        self.root.title("Gestión de Productos")
        self.root.geometry("1200x600")  # Tamaño de la ventana de gestión de productos
        self.configurar_interfaz()
        self.actualizar_lista_productos()
        self.gestion_factura = GestionFactura(sistema_pos)  # Inicializa gestion_factura aquí
        self.root.mainloop()
        
        
    def actualizar_lista_productos(self):
        # Limpiar el Treeview antes de actualizar
        self.tree.delete(*self.tree.get_children())
        # Recargar la lista de productos
        productos = self.sistema_pos.leer_csv(self.PRODUCTOS_FILE)
        for producto in productos:
            self.tree.insert("", "end", text=producto['idProducto'], values=(producto['nombre'], producto['cantidad'], producto['costoCompra'], producto['precioVenta'], producto['fechaVencimiento']))

    def ventana_agregar_producto(self):
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Producto")

        tk.Label(ventana_agregar, text="Nombre").grid(row=0, column=0)
        entry_nombre = tk.Entry(ventana_agregar)
        entry_nombre.grid(row=0, column=1)

        tk.Label(ventana_agregar, text="Cantidad").grid(row=1, column=0)
        entry_cantidad = tk.Entry(ventana_agregar)
        entry_cantidad.grid(row=1, column=1)

        tk.Label(ventana_agregar, text="Costo de Compra").grid(row=2, column=0)
        entry_costo_compra = tk.Entry(ventana_agregar)
        entry_costo_compra.grid(row=2, column=1)

        tk.Label(ventana_agregar, text="Precio de Venta").grid(row=3, column=0)
        entry_precio_venta = tk.Entry(ventana_agregar)
        entry_precio_venta.grid(row=3, column=1)

        tk.Label(ventana_agregar, text="Fecha de Vencimiento").grid(row=4, column=0)
        cal_fecha_vencimiento = DateEntry(ventana_agregar, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        cal_fecha_vencimiento.grid(row=4, column=1)

        btn_guardar = tk.Button(ventana_agregar, text="Guardar", command=lambda: self.guardar_producto(entry_nombre.get(), entry_cantidad.get(), entry_costo_compra.get(), entry_precio_venta.get(), cal_fecha_vencimiento.get(), ventana_agregar))
        btn_guardar.grid(row=5, columnspan=2)

    def guardar_producto(self, nombre, cantidad, costo_compra, precio_venta, fecha_vencimiento, ventana):
        try:
            cantidad = int(cantidad)
            costo_compra = float(costo_compra)
            precio_venta = float(precio_venta)
            datetime.strptime(fecha_vencimiento, '%Y-%m-%d')  # Verificar que la fecha sea válida

            # Guardar el producto utilizando el método del sistema POS
            self.sistema_pos.agregar_producto(nombre, cantidad, costo_compra, precio_venta, fecha_vencimiento)
            messagebox.showinfo("Información", "Producto agregado exitosamente.")
            ventana.destroy()
            self.actualizar_lista_productos()

        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, introduce valores válidos. Error: {e}")

    def ventana_actualizar_producto(self):
        seleccion = self.tree.selection()
        if seleccion:
            id_producto = self.tree.item(seleccion[0])['text']
            productos = self.sistema_pos.leer_csv(self.PRODUCTOS_FILE)
            datos_producto = next((producto for producto in productos if producto['idProducto'] == id_producto), None)
            if datos_producto:
                ventana_actualizar = tk.Toplevel(self.root)
                ventana_actualizar.title("Actualizar Producto")

                tk.Label(ventana_actualizar, text="Nombre").grid(row=0, column=0)
                entry_nombre = tk.Entry(ventana_actualizar)
                entry_nombre.insert(0, datos_producto['nombre'])
                entry_nombre.grid(row=0, column=1)

                tk.Label(ventana_actualizar, text="Cantidad").grid(row=1, column=0)
                entry_cantidad = tk.Entry(ventana_actualizar)
                entry_cantidad.insert(0, datos_producto['cantidad'])
                entry_cantidad.grid(row=1, column=1)

                tk.Label(ventana_actualizar, text="Costo de Compra").grid(row=2, column=0)
                entry_costo_compra = tk.Entry(ventana_actualizar)
                entry_costo_compra.insert(0, datos_producto['costoCompra'])
                entry_costo_compra.grid(row=2, column=1)

                tk.Label(ventana_actualizar, text="Precio de Venta").grid(row=3, column=0)
                entry_precio_venta = tk.Entry(ventana_actualizar)
                entry_precio_venta.insert(0, datos_producto['precioVenta'])
                entry_precio_venta.grid(row=3, column=1)

                tk.Label(ventana_actualizar, text="Fecha de Vencimiento").grid(row=4, column=0)
                cal_fecha_vencimiento = DateEntry(ventana_actualizar, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
                cal_fecha_vencimiento.set_date(datetime.strptime(datos_producto['fechaVencimiento'], '%Y-%m-%d'))
                cal_fecha_vencimiento.grid(row=4, column=1)

                btn_guardar_actualizacion = tk.Button(ventana_actualizar, text="Guardar", command=lambda: self.guardar_actualizacion_producto(id_producto, entry_nombre.get(), entry_cantidad.get(), entry_costo_compra.get(), entry_precio_venta.get(), cal_fecha_vencimiento.get(), ventana_actualizar))
                btn_guardar_actualizacion.grid(row=5, columnspan=2)
            else:
                messagebox.showerror("Error", "No se encontraron datos del producto.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un producto para actualizar.")

    def guardar_actualizacion_producto(self, id_producto, nuevo_nombre, nueva_cantidad, nuevo_costo_compra, nuevo_precio_venta, nueva_fecha_vencimiento, ventana):
        self.sistema_pos.actualizar_producto(id_producto, nuevo_nombre, nueva_cantidad, nuevo_costo_compra, nuevo_precio_venta, nueva_fecha_vencimiento)
        messagebox.showinfo("Información", "Producto actualizado exitosamente.")
        ventana.destroy()
        self.actualizar_lista_productos()

    def ventana_eliminar_producto(self):
        seleccion = self.tree.selection()
        if seleccion:
            confirmar_eliminacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar el producto seleccionado?")
            if confirmar_eliminacion:
                id_producto = self.tree.item(seleccion[0])['text']  # Obtener el ID del producto seleccionado
                self.sistema_pos.eliminar_producto(id_producto)
                messagebox.showinfo("Información", "Producto eliminado exitosamente.")
                self.actualizar_lista_productos()
        else:
            messagebox.showerror("Error", "Por favor, selecciona un producto para eliminar.")

    def ventana_vender_producto(self):
        seleccion = self.tree.selection()
        if seleccion:
            id_producto = self.tree.item(seleccion[0])['text']
            productos = self.sistema_pos.leer_csv(self.PRODUCTOS_FILE)
            datos_producto = next((producto for producto in productos if producto['idProducto'] == id_producto), None)
            if datos_producto:
                ventana_vender = tk.Toplevel(self.root)
                ventana_vender.title("Vender Producto")

                tk.Label(ventana_vender, text="Nombre").grid(row=0, column=0)
                tk.Label(ventana_vender, text=datos_producto['nombre']).grid(row=0, column=1)

                tk.Label(ventana_vender, text="Cantidad a vender").grid(row=1, column=0)
                entry_cantidad_vender = tk.Entry(ventana_vender)
                entry_cantidad_vender.grid(row=1, column=1)

                btn_vender = tk.Button(ventana_vender, text="Vender", command=lambda: self.vender_producto(id_producto, entry_cantidad_vender.get(), ventana_vender))
                btn_vender.grid(row=2, columnspan=2)
            else:
                messagebox.showerror("Error", "No se encontraron datos del producto.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un producto para vender.")
            

    def vender_producto(self, id_producto, cantidad_vender, ventana):
        try:
            cliente_id = 1  # Aquí necesitas obtener el ID del cliente de alguna manera

            # Convertir la cantidad a vender a un entero
            cantidad_vender = int(cantidad_vender)

            # Leer la lista de productos del archivo CSV
            productos = self.sistema_pos.leer_csv(self.PRODUCTOS_FILE)

            # Encontrar el producto correspondiente en la lista de productos
            producto = next((p for p in productos if p['idProducto'] == id_producto), None)

            # Verificar si el producto existe y hay suficiente cantidad para vender
            if producto and int(producto['cantidad']) >= cantidad_vender:
                # Restar la cantidad vendida del producto
                producto['cantidad'] = str(int(producto['cantidad']) - cantidad_vender)

                # Guardar la lista de productos actualizada en el archivo CSV
                self.sistema_pos.guardar_csv(self.PRODUCTOS_FILE, productos)

                # Mostrar mensaje de éxito
                messagebox.showinfo("Información", "Compra exitosa.")

                # Generar la factura con los detalles del producto vendido
                self.gestion_factura.generar_factura(cliente_id, id_producto, cantidad_vender, producto)

                # Cerrar la ventana de venta
                ventana.destroy()
                self.actualizar_lista_productos()

            else:
                # Mostrar mensaje de error si no hay suficiente cantidad para vender
                messagebox.showerror("Error", "No hay suficiente cantidad disponible para vender.")
        except ValueError:
            # Mostrar mensaje de error si la cantidad a vender no es un número entero
            messagebox.showerror("Error", "Por favor, introduce una cantidad válida.")



            

    def configurar_interfaz(self):
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(side=tk.TOP, fill=tk.X)

        btn_agregar = tk.Button(frame_botones, text="Agregar Producto", command=self.ventana_agregar_producto)
        btn_agregar.pack(side=tk.LEFT)

        btn_actualizar = tk.Button(frame_botones, text="Actualizar Producto", command=self.ventana_actualizar_producto)
        btn_actualizar.pack(side=tk.LEFT)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar Producto", command=self.ventana_eliminar_producto)
        btn_eliminar.pack(side=tk.LEFT)

        btn_vender = tk.Button(frame_botones, text="Vender Producto", command=self.ventana_vender_producto)
        btn_vender.pack(side=tk.LEFT)

        frame_lista = tk.Frame(self.root)
        frame_lista.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame_lista, columns=("Nombre", "Cantidad", "Costo de Compra", "Precio de Venta", "Fecha de Vencimiento"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Costo de Compra", text="Costo de Compra")
        self.tree.heading("Precio de Venta", text="Precio de Venta")
        self.tree.heading("Fecha de Vencimiento", text="Fecha de Vencimiento")
        self.tree.column("#0", stretch=tk.YES)
        self.tree.column("Nombre", stretch=tk.YES)
        self.tree.column("Cantidad", stretch=tk.YES)
        self.tree.column("Costo de Compra", stretch=tk.YES)
        self.tree.column("Precio de Venta", stretch=tk.YES)
        self.tree.column("Fecha de Vencimiento", stretch=tk.YES)
        self.tree.pack(fill=tk.BOTH, expand=True)
