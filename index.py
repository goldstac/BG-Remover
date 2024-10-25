from flask import Flask, render_template_string, request, send_file
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML template for the UI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Background Remover</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        input[type="file"] {
            margin: 10px 0;
        }
        input[type="submit"] {
            background-color: #007BFF;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Background Remover</h1>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" accept=".jpg,.jpeg,.png" required><br>
            <input type="submit" value="Remove Background">
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_image():
    uploaded_file = request.files['file']
    
    if uploaded_file and uploaded_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(image_path)
        
        # Remove background
        input_image = Image.open(image_path)
        output_image = remove(input_image)

        # Save the result as PNG to preserve transparency
        output_path = os.path.join(UPLOAD_FOLDER, f"no_bg_{uploaded_file.filename.split('.')[0]}.png")
        output_image.save(output_path, format='PNG')
        
        return send_file(output_path, as_attachment=True)
    else:
        return "Unsupported file format. Please upload a .jpg, .jpeg, or .png file."

if __name__ == '__main__':
    app.run(debug=True)
