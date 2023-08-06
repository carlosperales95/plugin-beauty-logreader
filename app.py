from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
base_dir = os.path.dirname(__file__)


@app.route('/')
def index():
    data = parseData()
    df = pd.DataFrame(data)
    # df.set_index('timestamp', inplace=True)
    return render_template('index.html',
                        tables=[df.to_html(classes='data')])


@app.route('/upload', methods=('POST',))
def upload():
    files = request.files.getlist('files')
    for file in files:
        fn = secure_filename(file.filename)
        print(os.path.join(base_dir, '.imports/' + fn))
        file.save(os.path.join(base_dir, '.imports/' + fn))
    return 'ok'  # change to your own logic


def parseData():
    data = {
        'timestamp': [],
        'type': [],
        'content': [],
        'uid': []
    }

    f = open("info.log","r")
    lines = f.readlines()
    for line in lines:
        timestamp = line[:34]
        data['timestamp'].append(timestamp)

        logger_type_end = line[35:].find(':')
        logger_type = line[35 : 35 + logger_type_end]
        type = logger_type[logger_type.find('.') + 1 :]
        data['type'].append(type)

        uid_start = line.find('{"uid":"') + 8
        uid = line[uid_start : uid_start + 7]
        data['uid'].append(uid)

        content = line[36 + logger_type_end : uid_start]
        data['content'].append(content)

    return data

def sortDF(df):
    return df.sort_values(by=['timestamp'])

