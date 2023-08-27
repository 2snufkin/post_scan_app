# pdf_app.py

import tkinter as tk
from tkinter import filedialog
from scan_tools import organize_scan_pdf, merge_2_pdfs_after_scan


class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Arranger")

        self.radio_var = tk.StringVar()
        self.radio_var.set("one_file")

        self.radio_frame = tk.Frame(root)
        self.one_file_radio = tk.Radiobutton(self.radio_frame, text="One File", variable=self.radio_var,
                                             value="one_file")
        self.two_files_radio = tk.Radiobutton(self.radio_frame, text="Two Files", variable=self.radio_var,
                                              value="two_files")

        self.radio_frame.pack()
        self.one_file_radio.pack(side="left")
        self.two_files_radio.pack(side="left")

        self.button_frame = tk.Frame(root)
        self.select_button = tk.Button(self.button_frame, text="Select File(s)", command=self.select_files)
        self.arrange_button = tk.Button(self.button_frame, text="Arrange", command=self.arrange)

        self.button_frame.pack()
        self.select_button.pack(side="left")
        self.arrange_button.pack(side="left")

    def select_files(self):
        if self.radio_var.get() == "one_file":
            self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        else:
            self.odd_pages_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            self.even_pages_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    def arrange(self):
        if self.radio_var.get() == "one_file":
            organize_scan_pdf(self.file_path)
            print("PDF arranged.")
        else:
            merge_2_pdfs_after_scan(self.odd_pages_path, self.even_pages_path)
            print("PDFs arranged.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()
