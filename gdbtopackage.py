import tkinter as tk
from tkinter import filedialog, messagebox
from osgeo import ogr
import os


class ConvertirApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversión GDB a GPKG")
        self.root.geometry("400x200")

        # Variable para guardar la ruta seleccionada
        self.gdb_path = tk.StringVar()

        # Etiqueta y botón para seleccionar la carpeta .gdb
        tk.Label(root, text="Seleccione la carpeta .gdb", font=("Arial", 12)).pack(pady=10)
        self.entry_gdb = tk.Entry(root, textvariable=self.gdb_path, width=50)
        self.entry_gdb.pack(pady=5)

        tk.Button(root, text="Seleccionar carpeta .gdb", command=self.select_gdb_folder).pack(pady=5)

        # Botón para iniciar la conversión
        tk.Button(root, text="Iniciar Conversión", command=self.iniciar_conversion).pack(pady=20)

    def select_gdb_folder(self):
        gdb_folder = filedialog.askdirectory(title="Seleccionar carpeta .gdb")
        if gdb_folder:
            self.gdb_path.set(gdb_folder)

    def iniciar_conversion(self):
        if not self.gdb_path.get():
            messagebox.showwarning("Advertencia", "Por favor, selecciona la carpeta GDB.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".gpkg",
                                                   filetypes=[("GPKG Files", "*.gpkg")],
                                                   title="Guardar archivo .gpkg")

        if not output_path:
            return

        # Ejecutar la conversión
        self.convert_gdb_to_gpkg(self.gdb_path.get(), output_path)

    def convert_gdb_to_gpkg(self, gdb_folder, output_path):
        # Elimina el archivo de salida si ya existe
        if os.path.exists(output_path):
            os.remove(output_path)

        driver = ogr.GetDriverByName('OpenFileGDB')
        if driver is None:
            messagebox.showerror("Error", "Driver OpenFileGDB no está disponible.")
            return

        # Abre la carpeta GDB como un geodatabase
        gdb = driver.Open(gdb_folder, 0)
        if not gdb:
            messagebox.showerror("Error", f"No se pudo abrir la geodatabase GDB: {gdb_folder}")
            return

        output_driver = ogr.GetDriverByName('GPKG')
        if output_driver is None:
            messagebox.showerror("Error", "No se pudo encontrar el driver de salida.")
            return

        # Crea el DataSource de salida
        output_layer = output_driver.CreateDataSource(output_path)
        if output_layer is None:
            messagebox.showerror("Error", "No se pudo crear el archivo de salida.")
            return

        for i in range(gdb.GetLayerCount()):
            layer = gdb.GetLayerByIndex(i)
            output_layer.CopyLayer(layer, layer.GetName())

        messagebox.showinfo("Éxito", "Conversión completada.")


# Crear la aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ConvertirApp(root)
    root.mainloop()
