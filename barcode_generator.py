import tkinter as tk
from tkinter.font import Font
from tkinter.messagebox import showerror

class barcode_gui:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.title = "EAN-13 Barcode Generator"
        self.root.title(self.title)
        self.create_widgets()

    def create_widgets(self):
        """
        Fungsi ini membuat seluruh widget yang terdapat di barcode_gui
        """
        # Buat label dan textbox serta variabelnya untuk filename.
        self.label_font = Font(family="Helvetica", weight="bold")
        self.save_label = tk.Label(self.root,text="Save barcode to PS file [eg: EAN13.eps]:", font=self.label_font)
        self.save_label.pack()
        self.filename_var = tk.StringVar()
        self.filename_field = tk.Entry(self.root, textvariable=self.filename_var)
        self.filename_field.bind('<Return>',self.generate_barcode)
        self.filename_field.pack()

        # Buat label dan textbox serta variabelnya untuk code yang hendak dibuat barcodenya.
        self.code_label = tk.Label(self.root,text="Enter code (first 12 decimal digits):", font=self.label_font)
        self.code_label.pack()
        self.code_var = tk.StringVar()
        self.code_field = tk.Entry(self.root, textvariable=self.code_var)
        self.code_field.bind('<Return>',self.generate_barcode)
        self.code_field.pack()

        # Buat tombol untuk mengenerate barcode (di samping ini, user juga dapat menekan enter pada textbox)
        self.generate_button = tk.Button(self.root, text="Generate barcode!", command=self.generate_barcode)
        self.generate_button.pack()
        self.canvas = tk.Canvas(self.root, width=250, height=300, bg="white")
        self.canvas.pack()

    def generate_barcode(self, event=None):
        # Validate code
        self.code = self.code_var.get()
        self.filter = filter(str.isdigit, self.code)
        self.code_filtered = "".join(self.filter)
        if len(self.code_filtered) != 12:
            showerror(self.title,"Please enter correct input code.")
        else:
            # Validate save path
            self.filename = self.filename_var.get()
            if not valid_filename(self.filename):
                showerror(self.title,"Please enter correct filename.")
            else:
                # Tambahkan check digit ke 12 digit code
                self.code_checked = self.code_filtered + checkdigit(self.code_filtered)
                # Hapus canvas sekarang dan buat object barcode_canvas baru
                self.canvas.destroy()
                self.canvas = barcode_canvas(self.root,self.code_checked)
                self.canvas.pack()
                self.canvas.update()
                self.canvas.postscript(file=self.filename)

    def mainloop(self):
        self.root.mainloop()

class barcode_canvas(tk.Canvas):
    # Konstanta yang digunakan dalam class ini
    L_CODE = ("0001101", "0011001", "0010011", "0111101", "0100011", "0110001", "0101111", "0111011", "0110111", "0001011")
    G_CODE = ("0100111", "0110011", "0011011", "0100001", "0011101", "0111001", "0000101", "0010001", "0001001", "0010111")
    R_CODE = ("1110010", "1100110", "1101100", "1000010", "1011100", "1001110", "1010000", "1000100", "1001000", "1110100")
    FIRST_STRUCTURE = ("LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG", "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL")
    SECOND_STRUCTURE = ("RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR", "RRRRRR")
    START_POSITION = (40,80)
    SEPARATOR_HEIGHT = 140
    NORMAL_HEIGHT = 130

    def __init__(self, root, code):
        # Init parent class (tk.Canvas) dengan ukuran dan warna yang sesuai
        super().__init__(root, width=250, height=300, bg="white")
        # Dari code yang telah dipass sebagai parameter dari constructor barcode_canvas, encode terlebih dahulu
        self.code = code
        self.encoded = self.get_encoded()
        # Buat barcode serta tulisan-tulisan dari hasil encode
        self.draw_barcode()
        self.draw_text()

    def get_encoded(self):
        """
        Fungsi ini mengembalikan list yang berisi kedua bagian self.code yang sudah diencode TANPA guard sequence.
        """
        def encode(digit,code_type):
            """
            Fungsi ini mengembalikan encoded code yang sesuai untuk digit yang dimasukkan.
            """
            if code_type == "L":
                return self.L_CODE[digit]
            elif code_type == "G":
                return self.G_CODE[digit]
            else:
                return self.R_CODE[digit]

        # Ambil digit pertama (digunakan untuk menentukan struktur)
        first_digit = int(self.code[0])

        # Ambil segmen pertama dan kedua serta strukturnya (berdasarkan digit pertama)
        first_seq = self.code[1:7]
        first_group = self.FIRST_STRUCTURE[first_digit]
        first_encoded = ""
        second_seq = self.code[7:]
        second_group = self.SECOND_STRUCTURE[first_digit]
        second_encoded = ""
        
        # Encode segmen pertama
        for index,code_type in enumerate(first_group):
            # Ambil digit sekarang (dalam int), kemudian encode sesuai dengan struktur
            curr_digit = int(first_seq[index])
            first_encoded += encode(curr_digit,code_type)

        # Encode segmen kedua
        for index,code_type in enumerate(second_group):
            curr_digit = int(second_seq[index])
            second_encoded += encode(curr_digit,code_type)

        # Kembalikan dalam tuple yang berisi segmen pertama dan kedua
        return (first_encoded,second_encoded)

    def draw_barcode(self):
        """
        Fungsi ini menggambar barcode dengan data yang sudah diencode di self.encoded.
        """
        def draw_bar(bit,x,start_y,width,color,guard=False):
            """
            Fungsi ini menggambar 1 bar dari barcode tergantung pada bit masukan.
            """
            # Untuk "guard" bar pada ujung dan tengah, gunakan tinggi yang lebih tinggi daripada biasa
            if guard:
                end_y = start_y + self.SEPARATOR_HEIGHT
            else:
                end_y = start_y + self.NORMAL_HEIGHT

            # Jika bit bernilai 0, gambar bar dengan warna putih (sama saja dengan tidak menggambar bar)
            if bit == "0":
                fill = "white"
            else:
                fill = color

            # Buatlah bar (dalam bentuk line) dengan parameter yang sesuai
            self.create_line(x,start_y,x,end_y, fill=fill, width=width)

        # Cari start position kemudian simpan komponen x dan y dalam variabel
        current_x, current_y = self.START_POSITION
        width = 2

        # Draw opening guard (101)
        for bit in "101":
            draw_bar(bit,current_x,current_y,width,"red",True)
            current_x += width

        # Draw first sequence
        for bit in self.encoded[0]:
            draw_bar(bit,current_x,current_y,width,"blue")
            current_x += width

        # Draw middle guard (01010)
        for bit in "01010":
            draw_bar(bit,current_x,current_y,width,"red",True)
            current_x += width

        # Draw second sequence
        for bit in self.encoded[1]:
            draw_bar(bit,current_x,current_y,width,"green")
            current_x += width

        # Draw end guard (101)
        for bit in "101":
            draw_bar(bit,current_x,current_y,width,"red",True)
            current_x += width
    
    def draw_text(self):
        """
        Fungsi ini menulis teks yang mendampingi barcode.
        """
        font = Font(size=15,family="Helvetica",weight="bold")
        # Tulis "EAN-13 Barcode:" di atas barcode
        current_x = self.START_POSITION[0] + 90
        current_y = self.START_POSITION[1] - 20
        self.create_text(current_x,current_y,text="EAN-13 Barcode:",font=font)

        # Set start position utk text di bawah barcode
        current_x = self.START_POSITION[0] - 15
        current_y = self.START_POSITION[1] + self.NORMAL_HEIGHT + 15

        # Tulis digit paling depan dari code
        self.create_text(current_x,current_y,text=self.code[0],font=font,anchor=tk.W)
        current_x += 33

        # Tulis segmen pertama dari code (digit index 1-6)
        self.create_text(current_x,current_y,text=self.code[1:7],font=font,anchor=tk.W)
        current_x += 90

        # Tulis segmen pertama dari code (digit index 7-akhir)
        self.create_text(current_x,current_y,text=self.code[7:],font=font,anchor=tk.W)

        # Tulis check digit dari code
        current_x = self.START_POSITION[0] + 90
        current_y += 30
        self.create_text(current_x,current_y,text=f"Check Digit: {self.code[-1]}",font=font,fill="#f5c816")

def checkdigit(code):
    """
    Fungsi yang menghitung checkdigit dari 12 digit EAN-13 code dan mengembalikan checkdigitnya dalam bentuk string.
    """
    # Konstanta untuk "weight" setiap digit (misal, digit ke-3 (index 2) weightnya 1)
    POSITION_WEIGHT = (1,3,1,3,1,3,1,3,1,3,1,3)
    # Nilai awal weighted sum (total seluruh digit yang telah dikalikan "weight" masing-masing digit)
    weighted_sum = 0

    # Iterasikan setiap digit dalam 12 digit code
    for index,digit in enumerate(code):
        # Jadikan digit dalam bentuk int, kemudian hitung dengan weight dan tambahkan ke weighted sum
        digit_int = int(digit)
        weighted_digit = digit_int * POSITION_WEIGHT[index]
        weighted_sum += weighted_digit

    # Hitung weighted sum mod 10 dan kembalikan checkdigit sesuai spesifikasi yang ada
    weighted_sum_modulo = weighted_sum % 10
    if weighted_sum_modulo != 0:
        return str(10 - weighted_sum_modulo)
    else:
        return str(weighted_sum_modulo)

def valid_filename(filename:str):
    """
    Fungsi yang melakukan validasi filename, di mana filename harus berekstensi .ps atau .eps.
    """
    # Menyimpan filename dalam bentuk upper sementara (hanya untuk pengecekan)
    filename_upper = filename.upper()

    # Cek ekstensi (harus .eps atau .ps, dan ada namanya i.e. bukan cuman ".ps")
    if not (filename_upper.endswith(".EPS") or filename_upper.endswith(".PS")):
        return False
    elif (filename_upper.startswith(".EPS") or filename_upper.startswith(".PS")):
        return False
    # Ketika filename sudah benar return True
    return True

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