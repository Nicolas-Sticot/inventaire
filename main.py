from tkinter import ttk, filedialog
import tkinter as tk
import csv


class InventoryGui(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.inv_file = tk.StringVar()
        self.inv_file.set(default_path)
        self.objects_list = []
        self._create_gui()
        self._load_objects()
        self.pack()

    def _create_gui(self):
        frm_inv_file = ttk.Frame(self)
        entry_inv_file = ttk.Entry(frm_inv_file, textvariable=self.inv_file)
        entry_inv_file.grid(row=0, column=0)

        btn_inv_file = ttk.Button(frm_inv_file, text="Fichier", command=self._change_inv_file)
        btn_inv_file.grid(row=0, column=1)

        frm_inv_file.grid(row=0, column=0)

        # Listbox pour afficher les objets
        listbox_objects = tk.Listbox(self)
        listbox_objects.grid(row=1, column=0)

        # Bouton pour charger les objets à partir du fichier
        btn_load_objects = ttk.Button(self, text="Charger les objets", command=self._load_objects)
        btn_load_objects.grid(row=2, column=0)

    def _change_inv_file(self):
        file_path = filedialog.askopenfilename(parent=self,
                                               title="Selection du fichier d'inventaire",
                                               initialdir="./",
                                               filetypes=[("Fichiers CSV", "*.csv")])
        if file_path:
            self.inv_file.set(file_path)

    def _load_objects(self):
        file_path = self.inv_file.get()
        if file_path:
            try:
                self.objects_list = []
                with open(file_path, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader)  # Ignorer l'en-tête
                    for row in csv_reader:
                        object_name = row[0]
                        self.objects_list.append(object_name)

                self._update_objects_listbox()
            except Exception as e:
                print(f"Erreur lors du chargement des objets : {e}")

    def _update_objects_listbox(self):
        listbox_objects = self.grid_slaves(row=1, column=0)[0]  # Récupère le Listbox
        listbox_objects.delete(0, tk.END)  # Efface les éléments actuels dans le Listbox
        for obj in self.objects_list:
            listbox_objects.insert(tk.END, obj)  # Ajoute chaque objet dans le Listbox


default_path = "./data/inv.csv"
root = tk.Tk()
app = InventoryGui(root)
root.mainloop()
