import tkinter as tk
from tkinter.font import Font

class GUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.label_font = Font(family="Helvetica", weight="bold")
        self.save_label = tk.Label(root,text="Save barcode to PS file [eg: EAN13.eps]:", font=self.label_font)
        self.save_label.pack()
        self.filename = tk.StringVar()
        self.filename_field = tk.Entry(root, textvariable=self.filename)
        self.filename_field.pack()
        self.code_label = tk.Label(root,text="Enter code (first 12 decimal digits):", font=self.label_font)
        self.code_label.pack()
        self.code = tk.StringVar()
        self.code_field = tk.Entry(root, textvariable=self.code)
        self.code_field.pack()
        self.canvas = tk.Canvas(root, width=200, height=200, bg="white")
        self.canvas.pack()

    def mainloop(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    window = GUI(root)
    window.mainloop()

if __name__ == "__main__":
    main()