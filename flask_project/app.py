from flask import Flask, render_template, request
import os
import cv2
import pytesseract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Download NLTK data for tokenization and stopwords (uncomment and run once if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

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

    return cleaned_text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        file = request.files['file']

        # If the user does not select a file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('index.html', message='No selected file')

        if file:
            # Save the uploaded file
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Perform OCR
            extracted_text = perform_ocr(file_path)

            # Process extracted text
            cleaned_text = process_text(extracted_text)

            # Render result template with extracted and cleaned text
            return render_template('result.html', filename=filename, extracted_text=extracted_text, cleaned_text=cleaned_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
