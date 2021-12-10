from flask import Flask, request, redirect, render_template
import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src", "models")) # :(

from PIL import Image
from predict import Classifier  # :(

app = Flask(__name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'png'}

app.config['UPLOAD_FOLDER'] = "./app/static/user_images/"

if not os.path.isdir(app.config['UPLOAD_FOLDER']):
	os.mkdir(app.config['UPLOAD_FOLDER'])

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files: # no file part
		return redirect(request.url)

	file = request.files['file']

	if file.filename == "": # no image for uploading
		return redirect(request.url)

	if file and allowed_file(file.filename):
		filename = file.filename
		path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(path_to_save)
		winner_color = Classifier().predict(Image.open(path_to_save))
		return render_template('prediction.html', path_to_image=os.path.join("user_images", filename), winner_color=winner_color)
	
	else: # not allowed format
		return redirect(request.url)
