import fitz  # PyMuPDF
import sys
import os
import argparse

def convert_pdf_to_png(pdf_path, output_dir=None, dpi=300):
    """
    Convert each page of a PDF file to a PNG image.
    
    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str, optional): Directory to save the generated PNGs. Defaults to a subfolder named after the PDF.
        dpi (int, optional): Dots per inch for the output images. Defaults to 300 (Standard High Quality).
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
        
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    if output_dir is None:
        # Default to a subfolder named after the PDF in the same directory
        output_dir = os.path.join(os.path.dirname(os.path.abspath(pdf_path)), base_name)
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        doc = fitz.open(pdf_path)
        print(f"Processing '{pdf_path}' with {len(doc)} pages...")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=dpi)
            
            output_filename = f"{base_name}_page_{page_num + 1:03d}.png"
            output_filepath = os.path.join(output_dir, output_filename)
            
            pix.save(output_filepath)
            print(f"Saved: {output_filepath}")
            
        print("Done!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF pages to PNG images.")
    parser.add_argument("pdf_path", help="Path to the source PDF file")
    parser.add_argument("-o", "--output-dir", help="Directory to save the PNG images (default: a subfolder named after the PDF)", default=None)
    parser.add_argument("--dpi", help="DPI for the output images (default: 300)", type=int, default=300)
    
    args = parser.parse_args()
    convert_pdf_to_png(args.pdf_path, args.output_dir, args.dpi)
