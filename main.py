from tkinter import ttk, filedialog
import tkinter as tk
import csv
import json


class InventoryGui(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.inv_file = tk.StringVar()
        self.inv_file.set(default_path)
        self.objects_list = []
        self.objects_info = {}
        self._create_gui()
        self._load_objects()
        self.pack()
        root.protocol("WM_DELETE_WINDOW", self._on_close)
    def _create_gui(self):
        frm_inv_file = ttk.Frame(self)
        entry_inv_file = ttk.Entry(frm_inv_file, textvariable=self.inv_file, width=80)
        entry_inv_file.grid(row=0, column=0)

        btn_inv_file = ttk.Button(frm_inv_file, text="Fichier", command=self._change_inv_file)
        btn_inv_file.grid(row=0, column=1)

        frm_inv_file.grid(row=0, column=0)

        frm_inv_list = ttk.Frame(self)

        # Listbox pour afficher les objets
        self.listbox_objects = tk.Listbox(frm_inv_list)
        self.listbox_objects.grid(row=1, column=0)

        # Bouton pour charger les objets à partir du fichier
        btn_load_objects = ttk.Button(frm_inv_list, text="Charger les objets", command=self._load_objects)
        btn_load_objects.grid(row=2, column=0)

        # Ajout de l'onglet d'ajout d'objet
        notebook = ttk.Notebook(frm_inv_list)
        notebook.grid(row=1, column=1, rowspan=2, padx=10)

        add_tab = ttk.Frame(notebook)
        notebook.add(add_tab, text="Ajouter un objet")

        # Bouton pour supprimer un objet
        btn_delete_object = ttk.Button(frm_inv_list, text="Supprimer", command=self._delete_object)
        btn_delete_object.grid(row=3, column=1, padx=10)

        # Simple et doubleclic sur un objet dans le Listbox
        self.listbox_objects.bind("<Double-Button-1>", lambda event: self._show_object_details())

        lbl_add_object = ttk.Label(add_tab, text="Nom de l'objet:")
        lbl_add_object.grid(row=0, column=0, padx=50, pady=5)

        self.entry_add_object = ttk.Entry(add_tab)
        self.entry_add_object.grid(row=0, column=1, padx=5, pady=5)

        lbl_add_reference = ttk.Label(add_tab, text="Référence:")
        lbl_add_reference.grid(row=1, column=0, padx=50, pady=5)

        self.entry_add_reference = ttk.Entry(add_tab)
        self.entry_add_reference.grid(row=1, column=1, padx=5, pady=5)

        lbl_add_date = ttk.Label(add_tab, text="Date d'emprunt:")
        lbl_add_date.grid(row=2, column=0, padx=50, pady=5)

        self.entry_add_date = ttk.Entry(add_tab)
        self.entry_add_date.grid(row=2, column=1, padx=5, pady=5)

        lbl_add_time = ttk.Label(add_tab, text="Heure d'emprunt:")
        lbl_add_time.grid(row=3, column=0, padx=50, pady=5)

        self.entry_add_time = ttk.Entry(add_tab)
        self.entry_add_time.grid(row=3, column=1, padx=5, pady=5)

        lbl_add_borrower = ttk.Label(add_tab, text="Emprunté par:")
        lbl_add_borrower.grid(row=4, column=0, padx=50, pady=5)

        self.entry_add_borrower = ttk.Entry(add_tab)
        self.entry_add_borrower.grid(row=4, column=1, padx=5, pady=5)

        btn_add_object = ttk.Button(add_tab, text="Ajouter", command=self._add_object)
        btn_add_object.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

        frm_inv_list.grid(row=1, column=0, padx=10, pady=10)

    def _change_inv_file(self):
        file_path = filedialog.askopenfilename(parent=self,
                                               title="Selection du fichier d'inventaire",
                                               initialdir="./",
                                               filetypes=[("Fichiers CSV", "*.csv")])
        if file_path:
            self.inv_file.set(file_path)

    def _on_close(self):
        self._save_objects_to_csv()
        app_root.destroy()

    def _load_objects(self):
        if not self.objects_list:  # Charger uniquement si la liste est vide
            file_path = self.inv_file.get()
            if file_path:
                try:
                    self.objects_list = []
                    self.objects_info = {}
                    with open(file_path, 'r') as csv_file:
                        csv_reader = csv.reader(csv_file)
                        next(csv_reader)  # Ignorer l'en-tête
                        for row in csv_reader:
                            object_name = row[0]
                            self.objects_list.append(object_name)
                            self.objects_info[object_name] = row[1]

                    self._update_objects_listbox()
                except Exception as e:
                    print(f"Erreur lors du chargement des objets : {e}")

    def _update_objects_listbox(self):
        self.listbox_objects.delete(0, tk.END)  # Efface les éléments actuels dans le Listbox
        for obj in self.objects_list:
            self.listbox_objects.insert(tk.END, obj)  # Ajoute chaque objet dans le Listbox

    def _add_object(self):
        object_name = self.entry_add_object.get()
        reference = self.entry_add_reference.get()
        date = self.entry_add_date.get()
        time = self.entry_add_time.get()
        borrower = self.entry_add_borrower.get()

        if object_name:
            self.objects_list.append(object_name)
            self.objects_info[object_name] = json.dumps({
                'Référence': reference,
                'Date d\'emprunt': date,
                'Heure d\'emprunt': time,
                'Emprunté par': borrower
            })
            self._update_objects_listbox()
            self._save_objects_to_csv()
            self.entry_add_object.delete(0, tk.END)
            self.entry_add_reference.delete(0, tk.END)
            self.entry_add_date.delete(0, tk.END)
            self.entry_add_time.delete(0, tk.END)
            self.entry_add_borrower.delete(0, tk.END)

    def _save_objects_to_csv(self):
        file_path = self.inv_file.get()
        if file_path:
            try:
                def _save_objects_to_csv(self):
                    with open(self.csv_filename, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Nom', 'Référence', 'Date d\'emprunt', 'Heure d\'emprunt', 'Emprunté par'])
                        for object_name, object_info_str in self.objects_info.items():
                            object_info = json.loads(object_info_str)
                            writer.writerow([object_name, object_info['Référence'], object_info['Date d\'emprunt'],
                                             object_info['Heure d\'emprunt'], object_info['Emprunté par']])
            except Exception as e:
                print(f"Erreur lors de l'enregistrement des objets : {e}")

    def _delete_object(self):
        selected_index = self.listbox_objects.curselection()
        if selected_index:
            object_index = selected_index[0]
            deleted_object = self.objects_list.pop(object_index)
            if deleted_object in self.objects_info:
                del self.objects_info[deleted_object]
            self._update_objects_listbox()
            self._save_objects_to_csv()
            print(f"Objet supprimé : {deleted_object}")

    def _edit_object(self, event):
        selected_index = self.listbox_objects.curselection()
        if selected_index:
            object_index = selected_index[0]
            object_name = self.objects_list[object_index]
            edit_window = tk.Toplevel(self)
            edit_window.title("Éditer l'objet")

            lbl_edit_object = ttk.Label(edit_window, text="Nouveau nom de l'objet:")
            lbl_edit_object.grid(row=0, column=0, padx=5, pady=5)

            entry_edit_object = ttk.Entry(edit_window)
            entry_edit_object.grid(row=0, column=1, padx=5, pady=5)
            entry_edit_object.insert(tk.END, object_name)

            btn_save = ttk.Button(edit_window, text="Enregistrer", command=lambda: self._save_edited_object(edit_window, object_index, entry_edit_object.get()))
            btn_save.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def _save_edited_object(self, edit_window, object_index, new_object_name):
        if new_object_name:
            self.objects_list[object_index] = new_object_name
            self._update_objects_listbox()
            self._save_objects_to_csv()
            edit_window.destroy()

    def _show_object_details(self):
        selected_index = self.listbox_objects.curselection()
        if selected_index:
            object_index = selected_index[0]
            object_name = self.objects_list[object_index]
            object_info_str = self.objects_info[object_name]

            # Convertir la chaîne de caractères en dictionnaire
            object_info = json.loads(object_info_str)

            details_window = tk.Toplevel(self)
            details_window.title("Détails de l'objet")

            lbl_name = ttk.Label(details_window, text="Nom:")
            lbl_name.grid(row=0, column=0, padx=5, pady=5)

            lbl_name_value = ttk.Label(details_window, text=object_name)
            lbl_name_value.grid(row=0, column=1, padx=5, pady=5)

            lbl_reference = ttk.Label(details_window, text="Référence:")
            lbl_reference.grid(row=1, column=0, padx=5, pady=5)

            lbl_reference_value = ttk.Label(details_window, text=object_info.get('Référence', 'N/A'))
            lbl_reference_value.grid(row=1, column=1, padx=5, pady=5)

            lbl_date_emprunt = ttk.Label(details_window, text="Date d'emprunt:")
            lbl_date_emprunt.grid(row=2, column=0, padx=5, pady=5)

            lbl_date_emprunt_value = ttk.Label(details_window, text=object_info.get('Date d\'emprunt', 'N/A'))
            lbl_date_emprunt_value.grid(row=2, column=1, padx=5, pady=5)

            lbl_heure_emprunt = ttk.Label(details_window, text="Heure d'emprunt:")
            lbl_heure_emprunt.grid(row=3, column=0, padx=5, pady=5)

            lbl_heure_emprunt_value = ttk.Label(details_window, text=object_info.get('Heure d\'emprunt', 'N/A'))
            lbl_heure_emprunt_value.grid(row=3, column=1, padx=5, pady=5)

            lbl_emprunte_par = ttk.Label(details_window, text="Emprunté par:")
            lbl_emprunte_par.grid(row=4, column=0, padx=5, pady=5)

            lbl_emprunte_par_value = ttk.Label(details_window, text=object_info.get('Emprunté par', 'N/A'))
            lbl_emprunte_par_value.grid(row=4, column=1, padx=5, pady=5)


default_path = "D:/Bureau/Inventaire/data/inv.csv"
app_root = tk.Tk()
app_root.title("Gestion d'inventaire")
app_root.iconbitmap("./enerialogo.ico")
app = InventoryGui(app_root)
app_root.mainloop()
