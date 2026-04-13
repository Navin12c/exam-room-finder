from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import pdfplumber
import io

# If using Windows, set this path (IMPORTANT)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Home route (test server)
@app.route('/')
def home():
    return "Server is working"

# Function: Extract text from image
def extract_text_from_image(file):
    try:
        image = Image.open(file).convert("RGB")
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return ""

# Function: Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return ""
    return text

# Main API
@app.route('/find', methods=['POST'])
def find_room():
    try:
        # Get file and roll number
        file = request.files.get('file')
        roll = request.form.get('roll')

        if not file or not roll:
            return jsonify({"result": "❗ File or roll number missing"})

        # Extract text
        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file)
        else:
            text = extract_text_from_image(file)

        if not text:
            return jsonify({"result": "❗ Could not read file"})

        # Search roll number
        for line in text.split("\n"):
            if roll.strip() in line:
                return jsonify({"result": f"✅ Found: {line}"})

        return jsonify({"result": "❌ Roll number not found"})

    except Exception as e:
        return jsonify({"result": f"❌ Error: {str(e)}"})

# Run server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)