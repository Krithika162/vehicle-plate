from flask import Flask, request, jsonify
import cv2
import numpy as np
import pytesseract
import os

app = Flask(__name__)

# Configure pytesseract (Render uses Linux)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route('/readnumberplate', methods=['POST'])
def read_number_plate():
    if 'imageFile' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['imageFile']
    image_np = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Optional: thresholding or noise removal
    text = pytesseract.image_to_string(gray)

    return jsonify({"number_plate": text.strip()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
