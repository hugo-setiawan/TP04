import tkinter as tk
from tkinter.font import Font

class GUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.label_font = Font(family="Helvetica", weight="bold")
        self.save_label = tk.Label(text="Save barcode to PS file [eg: EAN13.eps]:", font=label_font)
        self.save_label.pack()
        # INSERT TEXTBOX FOR FILENAME HERE
        self.code_label = tk.Label(text="Enter code (first 12 decimal digits):", font=label_font)
        self.code_label.pack()
        # INSERT TEXTBOX FOR FILENAME HERE
        # INSERT CANVAS HERE

    def mainloop(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    window = GUI(root)
    window.mainloop()

if __name__ == "__main__":
    main()