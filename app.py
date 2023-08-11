from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import pandas as pd
import uuid
from dateutil.parser import parse
import datetime

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
cases_path = 'cases'

data = {
    'timestamp': [],
    'type': [],
    'content': [],
    'uid': []
}

df_filters = {
    'date': [],
    'type': [],
    'find': [],
    'uid': []
}

df = pd.DataFrame()
filtered_df = pd.DataFrame()

show_upload = True

# Filters done, only need to add proper logic for requesting these
# filterTypeDF(df, ['INFO'])
# df = filterUIDDF(df, "942c7e3")
# df = filterContent(df, "XNT6LGX5PV5X8N82")
# df = filterDate(df, "2023-08-03T11:30:03", "2023-08-03T11:50:03")

@app.route('/')
def index():
    global df, filtered_df
    if(df.size > 0):
        filtered_df = df
        return render_template('index.html',
                        column_names=df.columns.values, row_data=list(df.values.tolist()),
                        zip=zip, link_column="content")
    else:
        return render_template('index.html')

@app.route('/upload')
def show_upload():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Create new case folder
    unique_foldername = str(uuid.uuid4())
    case_folder_path = os.path.join(base_dir, cases_path, unique_foldername)
    os.mkdir(case_folder_path)

    my_filename = os.path.join(case_folder_path, 'case.log')
    contents = []
    # Upload fields to newly created case folder
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(case_folder_path, uploaded_file.filename))
    # Parse each file data into data obj and remove uploaded files
    for filename in os.listdir(case_folder_path):
        f = os.path.join(case_folder_path, filename)
        if os.path.isfile(f):
            loaded_data, lines = parseData(os.path.join(case_folder_path, filename), data)
            for line in lines:
                contents.append(line)
            # Remove temp_uploaded files from newly created folder
            os.remove(os.path.join(case_folder_path, filename))
    # Write all files log lines to case.log
    with open(my_filename, "wb") as handle:
        for line in contents:
            handle.write(line.encode())
    # Create data frame from all log file lines
    global df, filtered_df
    df = pd.DataFrame(loaded_data)
    filtered_df = df
    print(filtered_df)
    return render_template('index.html',
                        column_names=df.columns.values, row_data=list(df.values.tolist()),
                        zip=zip, link_column="content")

@app.route('/filter', methods=['POST'])
def filter_df():
    global df_filters, filtered_df
    start_date = ''
    # Update FIlter list based on request
    for key, value in request.form.items():
        print('key: ' + key + " val: " + value)
        if(value == ''):
            continue
        if(key == 'uid'):
            df_filters[key].append(value)
            continue
        if(key == 'find'):
            df_filters['find'] = [value]
            continue
        if(key == 'type'):
            if(value != 'NONE'):
                df_filters['type'].append(value)
            continue
        if(key == 'start-date'):
            start_date = value
            continue
        if(key == 'end-date'):
            if(start_date != ''):
                df_filters['date'] = [[start_date, value]]
            continue
    # Apply all filters and display filtered dataframe
    filtered_df = apply_filters()
    return render_template('index.html',
                        column_names=filtered_df.columns.values, row_data=list(filtered_df.values.tolist()),
                        zip=zip, link_column="content", filters=df_filters)


def parseData(filename, data):
    f = open(filename,"r")
    lines = f.readlines()
    for line in lines:
        timestamp = line[:34]
        timestamp = timestamp[timestamp.find('[') + 1 : timestamp.find(']')]
        data['timestamp'].append(timestamp[:19])

        logger_type_end = line[35:].find(':')
        logger_type = line[35 : 35 + logger_type_end]
        type = logger_type[logger_type.find('.') + 1 :]
        data['type'].append(type)

        uid_start = line.find('{"uid":"') + 8
        if(uid_start != -1):
            uid = line[uid_start: uid_start + 7]
            data['uid'].append(uid)
        else:
            data['uid'].append(" - ")

        content = line[36 + logger_type_end : uid_start - 8]
        data['content'].append(content)

    return data, lines

def apply_filters():
    global df_filters, df, filtered_df
    filtered_df = df
    for date in df_filters['date']:
        start = datetime.datetime.strptime(date[0], '%Y-%m-%dT%H:%M')
        end = datetime.datetime.strptime(date[1], '%Y-%m-%dT%H:%M')
        filtered_df = filterDate(filtered_df, start, end)

    for text in df_filters['find']:
        filtered_df = filterContent(filtered_df, text)

    for uid_filter in df_filters['uid']:
        filtered_df = filterUIDDF(filtered_df, uid_filter)
    
    
    filtered_df = filterTypeDF(filtered_df, df_filters['type'])

    return filtered_df
    

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

