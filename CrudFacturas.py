import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import csv

class CrudFacturas:
    FACTURAS_FILE = 'facturas.csv'
    FACTURAS_IMPRIMIR_FILE = 'factura_imprimir.csv'

    def __init__(self, sistema_pos):
        self.sistema_pos = sistema_pos
        self.root = tk.Toplevel()
        self.root.title("Gestión de Facturas")
        self.root.geometry("800x500")  # Tamaño de la ventana de gestión de facturas
        self.configurar_interfaz()
        self.actualizar_lista_facturas()
        self.root.mainloop()
    
    def actualizar_lista_facturas(self):
        # Limpiar el Treeview antes de actualizar
        self.tree.delete(*self.tree.get_children())
        # Recargar la lista de facturas
        facturas = self.sistema_pos.leer_csv(self.sistema_pos.FACTURAS_FILE)
        for factura in facturas:
            self.tree.insert("", "end", text=factura['idFactura'], values=(factura['idCliente'], factura['fechaFactura'], factura['totalFactura'] , factura['nombreProducto'], factura['cantidadVendida'], factura['precioUnitario']))

    def ventana_actualizar_factura(self):
        seleccion = self.tree.selection()
        if seleccion:
            id_factura = self.tree.item(seleccion[0])['text']
            facturas = self.sistema_pos.leer_csv(self.sistema_pos.FACTURAS_FILE)
            datos_factura = next((factura for factura in facturas if factura['idFactura'] == id_factura), None)
            if datos_factura:
                ventana_actualizar = tk.Toplevel(self.root)
                ventana_actualizar.title("Actualizar Factura")

                tk.Label(ventana_actualizar, text="ID Cliente").grid(row=0, column=0)
                entry_id_cliente = tk.Entry(ventana_actualizar)
                entry_id_cliente.insert(0, datos_factura['idCliente'])
                entry_id_cliente.grid(row=0, column=1)

                tk.Label(ventana_actualizar, text="Fecha de Factura").grid(row=1, column=0)
                entry_fecha_factura = DateEntry(ventana_actualizar, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
                entry_fecha_factura.set_date(datos_factura['fechaFactura'])
                entry_fecha_factura.grid(row=1, column=1)

                tk.Label(ventana_actualizar, text="Total Factura").grid(row=2, column=0)
                entry_total_factura = tk.Entry(ventana_actualizar)
                entry_total_factura.insert(0, datos_factura['totalFactura'])
                entry_total_factura.grid(row=2, column=1)

                tk.Label(ventana_actualizar, text="Nombre Producto").grid(row=3, column=0)
                entry_nombre_producto = tk.Entry(ventana_actualizar)
                entry_nombre_producto.insert(0, datos_factura['nombreProducto'])
                entry_nombre_producto.grid(row=3, column=1)

                tk.Label(ventana_actualizar, text="Cantidad Vendida").grid(row=4, column=0)
                entry_cantidad_vendida = tk.Entry(ventana_actualizar)
                entry_cantidad_vendida.insert(0, datos_factura['cantidadVendida'])
                entry_cantidad_vendida.grid(row=4, column=1)

                tk.Label(ventana_actualizar, text="Precio Unitario").grid(row=5, column=0)
                entry_precio_unitario = tk.Entry(ventana_actualizar)
                entry_precio_unitario.insert(0, datos_factura['precioUnitario'])
                entry_precio_unitario.grid(row=5, column=1)

                btn_guardar_actualizacion = tk.Button(ventana_actualizar, text="Guardar", command=lambda: self.guardar_actualizacion_factura(id_factura, entry_id_cliente.get(), entry_fecha_factura.get(), entry_total_factura.get(), entry_nombre_producto.get(), entry_cantidad_vendida.get(), entry_precio_unitario.get(), ventana_actualizar))
                btn_guardar_actualizacion.grid(row=6, columnspan=2)
            else:
                messagebox.showerror("Error", "No se encontraron datos de la factura.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona una factura para actualizar.")

    def guardar_actualizacion_factura(self, id_factura, id_cliente, fecha_factura, total_factura, nombre_producto, cantidad_vendida, precio_unitario, ventana):
        facturas = self.sistema_pos.leer_csv(self.sistema_pos.FACTURAS_FILE)
        for factura in facturas:
            if factura['idFactura'] == id_factura:
                factura['idCliente'] = id_cliente
                factura['fechaFactura'] = fecha_factura
                factura['totalFactura'] = total_factura
                factura['nombreProducto'] = nombre_producto
                factura['cantidadVendida'] = cantidad_vendida
                factura['precioUnitario'] = precio_unitario
                break
        self.sistema_pos.guardar_csv(self.sistema_pos.FACTURAS_FILE, facturas)
        messagebox.showinfo("Información", "Factura actualizada exitosamente.")
        ventana.destroy()
        self.actualizar_lista_facturas()

    def ventana_eliminar_factura(self):
        seleccion = self.tree.selection()
        if seleccion:
            confirmar_eliminar = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar la factura seleccionada?")
            if confirmar_eliminar:
                id_factura = self.tree.item(seleccion[0])['text']
                self.sistema_pos.eliminar_factura(id_factura)
                messagebox.showinfo("Información", "Factura eliminada exitosamente.")
                self.actualizar_lista_facturas()
        else:
            messagebox.showerror("Error", "Por favor, selecciona una factura para eliminar.")
    

    def ventana_agregar_factura(self):
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Factura")

        tk.Label(ventana_agregar, text="ID Factura").grid(row=0, column=0)
        entry_id_factura = tk.Entry(ventana_agregar)
        entry_id_factura.grid(row=0, column=1)

        tk.Label(ventana_agregar, text="ID Cliente").grid(row=1, column=0)
        entry_id_cliente = tk.Entry(ventana_agregar)
        entry_id_cliente.grid(row=1, column=1)

        tk.Label(ventana_agregar, text="Fecha de Factura").grid(row=2, column=0)
        cal_fecha_factura = DateEntry(ventana_agregar, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        cal_fecha_factura.grid(row=2, column=1)

        tk.Label(ventana_agregar, text="Total Factura").grid(row=3, column=0)
        entry_total_factura = tk.Entry(ventana_agregar)
        entry_total_factura.grid(row=3, column=1)

        tk.Label(ventana_agregar, text="Nombre Producto").grid(row=4, column=0)
        entry_nombre_producto = tk.Entry(ventana_agregar)
        entry_nombre_producto.grid(row=4, column=1)

        tk.Label(ventana_agregar, text="Cantidad Vendida").grid(row=5, column=0)
        entry_cantidad_vendida = tk.Entry(ventana_agregar)
        entry_cantidad_vendida.grid(row=5, column=1)

        tk.Label(ventana_agregar, text="Precio Unitario").grid(row=6, column=0)
        entry_precio_unitario = tk.Entry(ventana_agregar)
        entry_precio_unitario.grid(row=6, column=1)

        btn_guardar = tk.Button(ventana_agregar, text="Guardar", command=lambda: self.guardar_factura(entry_id_factura.get(), entry_id_cliente.get(), cal_fecha_factura.get(), entry_total_factura.get(), entry_nombre_producto.get(), entry_cantidad_vendida.get(), entry_precio_unitario.get(), ventana_agregar))
        btn_guardar.grid(row=7, columnspan=2)

    def guardar_factura(self, id_factura, id_cliente, fecha_factura, total_factura, nombre_producto, cantidad_vendida, precio_unitario, ventana):
        # Verifica si todos los campos están llenos
        if id_factura and id_cliente and fecha_factura and total_factura and nombre_producto and cantidad_vendida and precio_unitario:
            factura_nueva = {
                'idFactura': id_factura,
                'idCliente': id_cliente,
                'fechaFactura': fecha_factura,
                'totalFactura': total_factura,
                'nombreProducto': nombre_producto,
                'cantidadVendida': cantidad_vendida,
                'precioUnitario': precio_unitario
            }
            # Guarda la nueva factura en el archivo CSV
            facturas = self.sistema_pos.leer_csv(self.sistema_pos.FACTURAS_FILE)
            facturas.append(factura_nueva)
            self.sistema_pos.guardar_csv(self.sistema_pos.FACTURAS_FILE, facturas)
            messagebox.showinfo("Información", "Factura agregada exitosamente.")
            ventana.destroy()
            self.actualizar_lista_facturas()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def leer_csv(self, archivo):
        with open(archivo, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def guardar_csv(self, archivo, datos):
        if datos:  # Verifica si la lista de datos no está vacía
            with open(archivo, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=datos[0].keys())
                writer.writeheader()
                for data in datos:
                    writer.writerow(data)
        else:
            print("La lista de datos está vacía. No se guardará ningún dato en el archivo CSV.")
            
    
    
    
    def limpiar_facturas_imprimir(self):
        confirmacion = messagebox.askyesno("Confirmar limpieza", "¿Estás seguro de que deseas limpiar el contenido de Facturas_imprimir?")
        if confirmacion:
            try:
                with open(self.FACTURAS_IMPRIMIR_FILE, 'r+') as file:
                    file.truncate(0)
                messagebox.showinfo("Información", "Contenido de Facturas_imprimir limpiado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo limpiar el archivo: {str(e)}")






    def configurar_interfaz(self):
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("ID Cliente", "Fecha Factura", "Total Factura", "Nombre Producto", "Cantidad Vendida", "Precio Unitario")
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100, anchor='center')
        self.tree.pack(expand=True, fill="both")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        btn_actualizar = tk.Button(btn_frame, text="Actualizar", command=self.ventana_actualizar_factura)
        btn_actualizar.grid(row=0, column=0, padx=5)
        
        btn_eliminar = tk.Button(btn_frame, text="Eliminar", command=self.ventana_eliminar_factura)
        btn_eliminar.grid(row=0, column=1, padx=5)
        
        btn_limpiar = tk.Button(btn_frame, text="Limpiar Facturas_imprimir", command=self.limpiar_facturas_imprimir)
        btn_limpiar.grid(row=0, column=3, padx=5)

if __name__ == "__main__":
    CrudFacturas()
