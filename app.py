from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os

app = Flask(__name__)

# Ensure uploads directory exists
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def get_top_colors(image_path, n_colors=10):
    img = Image.open(image_path)
    img = img.resize((img.width // 5, img.height // 5))  # Resize to speed up processing
    img = img.convert('RGB')  # Convert image to RGB

    pixels = np.array(img).reshape(-1, 3)  # Flatten the image to a list of RGB values

    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(pixels)

    # Get the most common colors
    colors = kmeans.cluster_centers_
    colors = colors.round(0).astype(int)
    hex_colors = [rgb_to_hex(color) for color in colors]

    return hex_colors


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Get the top 10 colors
    top_colors = get_top_colors(filepath)

    return jsonify({'colors': top_colors, 'image_url': f'/uploads/{file.filename}'})


if __name__ == '__main__':
    app.run(debug=True)
