 self.inicializar_archivos()
        self.root = tk.Tk()
        self.root.title("Sistema de Punto de Venta")
        self.root.geometry("600x400")  # Tamaño de la ventana principal
        self.configurar_interfaz()
        self.gestion_factura = GestionFactura(self) 
        self.root.mainloop()
        self.inicializar_archivos() 
        self.informes_analisis = InformesAnalisis()