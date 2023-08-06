from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
base_dir = os.path.dirname(__file__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=('POST',))
def upload():
    files = request.files.getlist('files')
    for file in files:
        fn = secure_filename(file.filename)
        print(os.path.join(base_dir, '.imports/' + fn))
        file.save(os.path.join(base_dir, '.imports/' + fn))
    return 'ok'  # change to your own logic