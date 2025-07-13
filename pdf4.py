import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re

# Function to convert PDF pages to images and save them
def pdf_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_document = fitz.open(pdf_path)

    try:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()

            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
            image.save(image_path)
            print(f"Saved {image_path}")

    except Exception as e:
        print(f"Error processing page {page_num + 1}: {e}")

    finally:
        pdf_document.close()

# Function to extract text from images using OCR
def extract_text_from_images(image_folder):
    extracted_texts = []

    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)

            # Optionally preprocess image using OpenCV (if needed)
            processed_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(processed_image, lang='eng', config='--psm 6')

            # Clean up extracted text
            cleaned_text = clean_extracted_text(extracted_text)

            extracted_texts.append(cleaned_text.strip())

    return extracted_texts

# Function to clean up extracted text
def clean_extracted_text(text):
    cleaned_lines = []
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if line and not re.match(r'^\s*$', line):
            cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text

# Example usage
if __name__ == "__main__":
    pdf_path = r"C:\Users\praja\OneDrive\Desktop\OCRopenCV\ever.pdf"
    output_folder = r"C:\Users\praja\OneDrive\Desktop\OCRopenCV\images"
    pdf_to_images(pdf_path, output_folder)

    extracted_texts = extract_text_from_images(output_folder)

    for i, text in enumerate(extracted_texts):
        print(f"Extracted text from page {i + 1}:\n{text}")
