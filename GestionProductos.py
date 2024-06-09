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
    CLIENTES_FILE = 'clientes.csv'
    FACTURAS_FILE = 'facturas.csv'

    def __init__(self, sistema_pos):
        self.sistema_pos = sistema_pos
        self.root = tk.Toplevel()
        self.root.title("Gestión de Productos")
        self.root.geometry("1200x600")  # Tamaño de la ventana de gestión de productos
        self.configurar_interfaz()
        self.actualizar_lista_productos()
        self.gestion_factura = GestionFactura(sistema_pos)  # Inicializa gestion_factura aquí
        self.detalles_temporales = {}  # Cambiar [] por {} para inicializar como un diccionario
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

                tk.Label(ventana_vender, text="ID del Cliente").grid(row=2, column=0)
                entry_id_cliente = tk.Entry(ventana_vender)
                entry_id_cliente.grid(row=2, column=1)

                btn_vender = tk.Button(ventana_vender, text="Vender", command=lambda: self.vender_producto(id_producto, entry_cantidad_vender.get(), entry_id_cliente.get(), ventana_vender))
                btn_vender.grid(row=3, columnspan=2)

            else:
                messagebox.showerror("Error", "No se encontraron datos del producto.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un producto para vender.")
            
            
            
    def vender_producto(self, ids_productos, cantidades_vender, documento_cliente, ventana):
        try:
            cliente_id = documento_cliente  # El documento del cliente se usa como identificador

            # Convertir las cantidades a vender a enteros
            cantidades_vender = [int(cantidad) for cantidad in cantidades_vender]

            # Inicializar la lista de detalles de factura
            detalles_factura = []

            # Leer la lista de productos del archivo CSV
            productos = self.sistema_pos.leer_csv(self.PRODUCTOS_FILE)

            # Iterar sobre los productos seleccionados
            for id_producto, cantidad_vender in zip(ids_productos, cantidades_vender):
                # Convertir id_producto a cadena
                id_producto = str(id_producto)

                # Encontrar el producto correspondiente en la lista de productos
                producto = next((p for p in productos if p['idProducto'] == id_producto), None)

                # Verificar si el producto existe y hay suficiente cantidad para vender
                if producto and int(producto['cantidad']) >= cantidad_vender:
                    # Calcular el subtotal para este producto
                    subtotal_producto = cantidad_vender * float(producto['precioVenta'])

                    # Agregar los detalles de la venta a la lista de detalles de factura
                    if id_producto in self.detalles_temporales:
                        # Si el producto ya está en los detalles temporales, actualizar la cantidad y el subtotal
                        self.detalles_temporales[id_producto]['Cantidad'] += cantidad_vender
                        self.detalles_temporales[id_producto]['Subtotal'] += subtotal_producto
                    else:
                        # Si el producto no está en los detalles temporales, agregarlo
                        self.detalles_temporales[id_producto] = {
                            'Producto': producto['nombre'],
                            'Cantidad': cantidad_vender,
                            'Precio Unitario': producto['precioVenta'],
                            'Subtotal': subtotal_producto
                        }

                    # Restar la cantidad vendida del producto
                    producto['cantidad'] = str(int(producto['cantidad']) - cantidad_vender)

                    # Actualizar la lista de productos en el archivo CSV
                    self.sistema_pos.guardar_csv(self.PRODUCTOS_FILE, productos)

                else:
                    # Mostrar mensaje de error si no hay suficiente cantidad para vender
                    messagebox.showerror("Error", f"No hay suficiente cantidad disponible para vender el producto con ID {id_producto}.")

            # Preguntar al cliente si desea seguir comprando
            continuar_comprando = messagebox.askyesno("Continuar Comprando", "¿Desea seguir comprando?")

            # Cerrar la ventana de venta si el cliente desea continuar comprando
            if continuar_comprando:
                ventana.destroy()

            # Si el cliente no desea seguir comprando o ha terminado la selección, generar la factura
            else:
                # Convertir el diccionario de detalles temporales a una lista de diccionarios para la factura
                detalles_factura = list(self.detalles_temporales.values())

                # Calcular el total sumando los subtotales de todos los productos en la lista de detalles de factura
                total_venta = sum(detalle['Subtotal'] for detalle in detalles_factura)

                # Generar la factura única con todos los detalles de la venta
                id_factura, cliente_info, _, _ = self.sistema_pos.gestion_factura.generar_factura(cliente_id, detalles_factura, total_venta)

                # Si se generó la factura correctamente, imprimir y guardar en archivo
                if id_factura:
                    self.imprimir_factura(id_factura, cliente_info, detalles_factura, total_venta)
                    messagebox.showinfo("Información", "Compra exitosa.")
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo generar la factura.")

                # Limpiar los detalles temporales después de generar la factura
                self.detalles_temporales.clear()

                # Actualizar la lista de productos en la ventana principal
                self.actualizar_lista_productos()

        except ValueError:
            # Mostrar mensaje de error si la cantidad a vender no es un número entero
            messagebox.showerror("Error", "Por favor, introduce una cantidad válida.")


    
  
 

            
                    
            
            
    
    def imprimir_factura(self, id_factura, cliente_info, detalles_factura, total_factura):
        # Definir el nombre del archivo CSV
        nombre_archivo = "factura_imprimir.csv"

        # Concatenar todos los detalles de la factura en una sola cadena
        detalles_concatenados = "\n".join([str(detalle) for detalle in detalles_factura])

        # Abrir el archivo en modo de adición (append) y crear un objeto escritor CSV
        with open(nombre_archivo, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Escribir la información de la factura en el archivo CSV
            writer.writerow(["Factura TIENDA LA QUINTA S.A:"])
            writer.writerow(["ID Factura:", id_factura])
            writer.writerow(["Cliente:", cliente_info])
            writer.writerow(["Detalles de la factura:\n ", detalles_concatenados])
            writer.writerow(["Total:", total_factura])

        print("La factura se ha guardado en el archivo:", nombre_archivo)

    
    

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
