import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd


class InventorySelect(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.inv_file = None
        self._change_inv_file()
        self._create_gui()
        self.pack()

    def _create_gui(self):
        box_inv_file = tk.Label(self, text=self.inv_file)
        box_inv_file.pack()

    def _change_inv_file(self):
        self.inv_file = filedialog.askopenfilename()
        print(self.inv_file)


def main():
    app = tk.Tk()
    app.title("Gestionnaire d'inventaire")
    InventorySelect(app)
    app.mainloop()


if __name__ == "__main__":
    main()

