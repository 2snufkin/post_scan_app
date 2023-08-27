import datetime
import os
import string
from datetime import datetime
import random

from PyPDF2 import PdfReader, PdfWriter, PdfMerger


def generate_output_path(input_pdf_path, prefix="scanned"):
    """
    generate an output path, so it will be saved in the Documents folder
    :param input_pdf_path: the original path of the pdf
    :param prefix: to add
    :return: the path as string
    """
    base_filename = os.path.splitext(os.path.basename(input_pdf_path))[0]
    output_filename = f"{base_filename}_{prefix}_{datetime.now().strftime('%H-%M')}.pdf"

    documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')
    duplex_scan_folder = os.path.join(documents_folder, 'Duplex scan')

    # Create the 'Duplex scan' sub-folder if it doesn't exist
    if not os.path.exists(duplex_scan_folder):
        os.makedirs(duplex_scan_folder)

    output_path = os.path.join(duplex_scan_folder, output_filename)
    return output_path

def get_total_pages(pdf_path):
    pdf_reader = PdfReader(open(pdf_path, 'rb'))
    total_pages = len(pdf_reader.pages)
    pdf_reader.stream.close()
    return total_pages

def generate_random_string(length):
    """
    Generate a random string of specified length.
    :param length: The length of the random string.
    :return: The generated random string.
    """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def reverse_pdf_pages(pdf_path):
    """
    Reverse the order of pages in a PDF file and include a random string in the filename.
    :param pdf_path: The path of the PDF file.
    :return: The new reversed PDF filename.
    """
    pdf_reader = PdfReader(open(pdf_path, 'rb'))
    pdf_writer = PdfWriter()

    for page in reversed(range(len(pdf_reader.pages))):
        pdf_writer.add_page(pdf_reader.pages[page])

    # Generate a random string of 12 characters
    random_string = generate_random_string(12)
    reversed_pdf_filename = 'reversed_{}_{}.pdf'.format(os.path.splitext(os.path.basename(pdf_path))[0], random_string)

    with open(reversed_pdf_filename, 'wb') as f:
        pdf_writer.write(f)

    return reversed_pdf_filename

def close_pdf(pdf_path):
    """
    Close a PDF file using PyPDF2's PdfReader.
    :param pdf_path: The path of the PDF file to close.
    :return: True if the PDF was closed successfully, False otherwise.
    """
    try:
        pdf_reader = PdfReader(pdf_path)
        pdf_reader.stream.close()
        print(f"PDF '{pdf_path}' closed successfully.")
        return True
    except Exception as e:
        print(f"An error occurred while trying to close '{pdf_path}': {e}")
        return False
def remove_file(filename):
    """
    Remove a file and handle exceptions using try-catch.
    :param filename: The name of the file to remove.
    :return: True if the file was removed successfully, False otherwise.
    """
    try:
        os.remove(filename)
        print(f"File '{filename}' removed successfully.")
        return True
    except OSError as e:
        print(f"An error occurred while trying to remove '{filename}': {e}")
        return False


def organize_scan_pdf(odd_even_pdf_path):
    """
         takes the path of a PDF file containing odd pages and  even pages (for example if the pdf contains 14 pages,
         the first 7 are the odd and the rest is the even pages) ,
         and then returns a single PDF file with pages arranged in the order of odd-even pairs.
        :param odd_even_pdf_path: the pdf that contains all the odd + even pages
        :return: nothing
        """
    pdf_reader = PdfReader(open(odd_even_pdf_path, 'rb'))
    total_pages = len(pdf_reader.pages)

    # Reverse only the even pages
    reversed_even_pdf = reverse_pdf_pages(odd_even_pdf_path)
    reversed_even_pdf_reader = PdfReader(open(reversed_even_pdf, 'rb'))

    # Create a new PDF writer
    merged_pdf_writer = PdfWriter()

    # Iterate through odd and even pairs and combine them
    for i in range(total_pages // 2):
        merged_pdf_writer.add_page(pdf_reader.pages[i])  # Odd page
        merged_pdf_writer.add_page(reversed_even_pdf_reader.pages[i])  # Even page

    # If there are an odd number of total pages, add the last odd page
    if total_pages % 2 != 0:
        merged_pdf_writer.add_page(pdf_reader.pages[total_pages - 1])

    # Generate the output PDF path
    output_filename = generate_output_path(odd_even_pdf_path, prefix="scanned")

    # Save the merged PDF in the current directory
    with open(output_filename, 'wb') as output_file:
        merged_pdf_writer.write(output_file)

    print(f"Merged PDF saved as '{output_filename}'.")

    # Close the PDF readers
    pdf_reader.stream.close()
    reversed_even_pdf_reader.stream.close()

    # Remove the reversed even PDF file
    remove_file(reversed_even_pdf)


def merge_2_pdfs_after_scan(odd_pdf, even_pdf):
    """
    if you scan pages in two steps: 1 for the odd pages and the second for the even pages, use this method to create
    one pdf file out of this scan
    :param odd_pdf: the pdf that contains the first scan
    :param even_pdf: the pdf that contains the second scan
    :return: nothing
    """
    # Reverse the pages in even_pdf
    reversed_even_pdf = reverse_pdf_pages(even_pdf)

    # Merge the odd and reversed even pages into a new PDF
    odd_pdf_reader = PdfReader(open(odd_pdf, 'rb'))
    reversed_even_pdf_reader = PdfReader(open(reversed_even_pdf, 'rb'))

    new_pdf_writer = PdfWriter()
    for page in range(len(odd_pdf_reader.pages)):
        new_pdf_writer.add_page(odd_pdf_reader.pages[page])
        if page < len(reversed_even_pdf_reader.pages):
            new_pdf_writer.add_page(reversed_even_pdf_reader.pages[page])

    # Generate the output PDF path
    output_filename = generate_output_path(odd_pdf, prefix="scanned")

    with open(os.path.join(os.path.dirname(odd_pdf), output_filename), 'wb') as f:
        new_pdf_writer.write(f)
    reversed_even_pdf_reader.stream.close()
    # close_pdf(reversed_even_pdf)
    # Remove the reversed even PDF file
    remove_file(reversed_even_pdf)



def merge_pdfs(input_paths, output_path):
    """
    merge x pdf files into one pdf
    :param input_paths: the paths of the pdf you want to merge
    :param output_path: the output file you want to save the pdf
    :return: true if the operation was successful
    """
    merger = PdfMerger()

    # Iterate through each input PDF file
    for path in input_paths:
        # Open the PDF file in read-binary mode
        with open(path, 'rb') as file:
            merger.append(file)

    # Write the merged PDF to the output file
    with open(output_path, 'wb') as output_file:
        merger.write(output_file)

    print("PDFs merged successfully!")
    return True
