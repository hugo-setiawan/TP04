import tkinter as tk
from tkinter.font import Font
from tkinter.messagebox import showerror
import string

class barcode_gui:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.title = "EAN-13 Barcode Generator"
        self.root.title(self.title)
        self.label_font = Font(family="Helvetica", weight="bold")
        self.save_label = tk.Label(root,text="Save barcode to PS file [eg: EAN13.eps]:", font=self.label_font)
        self.save_label.pack()
        self.filename_var = tk.StringVar()
        self.filename_field = tk.Entry(root, textvariable=self.filename_var)
        self.filename_field.pack()
        self.code_label = tk.Label(root,text="Enter code (first 12 decimal digits):", font=self.label_font)
        self.code_label.pack()
        self.code_var = tk.StringVar()
        self.code_field = tk.Entry(root, textvariable=self.code_var)
        self.code_field.pack()
        self.canvas = tk.Canvas(root, width=250, height=300, bg="white")
        self.canvas.pack()

    def mainloop(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    window = barcode_gui(root)
    window.mainloop()

if __name__ == "__main__":
    main()

# References
# https://www.youtube.com/watch?v=5buJAAa_AX4 (for EAN-13 barcode generation)
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter
# https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names (for filename validation)