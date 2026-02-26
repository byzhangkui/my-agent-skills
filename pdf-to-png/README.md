# Convert PDF to PNG

A Python-based utility to convert each page of a PDF document into a separate high-resolution PNG image.

This project is also designed as an AI Agent Skill (`SKILL.md`), allowing automated systems to process PDFs.

## Prerequisites

Before running the script, make sure you have Python installed and the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This project depends on the `PyMuPDF` library for fast and reliable PDF processing.

## Usage

The main capability is provided through the command-line interface of the `scripts/convert_pdf_to_png.py` script.

### Basic Usage

To convert a PDF with the default settings (outputting to a new subfolder named after the PDF, at 300 DPI for high quality sharing):

```bash
python scripts/convert_pdf_to_png.py /path/to/your/document.pdf
```

### Options

* **`pdf_path`** (Required): The absolute or relative path to the PDF file you wish to convert.
   * **`-o, --output-dir`** (Optional): The directory where the PNG images will be saved. If not provided, it defaults to creating a new subfolder (named after the PDF file) in the same directory as the original PDF file.
* **`--dpi`** (Optional): The DPI (Dots Per Inch) for the output images. Higher DPI means better resolution but larger file size. The default is **300** (Standard High Quality). Using higher values like 600 or 1200 will result in significantly larger file sizes.

### Advanced Examples

**1. Output to a specific folder**
```bash
python scripts/convert_pdf_to_png.py input.pdf -o ./output_images
```

**2. Convert at a higher resolution for print/maximum clarity (e.g., 600 or 1200 DPI)**
```bash
python scripts/convert_pdf_to_png.py input.pdf --dpi 600
```

## Output Format

The script processes the PDF and saves the images with the naming convention:
`[original_pdf_name]_page_[page_number].png`
(e.g., `document_page_001.png`, `document_page_002.png`).
