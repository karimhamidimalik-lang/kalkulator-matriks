import streamlit as st
import numpy as np
import pandas as pd

# ============================================================
# WARNA TAMPILAN
# ============================================================

BG = "#0b1020"
PANEL = "#11182b"
PANEL_2 = "#17213a"
INPUT_BG = "#0d1528"
TEXT = "#f5f7ff"
TEXT2 = "#aeb8d0"
BLUE = "#4f8cff"
BLUE_DARK = "#285dcc"
GREEN = "#27d17f"
RED = "#ff5c7a"
PURPLE = "#9b6cff"
BORDER = "#263653"


# ============================================================
# FUNGSI MATEMATIKA
# ============================================================

def baca_angka(teks):
    teks = teks.strip()

    if teks == "":
        return Fraction(0)

    try:
        return Fraction(teks)
    except:
        try:
            return Fraction(float(teks))
        except:
            raise ValueError(f"Nilai '{teks}' tidak valid.")


def format_angka(x):
    if isinstance(x, Fraction):

        if x.denominator == 1:
            return str(x.numerator)

        return f"{x.numerator}/{x.denominator}"

    return str(x)


def format_desimal(x):
    try:
        return f"{float(x):.4f}"
    except:
        return str(x)


def ukuran(A):
    return len(A), len(A[0])


def format_matriks(A):
    teks = ""

    for baris in A:
        teks += "[  "
        teks += "     ".join(format_angka(x) for x in baris)
        teks += "  ]\n"

    return teks


# ============================================================
# PENJUMLAHAN
# ============================================================

def tambah(A, B):

    if ukuran(A) != ukuran(B):
        raise ValueError(
            "Ukuran matriks A dan B harus sama."
        )

    baris, kolom = ukuran(A)

    hasil = []

    langkah = []

    for i in range(baris):

        baris_hasil = []

        for j in range(kolom):

            nilai = A[i][j] + B[i][j]

            baris_hasil.append(nilai)

            langkah.append(
                f"C{i+1}{j+1} = "
                f"{format_angka(A[i][j])} + "
                f"{format_angka(B[i][j])} = "
                f"{format_angka(nilai)}"
            )

        hasil.append(baris_hasil)

    return hasil, langkah


# ============================================================
# PENGURANGAN
# ============================================================

def kurang(A, B):

    if ukuran(A) != ukuran(B):
        raise ValueError(
            "Ukuran matriks A dan B harus sama."
        )

    baris, kolom = ukuran(A)

    hasil = []

    langkah = []

    for i in range(baris):

        baris_hasil = []

        for j in range(kolom):

            nilai = A[i][j] - B[i][j]

            baris_hasil.append(nilai)

            langkah.append(
                f"C{i+1}{j+1} = "
                f"{format_angka(A[i][j])} - "
                f"{format_angka(B[i][j])} = "
                f"{format_angka(nilai)}"
            )

        hasil.append(baris_hasil)

    return hasil, langkah


# ============================================================
# PERKALIAN
# ============================================================

def kali(A, B):

    baris_A = len(A)
    kolom_A = len(A[0])

    baris_B = len(B)
    kolom_B = len(B[0])

    if kolom_A != baris_B:
        raise ValueError(
            "Kolom A harus sama dengan baris B."
        )

    hasil = [
        [Fraction(0) for _ in range(kolom_B)]
        for _ in range(baris_A)
    ]

    langkah = []

    for i in range(baris_A):

        for j in range(kolom_B):

            bagian = []

            for k in range(kolom_A):

                bagian.append(
                    f"({format_angka(A[i][k])} × "
                    f"{format_angka(B[k][j])})"
                )

                hasil[i][j] += (
                    A[i][k] * B[k][j]
                )

            langkah.append(
                f"C{i+1}{j+1} = "
                + " + ".join(bagian)
                + f" = {format_angka(hasil[i][j])}"
            )

    return hasil, langkah


# ============================================================
# TRANSPOSE
# ============================================================

def transpose(A):

    hasil = [
        list(baris)
        for baris in zip(*A)
    ]

    langkah = []

    for i in range(len(A)):

        for j in range(len(A[0])):

            langkah.append(
                f"A{i+1}{j+1} → T{j+1}{i+1} "
                f"= {format_angka(A[i][j])}"
            )

    return hasil, langkah


# ============================================================
# DETERMINAN
# ============================================================

def determinan(A):

    n = len(A)

    if n != len(A[0]):
        raise ValueError(
            "Determinan hanya dapat dihitung "
            "untuk matriks persegi."
        )

    M = [baris[:] for baris in A]

    hasil = Fraction(1)

    langkah = []

    for i in range(n):

        pivot = i

        while (
            pivot < n
            and M[pivot][i] == 0
        ):
            pivot += 1

        if pivot == n:

            langkah.append(
                "Kolom memiliki pivot 0."
            )

            return Fraction(0), langkah

        if pivot != i:

            M[i], M[pivot] = (
                M[pivot],
                M[i]
            )

            hasil *= -1

            langkah.append(
                f"Tukar R{i+1} ↔ R{pivot+1}"
            )

        pivot_value = M[i][i]

        hasil *= pivot_value

        langkah.append(
            f"Pivot R{i+1} = "
            f"{format_angka(pivot_value)}"
        )

        for j in range(i + 1, n):

            if M[j][i] != 0:

                faktor = (
                    M[j][i] /
                    pivot_value
                )

                for k in range(i, n):

                    M[j][k] -= (
                        faktor * M[i][k]
                    )

                langkah.append(
                    f"R{j+1} = R{j+1} - "
                    f"({format_angka(faktor)})R{i+1}"
                )

    langkah.append(
        f"det(A) = {format_angka(hasil)}"
    )

    return hasil, langkah


# ============================================================
# INVERS
# ============================================================

def invers(A):

    n = len(A)

    if n != len(A[0]):
        raise ValueError(
            "Invers hanya dapat dihitung "
            "untuk matriks persegi."
        )

    M = []

    for i in range(n):

        baris = A[i][:]

        identitas = []

        for j in range(n):

            if i == j:
                identitas.append(Fraction(1))
            else:
                identitas.append(Fraction(0))

        M.append(baris + identitas)

    langkah = []

    for i in range(n):

        pivot = i

        while (
            pivot < n
            and M[pivot][i] == 0
        ):
            pivot += 1

        if pivot == n:

            raise ValueError(
                "Matriks tidak memiliki invers "
                "karena determinannya = 0."
            )

        if pivot != i:

            M[i], M[pivot] = (
                M[pivot],
                M[i]
            )

            langkah.append(
                f"Tukar R{i+1} ↔ R{pivot+1}"
            )

        pivot_value = M[i][i]

        for j in range(2 * n):

            M[i][j] /= pivot_value

        langkah.append(
            f"R{i+1} = R{i+1} / "
            f"{format_angka(pivot_value)}"
        )

        for j in range(n):

            if j != i:

                faktor = M[j][i]

                if faktor != 0:

                    for k in range(2 * n):

                        M[j][k] -= (
                            faktor * M[i][k]
                        )

                    langkah.append(
                        f"R{j+1} = R{j+1} - "
                        f"({format_angka(faktor)})R{i+1}"
                    )

    hasil = []

    for i in range(n):

        hasil.append(
            M[i][n:]
        )

    langkah.append(
        "Bagian kanan matriks menjadi A⁻¹."
    )

    return hasil, langkah


# ============================================================
# APLIKASI
# ============================================================

class KalkulatorMatriks:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "MatrixLab - Kalkulator Matriks"
        )

        self.root.geometry(
            "1200x780"
        )

        self.root.minsize(
            950,
            650
        )

        self.root.configure(
            bg=BG
        )

        self.entries_A = []
        self.entries_B = []

        self.animasi_judul()

        self.buat_interface()

    # ========================================================
    # ANIMASI JUDUL
    # ========================================================

    def animasi_judul(self):

        self.title_colors = [
            BLUE,
            "#638fff",
            "#8b72ff",
            PURPLE,
            "#638fff"
        ]

        self.title_index = 0

        self.root.after(
            300,
            self.ganti_warna_judul
        )

    def ganti_warna_judul(self):

        if hasattr(self, "judul"):

            self.judul.configure(
                fg=self.title_colors[
                    self.title_index
                ]
            )

        self.title_index = (
            self.title_index + 1
        ) % len(self.title_colors)

        self.root.after(
            500,
            self.ganti_warna_judul
        )

    # ========================================================
    # INTERFACE
    # ========================================================

    def buat_interface(self):

        header = tk.Frame(
            self.root,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )

        self.judul = tk.Label(
            header,
            text="MATRIXLAB",
            font=(
                "Segoe UI",
                27,
                "bold"
            ),
            bg=BG,
            fg=BLUE
        )

        self.judul.pack(
            anchor="w"
        )

        subtitle = tk.Label(
            header,
            text=(
                "Kalkulator Matriks • "
                "Perhitungan + Langkah Otomatis"
            ),
            font=(
                "Segoe UI",
                10
            ),
            bg=BG,
            fg=TEXT2
        )

        subtitle.pack(
            anchor="w"
        )

        # ====================================================
        # UKURAN MATRIKS
        # ====================================================

        ukuran_frame = tk.Frame(
            self.root,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        ukuran_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        tk.Label(
            ukuran_frame,
            text="UKURAN MATRIKS",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=PANEL,
            fg=TEXT
        ).pack(
            side="left",
            padx=20
        )

        self.baris_A = self.entry_kecil(
            ukuran_frame,
            "2"
        )

        self.kolom_A = self.entry_kecil(
            ukuran_frame,
            "2"
        )

        tk.Label(
            ukuran_frame,
            text="A",
            bg=PANEL,
            fg=BLUE,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(3, 15)
        )

        self.baris_B = self.entry_kecil(
            ukuran_frame,
            "2"
        )

        self.kolom_B = self.entry_kecil(
            ukuran_frame,
            "2"
        )

        tk.Label(
            ukuran_frame,
            text="B",
            bg=PANEL,
            fg=PURPLE,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(3, 20)
        )

        self.tombol(
            ukuran_frame,
            "＋  BUAT MATRIKS",
            self.buat_matriks,
            BLUE
        ).pack(
            side="left",
            padx=10
        )

        # ====================================================
        # INPUT MATRICES
        # ====================================================

        input_area = tk.Frame(
            self.root,
            bg=BG
        )

        input_area.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.frame_A = self.panel_matriks(
            input_area,
            "MATRIKS A",
            BLUE
        )

        self.frame_A.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        self.frame_B = self.panel_matriks(
            input_area,
            "MATRIKS B",
            PURPLE
        )

        self.frame_B.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        # ====================================================
        # OPERASI
        # ====================================================

        operasi = tk.Frame(
            self.root,
            bg=BG
        )

        operasi.pack(
            fill="x",
            padx=30,
            pady=8
        )

        tombol_data = [
            ("A + B", self.operasi_tambah, BLUE),
            ("A − B", self.operasi_kurang, BLUE),
            ("A × B", self.operasi_kali, GREEN),
            ("Transpose A", self.operasi_transpose, PURPLE),
            ("det(A)", self.operasi_determinan, RED),
            ("A⁻¹", self.operasi_invers, "#ff9f43")
        ]

        for teks, fungsi, warna in tombol_data:

            self.tombol(
                operasi,
                teks,
                fungsi,
                warna
            ).pack(
                side="left",
                padx=4,
                expand=True,
                fill="x"
            )

        # ====================================================
        # HASIL
        # ====================================================

        hasil_frame = tk.Frame(
            self.root,
            bg=BG
        )

        hasil_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(8, 20)
        )

        # Kartu hasil
        kartu_hasil = tk.Frame(
            hasil_frame,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        kartu_hasil.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        tk.Label(
            kartu_hasil,
            text="HASIL",
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            bg=PANEL,
            fg=GREEN
        ).pack(
            anchor="w",
            padx=15,
            pady=10
        )

        self.output_hasil = tk.Text(
            kartu_hasil,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            font=(
                "Consolas",
                14
            ),
            bd=0,
            padx=15,
            pady=15,
            wrap="none"
        )

        self.output_hasil.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # Kartu langkah
        kartu_langkah = tk.Frame(
            hasil_frame,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        kartu_langkah.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        tk.Label(
            kartu_langkah,
            text="LANGKAH PERHITUNGAN",
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            bg=PANEL,
            fg=BLUE
        ).pack(
            anchor="w",
            padx=15,
            pady=10
        )

        self.output_langkah = tk.Text(
            kartu_langkah,
            bg=INPUT_BG,
            fg=TEXT2,
            insertbackground=TEXT,
            font=(
                "Consolas",
                10
            ),
            bd=0,
            padx=15,
            pady=15,
            wrap="word"
        )

        self.output_langkah.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # ====================================================
        # FOOTER BUTTON
        # ====================================================

        footer = tk.Frame(
            self.root,
            bg=BG
        )

        footer.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        self.tombol(
            footer,
            "⟳  RESET",
            self.reset,
            RED
        ).pack(
            side="left"
        )

        self.tombol(
            footer,
            "▣  SALIN HASIL",
            self.salin_hasil,
            GREEN
        ).pack(
            side="right"
        )

        self.buat_matriks()

    # ========================================================
    # ENTRY KECIL
    # ========================================================

    def entry_kecil(
        self,
        parent,
        nilai
    ):

        entry = tk.Entry(
            parent,
            width=4,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            justify="center",
            relief="flat"
        )

        entry.insert(
            0,
            nilai
        )

        entry.pack(
            side="left",
            padx=3,
            pady=12
        )

        return entry

    # ========================================================
    # TOMBOL
    # ========================================================

    def tombol(
        self,
        parent,
        teks,
        fungsi,
        warna
    ):

        tombol = tk.Button(
            parent,
            text=teks,
            command=fungsi,
            bg=warna,
            fg="white",
            activebackground=warna,
            activeforeground="white",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=9
        )

        tombol.bind(
            "<Enter>",
            lambda e: tombol.configure(
                relief="raised"
            )
        )

        tombol.bind(
            "<Leave>",
            lambda e: tombol.configure(
                relief="flat"
            )
        )

        return tombol

    # ========================================================
    # PANEL MATRIKS
    # ========================================================

    def panel_matriks(
        self,
        parent,
        judul,
        warna
    ):

        frame = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        tk.Label(
            frame,
            text=judul,
            bg=PANEL,
            fg=warna,
            font=(
                "Segoe UI",
                11,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=10
        )

        return frame

    # ========================================================
    # BUAT MATRIKS
    # ========================================================

    def buat_matriks(self):

        try:

            rA = int(
                self.baris_A.get()
            )

            cA = int(
                self.kolom_A.get()
            )

            rB = int(
                self.baris_B.get()
            )

            cB = int(
                self.kolom_B.get()
            )

            if min(
                rA,
                cA,
                rB,
                cB
            ) <= 0:

                raise ValueError

            if max(
                rA,
                cA,
                rB,
                cB
            ) > 8:

                raise ValueError(
                    "Maksimal ukuran matriks adalah 8 × 8."
                )

        except:

            messagebox.showerror(
                "Ukuran Tidak Valid",
                "Masukkan ukuran matriks "
                "berupa bilangan bulat positif."
            )

            return

        for widget in self.frame_A.winfo_children():

            if isinstance(
                widget,
                tk.Frame
            ):

                widget.destroy()

        for widget in self.frame_B.winfo_children():

            if isinstance(
                widget,
                tk.Frame
            ):

                widget.destroy()

        self.entries_A = []
        self.entries_B = []

        # Matriks A
        grid_A = tk.Frame(
            self.frame_A,
            bg=PANEL
        )

        grid_A.pack(
            pady=10
        )

        for i in range(rA):

            baris = []

            for j in range(cA):

                entry = self.entry_matriks(
                    grid_A
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                baris.append(entry)

            self.entries_A.append(
                baris
            )

        # Matriks B
        grid_B = tk.Frame(
            self.frame_B,
            bg=PANEL
        )

        grid_B.pack(
            pady=10
        )

        for i in range(rB):

            baris = []

            for j in range(cB):

                entry = self.entry_matriks(
                    grid_B
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                baris.append(entry)

            self.entries_B.append(
                baris
            )

        self.status(
            "✓ Matriks berhasil dibuat"
        )

    # ========================================================
    # ENTRY MATRIKS
    # ========================================================

    def entry_matriks(
        self,
        parent
    ):

        entry = tk.Entry(
            parent,
            width=6,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=BLUE,
            justify="center",
            font=(
                "Consolas",
                12,
                "bold"
            ),
            relief="flat",
            highlightbackground=BORDER,
            highlightcolor=BLUE,
            highlightthickness=1
        )

        entry.insert(
            0,
            "0"
        )

        entry.bind(
            "<FocusIn>",
            lambda e: entry.configure(
                highlightbackground=BLUE
            )
        )

        entry.bind(
            "<FocusOut>",
            lambda e: entry.configure(
                highlightbackground=BORDER
            )
        )

        return entry

    # ========================================================
    # AMBIL MATRIKS
    # ========================================================

    def ambil_matriks(
        self,
        entries
    ):

        hasil = []

        for baris in entries:

            data = []

            for entry in baris:

                data.append(
                    baca_angka(
                        entry.get()
                    )
                )

            hasil.append(data)

        return hasil

    # ========================================================
    # TAMPILKAN HASIL
    # ========================================================

    def tampilkan(
        self,
        nama,
        hasil,
        langkah
    ):

        self.output_hasil.delete(
            "1.0",
            tk.END
        )

        self.output_langkah.delete(
            "1.0",
            tk.END
        )

        self.output_hasil.insert(
            tk.END,
            nama + "\n\n"
        )

        if isinstance(
            hasil,
            list
        ):

            self.output_hasil.insert(
                tk.END,
                format_matriks(
                    hasil
                )
            )

        else:

            self.output_hasil.insert(
                tk.END,
                "det(A) = "
                + format_angka(hasil)
            )

        self.output_langkah.insert(
            tk.END,
            "PROSES PERHITUNGAN\n"
        )

        self.output_langkah.insert(
            tk.END,
            "────────────────────────\n\n"
        )

        for nomor, item in enumerate(
            langkah,
            1
        ):

            self.output_langkah.insert(
                tk.END,
                f"{nomor}. {item}\n\n"
            )

        self.animasi_hasil()

    # ========================================================
    # ANIMASI HASIL
    # ========================================================

    def animasi_hasil(self):

        self.output_hasil.configure(
            bg="#15233a"
        )

        self.root.after(
            120,
            lambda:
            self.output_hasil.configure(
                bg=INPUT_BG
            )
        )

        self.root.after(
            240,
            lambda:
            self.output_hasil.configure(
                bg="#15233a"
            )
        )

        self.root.after(
            360,
            lambda:
            self.output_hasil.configure(
                bg=INPUT_BG
            )
        )

    # ========================================================
    # OPERASI
    # ========================================================

    def operasi_tambah(self):

        try:

            A = self.ambil_matriks(
                self.entries_A
            )

            B = self.ambil_matriks(
                self.entries_B
            )

            hasil, langkah = tambah(
                A,
                B
            )

            self.tampilkan(
                "A + B",
                hasil,
                langkah
            )

            self.status(
                "✓ Penjumlahan berhasil"
            )

        except Exception as e:

            messagebox.showerror(
                "Kesalahan",
                str(e)
            )

    def operasi_kurang(self):

        try:

            A = self.ambil_matriks(
                self.entries_A
            )

            B = self.ambil_matriks(
                self.entries_B
            )

            hasil, langkah = kurang(
                A,
                B
            )

            self.tampilkan(
                "A − B",
                hasil,
                langkah
            )

            self.status(
                "✓ Pengurangan berhasil"
            )

        except Exception as e:

            messagebox.showerror(
                "Kesalahan",
                str(e)
            )

    def operasi_kali(self):

        try:

            A = self.ambil_matriks(
                self.entries_A
            )

            B = self.ambil_matriks(
                self.entries_B
            )

            hasil, langkah = kali(
                A,
                B
            )

            self.tampilkan(
                "A × B",
                hasil,
                langkah
            )

            self.status(
                "✓ Perkalian berhasil"
            )

        except Exception as e:

            messagebox.showerror(
                "Kesalahan",
                str(e)
            )

    def operasi_transpose(self):

        try:

            A = self.ambil_matriks(
                self.entries_A
            )

            hasil, langkah = transpose(
                A
            )

            self.tampilkan(
                "Transpose A",
                hasil,
                langkah
            )

            self.status(
                "✓ Transpose berhasil"
            )

        except Exception as e:

            messagebox.showerror(
                "Kesalahan",
                str(e)
            )

    def operasi_determinan(self):

        try:

            A = self.ambil_matriks(
                self.entries_A
            )

            hasil, langkah = determinan(
                A
            )

            self.tampilkan(
                "Determinan A",
                hasil,
                langkah
            )

            self.status(
                "✓ Determinan berhasil"
            )

        except Exception as e:

            messagebox.showerror(
                "Kesalahan",
                str(e)
            )

    def operasi_invers(self):

        try:

            A = self.ambil_matriks(
                self.entries_A
            )

            hasil, langkah = invers(
                A
            )

            self.tampilkan(
                "Invers A",
                hasil,
                langkah
            )

            self.status(
                "✓ Invers berhasil"
            )

        except Exception as e:

            messagebox.showerror(
                "Kesalahan",
                str(e)
            )

    # ========================================================
    # STATUS
    # ========================================================

    def status(
        self,
        teks
    ):

        if hasattr(
            self,
            "status_label"
        ):

            self.status_label.configure(
                text=teks
            )

        else:

            self.status_label = tk.Label(
                self.root,
                text=teks,
                bg=BG,
                fg=GREEN,
                font=(
                    "Segoe UI",
                    9
                )
            )

            self.status_label.place(
                x=30,
                y=748
            )

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        for baris in self.entries_A:

            for entry in baris:

                entry.delete(
                    0,
                    tk.END
                )

                entry.insert(
                    0,
                    "0"
                )

        for baris in self.entries_B:

            for entry in baris:

                entry.delete(
                    0,
                    tk.END
                )

                entry.insert(
                    0,
                    "0"
                )

        self.output_hasil.delete(
            "1.0",
            tk.END
        )

        self.output_langkah.delete(
            "1.0",
            tk.END
        )

        self.status(
            "↻ Matriks telah direset"
        )

    # ========================================================
    # SALIN HASIL
    # ========================================================

    def salin_hasil(self):

        hasil = self.output_hasil.get(
            "1.0",
            tk.END
        )

        if hasil.strip() == "":

            messagebox.showinfo(
                "Salin",
                "Belum ada hasil."
            )

            return

        self.root.clipboard_clear()

        self.root.clipboard_append(
            hasil
        )

        self.status(
            "✓ Hasil berhasil disalin"
        )


# ============================================================
# MENJALANKAN PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    aplikasi = KalkulatorMatriks(
        root
    )

    root.mainloop()
