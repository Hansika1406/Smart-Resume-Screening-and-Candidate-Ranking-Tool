import fitz
import pdfplumber
import pytesseract
import re

from pdf2image import convert_from_path


# -----------------------------
# Tesseract Location
# -----------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

POPPLER_PATH = r"C:\poppler\Library\bin"
# -----------------------------
# Extract using PyMuPDF
# -----------------------------

def extract_pymupdf(pdf_path):

    text = ""

    try:

        doc = fitz.open(pdf_path)

        for page in doc:

            text += page.get_text()

        doc.close()

    except:

        text = ""

    return text
# -----------------------------
# Extract using pdfplumber
# -----------------------------

def extract_pdfplumber(pdf_path):

    text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

    except:

        text = ""

    return text
# -----------------------------
# Extract using OCR
# -----------------------------

def extract_ocr(pdf_path):

    text = ""

    try:

        images = convert_from_path(
            pdf_path,
            poppler_path=POPPLER_PATH
        )

        for image in images:

            text += pytesseract.image_to_string(image)

    except:

        text = ""

    return text
# -----------------------------
# Clean Resume Text
# -----------------------------

def clean_text(text):

    text = re.sub(r"\(cid:\d+\)", " ", text)

    text = re.sub(r"[•●▪■►◆★]", " ", text)

    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()
# -----------------------------
# Main Resume Parser
# -----------------------------

def extract_resume_text(pdf_path):

    # First Try PyMuPDF

    text = extract_pymupdf(pdf_path)

    if len(text.strip()) > 200:

        return clean_text(text)

    # Second Try pdfplumber

    text = extract_pdfplumber(pdf_path)

    if len(text.strip()) > 200:

        return clean_text(text)

    # Last Try OCR

    text = extract_ocr(pdf_path)

    return clean_text(text)
