import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox

from scan_tools import organize_scan_pdf, merge_2_pdfs_after_scan, get_total_pages

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Arranger")
        self.root.configure(bg="white")  # Set background color to white


        # Calculate screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the center position for the window
        window_width = screen_width // 3
        window_height = screen_height // 3
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.radio_var = tk.StringVar()
        self.radio_var.set("one_file")

        # Add header label
        self.header_label = tk.Label(root, text="PDF Arranger", font=("Helvetica", 16), bg="white")
        self.header_label.pack(pady=10)

        # Add user message and input for number of pages
        self.user_message = tk.Label(root, text="Please enter the number of pages you scanned:", bg="white")
        self.user_message.pack()
        self.num_pages_entry = tk.Entry(root)
        self.num_pages_entry.pack(pady=5)

        self.radio_var = tk.StringVar()
        self.radio_var.set("one_file")

        self.radio_frame = tk.Frame(root, bg="white")  # Set background color of the frame
        self.one_file_radio = tk.Radiobutton(self.radio_frame, text="One File", variable=self.radio_var,
                                             value="one_file", bg="white")  # Set background color of the radio button
        self.two_files_radio = tk.Radiobutton(self.radio_frame, text="Two Files", variable=self.radio_var,
                                              value="two_files", bg="white")

        self.radio_frame.pack()
        self.one_file_radio.pack(side="left", padx=10, pady=10)  # Adding some padding
        self.two_files_radio.pack(side="left", padx=10, pady=10)

        self.button_frame = tk.Frame(root, bg="white")  # Set background color of the frame
        self.select_button = tk.Button(self.button_frame, text="Select File(s)", command=self.select_files,
                                       bg="pink", fg="black")  # Set button colors
        self.arrange_button = tk.Button(self.button_frame, text="Arrange", command=self.arrange,
                                        bg="lightblue", fg="black")

        self.button_frame.pack()
        self.select_button.pack(side="left", padx=10, pady=10)  # Adding some padding
        self.arrange_button.pack(side="left", padx=10, pady=10)

    def select_files(self):
        if self.radio_var.get() == "one_file":
            self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        else:
            self.odd_pages_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            self.even_pages_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    def arrange(self):
        error_message= "Number of scanned pages does not match the total number of pages. Not all pages have been scanned"
        try:
            num_pages = int(self.num_pages_entry.get())
            if self.radio_var.get() == "one_file":
                if num_pages == get_total_pages(self.file_path):
                    organize_scan_pdf(self.file_path)
                    messagebox.showinfo("Success", "PDF arranged.")
                else:
                    messagebox.showerror("Error", error_message)
            else:
                if num_pages == get_total_pages(self.odd_pages_path) + self.get_total_pages(self.even_pages_path):
                    merge_2_pdfs_after_scan(self.odd_pages_path, self.even_pages_path)
                    messagebox.showinfo("Success", "PDFs arranged.")
                else:
                    messagebox.showerror("Error", error_message)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of pages.")






if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()