from flask import Flask, request, jsonify
import easyocr
import numpy as np
import cv2
from PIL import Image
import io

app = Flask(__name__)
reader = easyocr.Reader(['en'])

@app.route('/readnumberplate', methods=['POST'])
def read_number_plate():
    if 'imageFile' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['imageFile']
    image_bytes = file.read()
    npimg = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = reader.readtext(img)
    if results:
        plate_text = max(results, key=lambda x: x[2])[1]  # most confident result
    else:
        plate_text = "Not detected"

    return jsonify({
        "number_plate": plate_text,
        "status": "success"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
