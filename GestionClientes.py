import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import SistemaPOS

class GestionClientes:
    CLIENTES_FILE = 'clientes.csv'

    def __init__(self, sistema_pos):
        self.sistema_pos = sistema_pos
        self.root = tk.Toplevel()
        self.root.title("Gestión de Clientes")
        self.root.geometry("800x600")  # Tamaño de la ventana de gestión de clientes
        self.root.configure(bg='light blue')
        self.configurar_interfaz()
        self.actualizar_lista_clientes()
        self.root.mainloop()

    def actualizar_lista_clientes(self):
        # Limpiar el Treeview antes de actualizar
        self.tree.delete(*self.tree.get_children())
        # Recargar la lista de clientes
        clientes = self.sistema_pos.leer_csv(self.CLIENTES_FILE)
        for cliente in clientes:
            self.tree.insert("", "end", text=cliente['idCliente'], values=(cliente['nombre'], cliente['fechaNacimiento'], cliente['documento']))

    def ventana_agregar_cliente(self):
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Cliente")

        tk.Label(ventana_agregar, text="Nombre").grid(row=0, column=0)
        entry_nombre = tk.Entry(ventana_agregar)
        entry_nombre.grid(row=0, column=1)

        tk.Label(ventana_agregar, text="Documento").grid(row=1, column=0)
        entry_documento = tk.Entry(ventana_agregar)
        entry_documento.grid(row=1, column=1)

        tk.Label(ventana_agregar, text="Fecha de Nacimiento").grid(row=2, column=0)
        cal_fecha_nacimiento = DateEntry(ventana_agregar, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        cal_fecha_nacimiento.grid(row=2, column=1)

        btn_guardar = tk.Button(ventana_agregar, text="Guardar", command=lambda: self.guardar_cliente(entry_nombre.get(), cal_fecha_nacimiento.get(), entry_documento.get(), ventana_agregar))
        btn_guardar.grid(row=3, columnspan=2)

    def guardar_cliente(self, nombre, fecha_nacimiento, documento, ventana):
        self.sistema_pos.agregar_cliente(nombre, fecha_nacimiento, documento)
        ventana.destroy()
        self.actualizar_lista_clientes()
        
    def ventana_actualizar_cliente(self):
        seleccion = self.tree.selection()
        if seleccion:
            id_cliente = self.tree.item(seleccion[0])['text']
            clientes = self.sistema_pos.leer_csv(self.CLIENTES_FILE)
            datos_cliente = next((cliente for cliente in clientes if cliente['idCliente'] == id_cliente), None)
            if datos_cliente:
                ventana_actualizar = tk.Toplevel(self.root)
                ventana_actualizar.title("Actualizar Cliente")

                tk.Label(ventana_actualizar, text="Nombre").grid(row=0, column=0)
                entry_nombre = tk.Entry(ventana_actualizar)
                entry_nombre.insert(0, datos_cliente['nombre'])
                entry_nombre.grid(row=0, column=1)

                tk.Label(ventana_actualizar, text="Documento").grid(row=1, column=0)
                entry_documento = tk.Entry(ventana_actualizar)
                entry_documento.insert(0, datos_cliente['documento'])
                entry_documento.grid(row=1, column=1)

                tk.Label(ventana_actualizar, text="Fecha de Nacimiento").grid(row=2, column=0)
                cal_fecha_nacimiento = DateEntry(ventana_actualizar, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
                cal_fecha_nacimiento.set_date(datetime.strptime(datos_cliente['fechaNacimiento'], '%Y-%m-%d'))
                cal_fecha_nacimiento.grid(row=2, column=1)

                btn_guardar_actualizacion = tk.Button(ventana_actualizar, text="Guardar", command=lambda: self.guardar_actualizacion_cliente(id_cliente, entry_nombre.get(), cal_fecha_nacimiento.get(), entry_documento.get(), ventana_actualizar))
                btn_guardar_actualizacion.grid(row=3, columnspan=2)
            else:
                messagebox
                messagebox.showerror("Error", "No se encontraron datos del cliente.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un cliente para actualizar.")

    def guardar_actualizacion_cliente(self, id_cliente, nuevo_nombre, nueva_fecha_nacimiento, nuevo_documento, ventana):
        self.sistema_pos.actualizar_cliente(id_cliente, nuevo_nombre, nueva_fecha_nacimiento, nuevo_documento)
        messagebox.showinfo("Información", "Cliente actualizado exitosamente.")
        ventana.destroy()
        self.actualizar_lista_clientes()

    def ventana_eliminar_cliente(self):
        seleccion = self.tree.selection()
        if seleccion:
            confirmar_eliminacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar el cliente seleccionado?")
            if confirmar_eliminacion:
                id_cliente = self.tree.item(seleccion[0])['text']  # Obtener el ID del cliente seleccionado
                self.sistema_pos.eliminar_cliente(id_cliente)
                messagebox.showinfo("Información", "Cliente eliminado exitosamente.")
                self.actualizar_lista_clientes()
        else:
            messagebox.showerror("Error", "Por favor, selecciona un cliente para eliminar.")

    def configurar_interfaz(self):
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("Nombre", "Fecha de Nacimiento", "Documento")
        self.tree.heading("#0", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Fecha de Nacimiento", text="Fecha de Nacimiento")
        self.tree.heading("Documento", text="Documento")
        self.tree.pack(expand=True, fill="both")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        btn_agregar = tk.Button(btn_frame, text="Agregar", command=self.ventana_agregar_cliente)
        btn_agregar.grid(row=0, column=0, padx=5)

        btn_actualizar = tk.Button(btn_frame, text="Actualizar", command=self.ventana_actualizar_cliente)
        btn_actualizar.grid(row=0, column=1, padx=5)
        
        btn_eliminar = tk.Button(btn_frame, text="Eliminar", command=self.ventana_eliminar_cliente)
        btn_eliminar.grid(row=0, column=2, padx=5)
        
if __name__ == "main":
    sistema_pos = SistemaPOS.SistemaPOS()
    GestionClientes(sistema_pos)
