import os
import shortuuid
import datetime
import pandas as pd
from flask_paginate import Pagination, get_page_args
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
cases_path = os.path.join(base_dir, 'cases')

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
case_names = []

### ENDPOINTS
@app.route('/')
def index():
    global df, filtered_df, cases_path, case_names
    case_names = get_cases(cases_path)
    return render_template('index.html', case_dirs=case_names)

@app.route('/upload')
def show_upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Create new case folder
    unique_foldername = "[CASE]" + str(shortuuid.uuid())
    case_folder_path = os.path.join(cases_path, unique_foldername)
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
            loaded_data, lines = parse_file_data(os.path.join(case_folder_path, filename), data)
            for line in lines:
                contents.append(line)
            # Remove temp_uploaded files from newly created folder
            os.remove(os.path.join(case_folder_path, filename))
    
    # Write all files log lines to case.log
    with open(my_filename, "wb") as handle:
        for line in contents:
            handle.write(line.encode())
    
    # Create data frame from all log file lines
    global df, filtered_df, case_names
    df = pd.DataFrame(loaded_data)
    filtered_df = df
    case_names = get_cases(cases_path)
    return redirect(url_for('show_filtered', filename=unique_foldername))


@app.route('/<filename>/filter', methods=['POST'])
def filter_df(filename):
    global df_filters, filtered_df
    # Update Filter list based on request
    df_filters = add_filters(df_filters, request.form.items())
    return redirect(url_for('show_filtered', filename=filename))


@app.route('/<filename>')
def show_filtered(filename):
    global df, df_filters, filtered_df, case_names, cases_path
    case_folder_path = os.path.join(cases_path, filename)
    f = os.path.join(case_folder_path, 'case.log')
    if os.path.isfile(f):
        loaded_data, lines = parse_file_data(f, data)
    
    df = pd.DataFrame(loaded_data)
    filtered_df = df
    # Apply all filters and display filtered dataframe
    filtered_df = apply_filters()
    page, per_page, offset = get_page_args(page_parameter='page',
                                        per_page_parameter='per_page')
    total = len(filtered_df)
    pagination_users = get_entries(filtered_df, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    if (request.args.get('page') is not None):
        page = request.args.get('page')

    return render_template('index.html',
                        column_names = df.columns.values,
                        row_data = list(pagination_users.values.tolist()),
                        page = page,
                        per_page = per_page,
                        pagination = pagination,
                        file_uid = filename,
                        zip = zip,
                        filters = df_filters,
                        link_column = "content",
                        case_dirs=case_names)

@app.route('/<filename>/remove-filter', methods=['POST'])
def remove_filter(filename):
    global df_filters, filtered_df
    # Update FIlter list based on request
    df_filters = remove_filter(df_filters, request.form.items())
    return redirect(url_for('show_filtered', filename=filename))

@app.route('/<filename>/clear-filter')
def clear_filter(filename):
    global df_filters, filtered_df
    df_filters = {
        'date': [],
        'type': [],
        'find': [],
        'uid': []
    }
    return redirect(url_for('show_filtered', filename=filename))


# Parse log file content as data object
def parse_file_data(filename, data):
    f = open(filename,"r")
    lines = f.readlines()
    # Iterate through each line that will be parsed into data fields
    for line in lines:
        # Parse timestamp
        timestamp = line[:34]
        timestamp = timestamp[timestamp.find('[') + 1 : timestamp.find(']')]
        data['timestamp'].append(timestamp[:19])
        # Parse log type
        logger_type_end = line[35:].find(':')
        logger_type = line[35 : 35 + logger_type_end]
        type = logger_type[logger_type.find('.') + 1 :]
        data['type'].append(type)
        # Parse uid
        uid_start = line.find('{"uid":"') + 8
        if(uid_start != -1):
            uid = line[uid_start: uid_start + 7]
            data['uid'].append(uid)
        else:
            data['uid'].append(" - ")
        # Parse log content
        content = line[36 + logger_type_end : uid_start - 8]
        data['content'].append(content)
    return data, lines

# Apply all filters in df_filters
def apply_filters():
    global df_filters, df, filtered_df
    filtered_df = df
    if(df_filters['date'] != []):
        for date in df_filters['date']:
            start = datetime.datetime.strptime(date[0], '%Y-%m-%dT%H:%M')
            end = datetime.datetime.strptime(date[1], '%Y-%m-%dT%H:%M')
            filtered_df = filter_df_between_dates(filtered_df, start, end)
        
    filtered_df = find_df_contents(filtered_df, df_filters['find'])
    filtered_df = filter_df_uids(filtered_df, df_filters['uid'])
    filtered_df = filter_df_types(filtered_df, df_filters['type'])

    return filtered_df
    
# Sorting DataFrame ASC
def sort_df(df):
    return df.sort_values(by=['timestamp'])

# Filtering DataFrame by type
def filter_df_types(df, values):
    if not values:
        return df
    return df[df['type'].isin(values)]

# Filtering DataFrame by uid
def filter_df_uids(df, values):
    if not values:
        return df
    return df[df['uid'].isin(values)]

# Filtering DataFrame by String to match in content
def find_df_contents(df, values):
    if not values:
        return df
    for value in values:
        df = df[df['content'].str.contains(value)]
    return df

# Filtering DataFrame by date between start_date and end_date
def filter_df_between_dates (df, start_date, end_date):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    mask = (df['timestamp'] > start_date) & (df['timestamp'] <= end_date)
    print(df.loc[mask])

    return df.loc[mask]

# Get df as entries filtered by offset and pagination limit
def get_entries(df, offset=0, per_page=10):
    # print(df[offset: offset + per_page])
    return df[offset: offset + per_page]


def add_filters(df_filters, items):
    start_date = ''
    for key, value in items:
        if(value == ''):
            continue
        if(key == 'uid'):
            df_filters[key].append(value)
            continue
        if(key == 'find'):
            df_filters['find'] = [value]
            continue
        if(key == 'type'):
            if(value != 'NONE' and value not in df_filters['type']):
                df_filters['type'].append(value)
            continue
        if(key == 'start-date'):
            start_date = value
            continue
        if(key == 'end-date'):
            if(start_date != ''):
                df_filters['date'] = [[start_date, value]]
            continue
    return df_filters


def remove_filter(df_filters, items):
    for key, value in items:
        if(key == 'uid'):
            df_filters[key].remove(value)
            continue
        if(key == 'find'):
            df_filters['find'] = []
            continue
        if(key == 'type'):
            if(value != 'NONE'):
                df_filters['type'].remove(value)
            continue
        if(key == 'date'):
            df_filters['date'] = []
            continue
    return df_filters

def get_cases(rootdir):
    paths = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            paths.append(d)
    return paths