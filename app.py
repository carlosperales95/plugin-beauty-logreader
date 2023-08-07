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
    filterTypeDF(df, ['INFO'])
    # df = filterUIDDF(df, "942c7e3")
    # df = filterContent(df, "XNT6LGX5PV5X8N82")
    # df = filterDate(df, "2023-08-03T11:30:03", "2023-08-03T11:50:03")

    return render_template('index.html',
                        column_names=df.columns.values, row_data=list(df.values.tolist()),
                        zip=zip, link_column="content")


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
        timestamp = timestamp[timestamp.find('[') + 1 : timestamp.find(']')]
        data['timestamp'].append(timestamp)

        logger_type_end = line[35:].find(':')
        logger_type = line[35 : 35 + logger_type_end]
        type = logger_type[logger_type.find('.') + 1 :]
        data['type'].append(type)

        uid_start = line.find('{"uid":"') + 8
        uid = line[uid_start : uid_start + 7]
        data['uid'].append(uid)

        content = line[36 + logger_type_end : uid_start - 8]
        data['content'].append(content)

    return data

def sortDF(df):
    return df.sort_values(by=['timestamp'])

def filterTypeDF(df, types):
    return df[df['type'].isin(types)]


def filterUIDDF(df, value):
    return df[df['uid'].str.contains(value)]

def filterContent(df, value):
    return df[df['content'].str.contains(value)]

def filterDate (df, start_date, end_date):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    mask = (df['timestamp'] > start_date) & (df['timestamp'] <= end_date)
    print(df.loc[mask])

    return df.loc[mask]
