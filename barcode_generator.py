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
        self.generate_button = tk.Button(root, text="Generate barcode!", command=self.generate_barcode)
        self.generate_button.pack()
        self.canvas = tk.Canvas(root, width=250, height=300, bg="white")
        self.canvas.pack()

    def generate_barcode(self):
        # Validate code
        self.code = self.code_var.get()
        self.filter = filter(str.isdigit, self.code)
        self.code_filtered = "".join(self.filter)
        if len(self.code_filtered) != 12:
            showerror(self.title,"Please enter correct input code.")
            return False
        # Validate save path
        self.filename = self.filename_var.get()
        # Tambahkan check digit ke 12 digit code
        self.code_checked = self.code_filtered + str(checkdigit(self.code_filtered))
        # Hapus canvas sekarang dan buat object barcode_canvas baru
        self.canvas.destroy()
        self.canvas = barcode_canvas(self.root,self.code_checked)
        self.canvas.pack()
        return True

    def mainloop(self):
        self.root.mainloop()

class barcode_canvas(tk.Canvas):
    # Konstanta yang digunakan dalam class ini
    L_CODE = ("0001101", "0011001", "0010011", "0111101", "0100011", "0110001", "0101111", "0111011", "0110111", "0001011")
    G_CODE = ("0100111", "0110011", "0011011", "0100001", "0011101", "0111001", "0000101", "0010001", "0001001", "0010111")
    R_CODE = ("1110010", "1100110", "1101100", "1000010", "1011100", "1001110", "1010000", "1000100", "1001000", "1110100")
    FIRST_STRUCTURE = ("LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG", "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL")
    SECOND_STRUCTURE = ("RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR")
    START_POSITION = (30,80)
    SEPARATOR_HEIGHT = 22 # TODO change initial value
    NORMAL_HEIGHT = 25 # TODO change initial value

    def __init__(self, root, code) -> None:
        # Init parent class (tk.Canvas) dengan ukuran dan warna yang sesuai
        super().__init__(root, width=250, height=300, bg="white")
        # Dari code yang telah dipass sebagai parameter dari constructor barcode_canvas, encode terlebih dahulu
        self.code = code
        self.encoded = self.get_encoded()
        # Buat barcode dari hasil encode
        self.draw_barcode()

    def get_encoded(self):
        """
        Fungsi ini mengembalikan list yang berisi kedua bagian self.code yang sudah diencode TANPA guard sequence.
        """
        first_seq = self.code[1:7]
        first_digit = int(self.code[0])
        first_group = self.FIRST_STRUCTURE[first_digit]
        second_seq = self.code[7:]
        second_group = self.SECOND_STRUCTURE[first_digit]
        first_encoded = ""
        second_encoded = ""
        # FIRST SEQUENCE
        for index,code_type in enumerate(first_group):
            curr_digit = int(first_seq[index])
            if code_type == "L":
                first_encoded += self.L_CODE[curr_digit]
            else:
                first_encoded += self.G_CODE[curr_digit]
        # SECOND SEQUENCE
        for index,code_type in enumerate(second_group):
            curr_digit = int(second_seq[index])
            second_encoded += self.R_CODE[curr_digit]
        return (first_encoded,second_encoded)

    def draw_barcode(self):
        """
        Fungsi ini menggambar barcode dengan data yang sudah diencode di self.encoded.
        """
        def draw_bar(bit,start_x,start_y,width,color,guard=False):
            if guard:
                end_y = start_y + self.SEPARATOR_HEIGHT
            else:
                end_y = start_y + self.NORMAL_HEIGHT
            if bit == "0":
                fill = "white"
            else:
                fill = color
            end_x = start_x + width
            self.create_rectangle(start_x,start_y,end_x,end_y,fill=fill,width=0)
        current_x = self.START_POSITION[0]
        current_y = self.START_POSITION[1]
        width = 2
        # Draw opening guard (101)
        for bit in "101":
            draw_bar(bit,current_x,current_y,width,"red",True)
            current_x += width
        # Draw first seq
        for bit in self.encoded[0]:
            draw_bar(bit,current_x,current_y,width,"blue")
            current_x += width
        # Draw middle guard (01010)
        for bit in "01010":
            draw_bar(bit,current_x,current_y,width,"red",True)
            current_x += width
        # Draw second seq
        for bit in self.encoded[1]:
            draw_bar(bit,current_x,current_y,width,"green")
            current_x += width
        # Draw end guard (101)
        for bit in "101":
            draw_bar(bit,current_x,current_y,width,"red",True)
            current_x += width
    

def checkdigit(code):
    # Konstanta untuk "weight" setiap digit (misal, digit ke-3 weightnya 1 ada di index 2)
    POSITION_WEIGHT = (1,3,1,3,1,3,1,3,1,3,1,3)
    weighted_sum = 0
    for index,digit in enumerate(code):
        digit_int = int(digit)
        weighted_digit = digit_int * POSITION_WEIGHT[index]
        weighted_sum += weighted_digit
    weighted_sum_modulo = weighted_sum % 10
    if weighted_sum_modulo != 0:
        return str(10 - weighted_sum_modulo)
    else:
        return weighted_sum_modulo


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