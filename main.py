from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Image Processing API! Use the /process-image endpoint."

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        data = request.json
        base_image_url = data['base_image_url']
        overlay_image_url = data['overlay_image_url']
        text_to_add = data['text_to_add']

        response = requests.get(base_image_url)
        base_image = Image.open(BytesIO(response.content))

        response = requests.get(overlay_image_url)
        overlay = Image.open(BytesIO(response.content))

        overlay = overlay.resize(base_image.size, Image.ANTIALIAS)
        base_image.paste(overlay, (0, 0), overlay)

        draw = ImageDraw.Draw(base_image)
        font = ImageFont.load_default()
        draw.text((50, 50), text_to_add, fill="white")

        output = BytesIO()
        base_image.save(output, format='PNG')
        output.seek(0)

        return send_file(output, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
