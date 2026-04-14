from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pdfplumber
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Home route
@app.route('/')
def home():
    return "Server is working"

# 🔍 OCR using OCR.space API
def extract_text_from_image(file):
    try:
        url = "https://api.ocr.space/parse/image"
        files = {"file": file}
        data = {
            "apikey": "helloworld",  # Free demo key (limited usage)
            "language": "eng"
        }

        response = requests.post(url, files=files, data=data)
        result = response.json()

        if result.get("IsErroredOnProcessing"):
            return ""

        return result["ParsedResults"][0]["ParsedText"]

    except Exception as e:
        return ""

# 📄 Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        return ""
    return text

# 🚀 Main API
@app.route('/find', methods=['POST'])
def find_room():
    try:
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
    app.run(host='0.0.0.0', port=5000)
