---
name: Convert PDF to PNG
description: A skill to convert each page of a PDF file into a separate PNG image using PyMuPDF.
---

# Convert PDF to PNG Skill

This skill allows the agent to convert a given PDF file into a sequence of PNG images, one for each page.

## Prerequisites

Before using this script, ensure you have installed the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

The main capability is provided through a Python script located at `scripts/convert_pdf_to_png.py`. 

### Running the script

You can execute the script using the Python interpreter. The script takes the path to the PDF file as a required argument.

```bash
python scripts/convert_pdf_to_png.py /path/to/your/file.pdf
```

### Options

* **`pdf_path`** (Required): The absolute path to the PDF file you wish to convert.
* **`-o, --output-dir`** (Optional): The directory where the PNG images will be saved. If not provided, it defaults to creating a new subfolder (named after the PDF file) in the same directory as the original PDF file.
* **`--dpi`** (Optional): The DPI (Dots Per Inch) for the output images. Higher DPI means better resolution but larger file size. The default is 300 (Standard High Quality, balances clarity and file size).

### Example Commands

1. **Basic Usage (outputs to a new `sample` subfolder in the Documents directory)**
   ```bash
   python scripts/convert_pdf_to_png.py /Users/kory/Documents/sample.pdf
   ```

2. **Specify Output Directory**
   ```bash
   python scripts/convert_pdf_to_png.py /Users/kory/Documents/sample.pdf -o /Users/kory/Documents/output_images
   ```

3. **Specify Output Directory and DPI**
   ```bash
   python scripts/convert_pdf_to_png.py /Users/kory/Documents/sample.pdf -o /Users/kory/Documents/output_images --dpi 600
   ```

## Output Format

The script processes the PDF and saves the images with the naming convention:
`[original_pdf_name]_page_[page_number].png`
(e.g., `sample_page_001.png`, `sample_page_002.png`).
