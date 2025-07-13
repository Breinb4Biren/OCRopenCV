import cv2
import pytesseract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Download NLTK data for tokenization and stopwords (uncomment and run once if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    extracted_text = pytesseract.image_to_string(gray)

    return extracted_text

# Function to preprocess and analyze text
def process_text(text):
    # Tokenize text
    tokens = word_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words and word.isalnum()]

    # Stemming (optional)
    porter = PorterStemmer()
    stemmed_tokens = [porter.stem(word) for word in filtered_tokens]

    # Join tokens back into a clean text
    cleaned_text = ' '.join(stemmed_tokens)

    # Example: Print cleaned text
    print("Cleaned Text:")
    print(cleaned_text)

    # Example: Perform further analysis like NER or classification

# Main function
if __name__ == '__main__':
    # Example usage: replace 'WhatsApp Image 2024-02-20 at 14.01.17_e649e68f.jpg' with your image file path
    image_path = r'C:\Users\praja\OneDrive\Desktop\OCRopenCV\Screenshot (1122).png'
    print(f"Reading image from: {image_path}")
    extracted_text = perform_ocr(image_path)
    
    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)

    # Process and analyze the extracted text
    process_text(extracted_text)
