import cv2
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path based on your installation

# Function to perform OCR on an image file
def perform_ocr(image_path):
    # Read image using OpenCV
    image = cv2.imread(image_path)
    
    # Check if the image was successfully read
    if image is None:
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Preprocess the image (convert to grayscale, apply thresholding, etc. if needed)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(gray)

    return text

# Main function
if __name__ == '__main__':
    # Example usage: replace 'example.png' with your image file path
    image_path = r'C:\Users\praja\OneDrive\Desktop\OCRopenCV\Screenshot (1122).png'
    print(f"Reading image from: {image_path}")
    extracted_text = perform_ocr(image_path)
    
    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)
