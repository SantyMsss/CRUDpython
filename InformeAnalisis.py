import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import DateEntry
from datetime import datetime
import csv

class InformesAnalisis:
    def __init__(self, sistema_pos):
        self.sistema_pos = sistema_pos
        self.root = tk.Toplevel()
        self.root.title("Informes y Análisis")
        self.configurar_interfaz()
        self.root.mainloop()

    def configurar_interfaz(self):
        # Configuración de la interfaz gráfica
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        btn_agotados = tk.Button(self.frame, text="Generar Informe de Productos Agotados", command=self.generar_informe_agotados)
        btn_agotados.grid(row=0, column=0, padx=5, pady=5)

        btn_baja_rotacion = tk.Button(self.frame, text="Generar Informe de Productos con Baja Rotación", command=self.generar_informe_baja_rotacion)
        btn_baja_rotacion.grid(row=1, column=0, padx=5, pady=5)

        btn_ventas_rango = tk.Button(self.frame, text="Generar Informe de Ventas en Rango de Tiempo", command=self.generar_informe_ventas_rango)
        btn_ventas_rango.grid(row=2, column=0, padx=5, pady=5)

    def generar_informe_agotados(self):
        productos = self.sistema_pos.leer_csv(self.sistema_pos.PRODUCTOS_FILE)
        productos_agotados = [producto for producto in productos if int(producto['cantidad']) == 0]

        self.mostrar_informe(productos_agotados, 'Informe de Productos Agotados')

    def generar_informe_baja_rotacion(self):
        # Consideraremos productos con baja rotación aquellos con ventas menores a un umbral, por ejemplo, 10 unidades.
        umbral_baja_rotacion = 10
        productos = self.sistema_pos.leer_csv(self.sistema_pos.PRODUCTOS_FILE)
        ventas = self.sistema_pos.leer_csv(self.sistema_pos.FACTURAS_FILE)

        ventas_por_producto = {}
        for venta in ventas:
            nombre_producto = venta['nombreProducto']
            cantidad_vendida = int(venta['cantidadVendida'])
            if nombre_producto in ventas_por_producto:
                ventas_por_producto[nombre_producto] += cantidad_vendida
            else:
                ventas_por_producto[nombre_producto] = cantidad_vendida

        productos_baja_rotacion = [producto for producto in productos if ventas_por_producto.get(producto['nombre'], 0) < umbral_baja_rotacion]

        self.mostrar_informe(productos_baja_rotacion, 'Informe de Productos con Baja Rotación')

    def generar_informe_ventas_rango(self):
        def obtener_rango():
            fecha_inicio = cal_inicio.get_date()
            fecha_fin = cal_fin.get_date()
            self.informe_ventas_rango(fecha_inicio, fecha_fin, ventana_rango)

        ventana_rango = tk.Toplevel(self.root)
        ventana_rango.title("Seleccionar Rango de Fechas")

        tk.Label(ventana_rango, text="Fecha de Inicio:").grid(row=0, column=0)
        cal_inicio = DateEntry(ventana_rango)
        cal_inicio.grid(row=0, column=1)

        tk.Label(ventana_rango, text="Fecha de Fin:").grid(row=1, column=0)
        cal_fin = DateEntry(ventana_rango)
        cal_fin.grid(row=1, column=1)

        btn_generar = tk.Button(ventana_rango, text="Generar Informe", command=obtener_rango)
        btn_generar.grid(row=2, columnspan=2, pady=10)


    def informe_ventas_rango(self, fecha_inicio, fecha_fin, ventana):
        ventas = self.sistema_pos.leer_csv(self.sistema_pos.FACTURAS_FILE)
        informes_ventas = []
        sumatoria_total = 0

        for venta in ventas:
            fecha_venta = datetime.strptime(venta['fechaFactura'], '%Y-%m-%d').date()
            if fecha_inicio <= fecha_venta <= fecha_fin:
                informes_ventas.append(venta)
                sumatoria_total += float(venta['totalFactura'])

        self.mostrar_informe(informes_ventas, f'Informe de Ventas desde {fecha_inicio} hasta {fecha_fin}', sumatoria_total)
        ventana.destroy()

    def mostrar_informe(self, data, titulo, sumatoria_total=None):
        ventana_informe = tk.Toplevel(self.root)
        ventana_informe.title(titulo)

        text_area = tk.Text(ventana_informe, wrap='word')
        text_area.pack(expand=True, fill='both')

        if data:
            for item in data:
                text_area.insert(tk.END, f"{item}\n")

            if sumatoria_total is not None:
                text_area.insert(tk.END, f"\nSumatoria Total de Ventas: {sumatoria_total}\n")
            
            btn_guardar_csv = tk.Button(ventana_informe, text="Guardar como CSV", command=lambda: self.guardar_informe(data, 'csv'))
            btn_guardar_csv.pack(side=tk.LEFT, padx=5, pady=5)

            btn_guardar_txt = tk.Button(ventana_informe, text="Guardar como TXT", command=lambda: self.guardar_informe(data, 'txt'))
            btn_guardar_txt.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            text_area.insert(tk.END, "No se encontraron datos para el informe.\n")

    def guardar_informe(self, data, file_type):
        file_extension = f".{file_type}"
        file_name = filedialog.asksaveasfilename(defaultextension=file_extension, filetypes=[(file_type.upper(), file_extension)])

        if file_name:
            try:
                if file_type == 'csv':
                    with open(file_name, mode='w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                elif file_type == 'txt':
                    with open(file_name, mode='w') as file:
                        for item in data:
                            file.write(f"{item}\n")

                messagebox.showinfo("Información", f"Informe guardado exitosamente como {file_extension.upper()}.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

if __name__ == "__main__":
    InformesAnalisis()
