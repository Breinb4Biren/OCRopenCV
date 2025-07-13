import fitz  # PyMuPDF
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def perform_ocr(pdf_path):
    print(f"Performing OCR on PDF: {pdf_path}")
    
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return ""

    extracted_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        try:
            # Extract text directly from the page
            text = page.get_text()
            if text.strip():  # Check if extracted text is not empty
                extracted_text += text + "\n\n"
                print(f"Extracted text from page {page_num + 1}:")
                print(text)
            else:
                print(f"No text found on page {page_num + 1}. Attempting OCR on images...")
                pix = page.get_pixmap()
                
                # Convert the pixmap to a numpy array
                img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                if img_data is None or img_data.size == 0:
                    print(f"Failed to decode image for page {page_num + 1}. Skipping...")
                    continue
                
                if pix.n == 4:
                    img = cv2.cvtColor(img_data, cv2.COLOR_BGRA2BGR)
                else:
                    img = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)

                # Perform OCR using pytesseract
                text_from_image = pytesseract.image_to_string(img)
                
                if text_from_image.strip():
                    extracted_text += text_from_image + "\n\n"
                    print(f"Extracted text from image on page {page_num + 1}:")
                    print(text_from_image)
                else:
                    print(f"No text extracted from image on page {page_num + 1}")
                
        except Exception as e:
            print(f"Error processing page {page_num + 1}: {e}")
            continue

    print("OCR extraction completed.")
    return extracted_text.strip()

if __name__ == '__main__':
    #pdf_path = r'C:\Users\praja\OneDrive\Desktop\OCRopenCV\ever.pdf'
    pdf_path = r'C:\Users\praja\OneDrive\Desktop\OCRopenCV\Resume.pdf'
    print(f"Reading PDF from: {pdf_path}")
    
    extracted_text = perform_ocr(pdf_path)

    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)
