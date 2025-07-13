import fitz  # PyMuPDF
import cv2
import pytesseract
import numpy as np

# Function to convert PDF pages to images and extract text
def pdf_to_images_and_ocr(pdf_path):
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Iterate over each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Convert PDF page to image (RGB mode)
            pix = page.get_pixmap()
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))

            # Convert image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            
            # Apply thresholding
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Apply noise removal
            denoised = cv2.fastNlMeansDenoising(thresh, h=30)
            
            # Correct skew
            coords = np.column_stack(np.where(thresh > 0))
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            (h, w) = img.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(denoised, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            
            # Perform OCR
            text = pytesseract.image_to_string(rotated)
            print(f"Extracted text from page {page_num + 1}:")
            print(text)

            # Optionally save preprocessed images for verification
            cv2.imwrite(f'preprocessed_page_{page_num + 1}.jpg', rotated)

        pdf_document.close()

    except Exception as e:
        print(f"Error processing PDF: {e}")

# Example usage
if __name__ == "__main__":
    pdf_path = r'C:\Users\praja\OneDrive\Desktop\OCRopenCV\ever.pdf'
    pdf_to_images_and_ocr(pdf_path)
