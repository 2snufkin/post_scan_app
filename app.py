import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog, ttk
import os

from scan_tools import organize_scan_pdf, merge_2_pdfs_after_scan, get_total_pages


class ModernPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplex Scanner Organizer")
        self.root.configure(bg="#f5f5f5")

        # Configure modern styling
        self.setup_styles()

        # Calculate screen dimensions for responsive design
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Make window larger and more modern
        window_width = min(600, screen_width // 2)
        window_height = min(700, screen_height // 2)
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.resizable(True, True)

        # Initialize variables
        self.radio_var = tk.StringVar(value="one_file")
        self.file_path = ""
        self.odd_pages_path = ""
        self.even_pages_path = ""

        self.create_modern_ui()

    def setup_styles(self):
        """Configure modern styling for ttk widgets"""
        style = ttk.Style()
        style.theme_use("clam")

        # Define consistent color scheme
        bg_color = "white"  # Light gray background
        text_color = "#2c3e50"  # Dark blue-gray text
        accent_color = "#3498db"  # Blue accent

        # Configure custom styles with consistent background
        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold"),
            background=bg_color,
            foreground=text_color,
        )
        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
            background=bg_color,
            foreground=text_color,
        )
        style.configure(
            "Instruction.TLabel",
            font=("Segoe UI", 10),
            background=bg_color,
            foreground="#555555",
        )
        style.configure(
            "Modern.TRadiobutton",
            font=("Segoe UI", 11),
            background=bg_color,
            foreground=text_color,
        )
        style.configure(
            "Action.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 10),
            background=accent_color,
            foreground="white",
        )

        # Configure button hover effects
        style.map(
            "Action.TButton",
            background=[("active", "#2980b9"), ("!active", accent_color)],
            foreground=[("active", "white"), ("!active", "white")],
            relief=[("pressed", "flat"), ("!pressed", "raised")],
        )

        # Configure frame backgrounds
        style.configure("TFrame", background=bg_color)
        style.configure("TLabelFrame", background=bg_color)
        style.configure("TLabelFrame.Label", background=bg_color, foreground=text_color)

    def create_modern_ui(self):
        """Create the modern user interface"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header section
        self.create_header(main_frame)

        # Instructions section
        self.create_instructions(main_frame)

        # Page count section
        self.create_page_count_section(main_frame)

        # Scanning mode selection
        self.create_mode_selection(main_frame)

        # File selection section
        self.create_file_selection(main_frame)

        # Action buttons
        self.create_action_buttons(main_frame)

        # Status section
        self.create_status_section(main_frame)

    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = ttk.Label(
            header_frame, text="📄 Duplex Scanner Organizer", style="Title.TLabel"
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame,
            text="Organize your scanned documents with ease",
            style="Subtitle.TLabel",
        )
        subtitle_label.pack(pady=(5, 0))

    def create_instructions(self, parent):
        """Create the instructions section"""
        instructions_frame = ttk.LabelFrame(parent, text="How it works", padding="15")
        instructions_frame.pack(fill=tk.X, pady=(0, 20))

        instructions_text = """This tool helps you organize PDFs from duplex (double-sided) scanning:

• ONE FILE: Choose this if you scanned all pages into a single PDF
  (First half = odd pages, Second half = even pages)

• TWO FILES: Choose this if you scanned odd and even pages separately
  (One PDF with odd pages, another PDF with even pages)

The tool will automatically arrange pages in the correct order and save 
the result to your Documents/Duplex scan folder."""

        instruction_label = ttk.Label(
            instructions_frame,
            text=instructions_text,
            style="Instruction.TLabel",
            justify=tk.LEFT,
        )
        instruction_label.pack(anchor=tk.W)

    def create_page_count_section(self, parent):
        """Create the page count input section"""
        page_frame = ttk.LabelFrame(parent, text="Document Information", padding="15")
        page_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(
            page_frame,
            text="Total number of pages in your document:",
            style="Instruction.TLabel",
        ).pack(anchor=tk.W)

        self.num_pages_entry = ttk.Entry(page_frame, font=("Segoe UI", 12), width=10)
        self.num_pages_entry.pack(anchor=tk.W, pady=(5, 0))

    def create_mode_selection(self, parent):
        """Create the scanning mode selection"""
        mode_frame = ttk.LabelFrame(parent, text="Scanning Mode", padding="15")
        mode_frame.pack(fill=tk.X, pady=(0, 20))

        # One file option
        one_file_frame = ttk.Frame(mode_frame)
        one_file_frame.pack(fill=tk.X, pady=(0, 10))

        self.one_file_radio = ttk.Radiobutton(
            one_file_frame,
            text="📄 One File",
            variable=self.radio_var,
            value="one_file",
            style="Modern.TRadiobutton",
            command=self.on_mode_change,
        )
        self.one_file_radio.pack(anchor=tk.W)

        one_file_desc = ttk.Label(
            one_file_frame,
            text="   All pages scanned into a single PDF file",
            style="Instruction.TLabel",
        )
        one_file_desc.pack(anchor=tk.W)

        # Two files option
        two_files_frame = ttk.Frame(mode_frame)
        two_files_frame.pack(fill=tk.X)

        self.two_files_radio = ttk.Radiobutton(
            two_files_frame,
            text="📄📄 Two Files",
            variable=self.radio_var,
            value="two_files",
            style="Modern.TRadiobutton",
            command=self.on_mode_change,
        )
        self.two_files_radio.pack(anchor=tk.W)

        two_files_desc = ttk.Label(
            two_files_frame,
            text="   Odd and even pages scanned into separate PDF files",
            style="Instruction.TLabel",
        )
        two_files_desc.pack(anchor=tk.W)

    def create_file_selection(self, parent):
        """Create the file selection section"""
        self.file_frame = ttk.LabelFrame(parent, text="File Selection", padding="15")
        self.file_frame.pack(fill=tk.X, pady=(0, 20))

        # Dynamic content based on mode
        self.update_file_selection_ui()

    def create_action_buttons(self, parent):
        """Create the action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        # Select files button
        self.select_button = ttk.Button(
            button_frame,
            text="📁 Select File(s)",
            command=self.select_files,
            style="Action.TButton",
        )
        self.select_button.pack(side=tk.LEFT, padx=(0, 10))

        # Process button
        self.process_button = ttk.Button(
            button_frame,
            text="⚡ Organize PDF",
            command=self.arrange,
            style="Action.TButton",
        )
        self.process_button.pack(side=tk.LEFT, padx=10, pady=10)  
        self.process_button.pack(side=tk.LEFT)

    def create_status_section(self, parent):
        """Create the status section"""
        self.status_frame = ttk.Frame(parent)
        self.status_frame.pack(fill=tk.X)

        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready to organize your PDFs",
            style="Instruction.TLabel",
        )
        self.status_label.pack()

    def on_mode_change(self):
        """Handle mode change"""
        self.update_file_selection_ui()
        self.update_status("Mode changed. Please select your file(s).")

    def update_file_selection_ui(self):
        """Update the file selection UI based on selected mode"""
        # Clear existing widgets
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        if self.radio_var.get() == "one_file":
            ttk.Label(
                self.file_frame,
                text="Select your scanned PDF file:",
                style="Instruction.TLabel",
            ).pack(anchor=tk.W)
            self.file_display = ttk.Label(
                self.file_frame, text="No file selected", foreground="#e74c3c"
            )
            self.file_display.pack(anchor=tk.W, pady=(5, 0))
        else:
            ttk.Label(
                self.file_frame,
                text="Select your PDF files:",
                style="Instruction.TLabel",
            ).pack(anchor=tk.W)

            ttk.Label(
                self.file_frame, text="Odd pages file:", style="Instruction.TLabel"
            ).pack(anchor=tk.W, pady=(10, 0))
            self.odd_file_display = ttk.Label(
                self.file_frame, text="No file selected", foreground="#e74c3c"
            )
            self.odd_file_display.pack(anchor=tk.W, pady=(2, 0))

            ttk.Label(
                self.file_frame, text="Even pages file:", style="Instruction.TLabel"
            ).pack(anchor=tk.W, pady=(10, 0))
            self.even_file_display = ttk.Label(
                self.file_frame, text="No file selected", foreground="#e74c3c"
            )
            self.even_file_display.pack(anchor=tk.W, pady=(2, 0))

    def update_status(self, message, color="#7f8c8d"):
        """Update the status message"""
        self.status_label.config(text=message, foreground=color)

    def select_files(self):
        """Handle file selection"""
        try:
            if self.radio_var.get() == "one_file":
                self.file_path = filedialog.askopenfilename(
                    title="Select PDF file with all pages",
                    filetypes=[("PDF files", "*.pdf")],
                    initialdir=os.path.expanduser("~"),
                )
                if self.file_path:
                    filename = os.path.basename(self.file_path)
                    self.file_display.config(text=f"✓ {filename}", foreground="#27ae60")
                    self.update_status(f"Selected: {filename}", "#27ae60")
                else:
                    self.update_status("No file selected", "#e74c3c")
            else:
                # Select odd pages file
                self.odd_pages_path = filedialog.askopenfilename(
                    title="Select PDF file with ODD pages (1, 3, 5, ...)",
                    filetypes=[("PDF files", "*.pdf")],
                    initialdir=os.path.expanduser("~"),
                )
                if self.odd_pages_path:
                    odd_filename = os.path.basename(self.odd_pages_path)
                    self.odd_file_display.config(
                        text=f"✓ {odd_filename}", foreground="#27ae60"
                    )

                    # Select even pages file
                    self.even_pages_path = filedialog.askopenfilename(
                        title="Select PDF file with EVEN pages (2, 4, 6, ...)",
                        filetypes=[("PDF files", "*.pdf")],
                        initialdir=os.path.dirname(self.odd_pages_path),
                    )
                    if self.even_pages_path:
                        even_filename = os.path.basename(self.even_pages_path)
                        self.even_file_display.config(
                            text=f"✓ {even_filename}", foreground="#27ae60"
                        )
                        self.update_status(
                            "Both files selected successfully", "#27ae60"
                        )
                    else:
                        self.update_status(
                            "Please select the even pages file", "#e74c3c"
                        )
                else:
                    self.update_status("No files selected", "#e74c3c")
        except Exception as e:
            self.update_status(f"Error selecting files: {str(e)}", "#e74c3c")

    def arrange(self):
        """Process and arrange the PDF files"""
        try:
            # Validate page count input
            if not self.num_pages_entry.get().strip():
                messagebox.showerror(
                    "Input Error", "Please enter the total number of pages."
                )
                return

            try:
                num_pages = int(self.num_pages_entry.get())
                if num_pages <= 0:
                    raise ValueError("Page count must be positive")
            except ValueError:
                messagebox.showerror(
                    "Input Error", "Please enter a valid positive number for pages."
                )
                return

            self.update_status("Processing PDF...", "#f39c12")
            self.root.update()

            error_message = (
                "The number of pages you entered doesn't match the total pages in your PDF(s). "
                "Please check that all pages were scanned correctly."
            )

            if self.radio_var.get() == "one_file":
                if not self.file_path:
                    messagebox.showerror(
                        "File Error", "Please select a PDF file first."
                    )
                    return

                if not os.path.exists(self.file_path):
                    messagebox.showerror(
                        "File Error", "The selected file no longer exists."
                    )
                    return

                actual_pages = get_total_pages(self.file_path)
                if num_pages == actual_pages:
                    organize_scan_pdf(self.file_path)
                    self.update_status("✓ PDF organized successfully!", "#27ae60")
                    messagebox.showinfo(
                        "Success",
                        f"Your PDF has been organized successfully!\n\n"
                        f"The organized file has been saved to:\n"
                        f"Documents/Duplex scan/",
                    )
                else:
                    self.update_status("Error: Page count mismatch", "#e74c3c")
                    messagebox.showerror(
                        "Page Count Error",
                        f"{error_message}\n\n"
                        f"Expected: {num_pages} pages\n"
                        f"Found: {actual_pages} pages",
                    )
            else:
                if not self.odd_pages_path or not self.even_pages_path:
                    messagebox.showerror(
                        "File Error", "Please select both odd and even pages PDF files."
                    )
                    return

                if not os.path.exists(self.odd_pages_path) or not os.path.exists(
                    self.even_pages_path
                ):
                    messagebox.showerror(
                        "File Error", "One or both selected files no longer exist."
                    )
                    return

                odd_total = get_total_pages(self.odd_pages_path)
                even_total = get_total_pages(self.even_pages_path)

                if num_pages == odd_total == even_total:
                    merge_2_pdfs_after_scan(self.odd_pages_path, self.even_pages_path)
                    self.update_status("✓ PDFs merged successfully!", "#27ae60")
                    messagebox.showinfo(
                        "Success",
                        f"Your PDFs have been merged successfully!\n\n"
                        f"The organized file has been saved to:\n"
                        f"Documents/Duplex scan/",
                    )
                else:
                    self.update_status("Error: Page count mismatch", "#e74c3c")
                    messagebox.showerror(
                        "Page Count Error",
                        f"{error_message}\n\n"
                        f"Expected: {num_pages} pages each\n"
                        f"Odd pages file: {odd_total} pages\n"
                        f"Even pages file: {even_total} pages",
                    )

        except Exception as e:
            self.update_status(f"Error: {str(e)}", "#e74c3c")
            messagebox.showerror(
                "Processing Error",
                f"An error occurred while processing your PDF:\n\n{str(e)}",
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernPDFApp(root)
    root.mainloop()
