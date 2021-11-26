
import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# নিচের অ্যাাপ কল করে যাস্ট সার্ভারে রান অথাত ওয়েবে রান করাইছি।
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

# এইটা হলো প্রথম ও ওয়েব পেজ , যেখনে dash use করে file select করবো।
# আমি নিচের দুইটা Div function কমেন্ট করে দিছি এখন রান করায়া দেখলে শুধু লে আউট টা দেখতে পারবি
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },

        multiple=True
    ),

    # নিচের ২ টা ফাংশন কমেন্ট করে দিলে
    # html.Div(id='output-div'),
    html.Div(id='output-datatable'),
])

# html.Div(id='output-datatable'),  নিচের ফাংশন দাড়া প্রথম callback return kore. line number 98-107

# নিচের ফানশন কল হইছে নিচের কল ব্যাক থেকে
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
# এখনে ফাইল নেম কি, সে অনুসারে হ্যান্ডেল করবো csv hole , xls hole....
# এইটা ড্যাশ ডকুমেন্টেই আছে।
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:

            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:

            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
# নিচের সবটুকু রিটার্ন করবে ফাংশন থেকে।
    return html.Div([
        html.H5(filename), # ফাইল নাম অনুসারে নাম দেখাবে
        html.H6(datetime.datetime.fromtimestamp(date)), # নামের পর একটা ডেট ও আছে দেখিস
        html.P("Inset X axis data"), # তারপর এক্স এক্সিস ইন্সার্ট করার জন্য এইটা শো করবও
        dcc.Dropdown(id='xaxis-data', # তারপর কলাম অনুসারে , option নামক লিস্টে সব ডাটা ইন্সার্ট করবো, Y axis এ ও সেম
                     options=[{'label': x, 'value': x} for x in df.columns]),
        html.P("Inset Y axis data"),
        dcc.Dropdown(id='yaxis-data',
                     options=[{'label': x, 'value': x} for x in df.columns]),
        html.Button(id="submit-button", children="Create Graph"), # বাটন create করলাম গ্রাফ create করার জন্য
        html.Hr(), # Hr() mane Y axis er সমান্তরাল ।
# এইটা দারা ১৫ টা কলাম নিচে শো কররো।
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),

        html.Hr(),


        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
# html.Div(id='output-div'), এই ফাংশন নিচের callback e কাজ  করে

@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'), # dcc.Upload component থেকে upload data r ৩ টা যিনিস বা প্ররপস নিতে পারি  content , filename and last_modified
              # এগুলা থেকে আমরা ফাইল শীট টা ইনপুট নিব আসলে। যখনই dcc.Upload দিবো তখনই এই যিনিস গুলাতে কিছু ডাটা যোগ হবে।
              # for more information visit dash.Upload component properties
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
# update_output নামের ফাংশন টা দিয়ে আমরা যে csv ফাইল ইনপুট নিছি তা নিজের ইচ্ছা মত চেঞ্জ করে ব্যাবহার করতে পারি
# এখনে list_of_contents e কিছু না থকলে  if function কল হবে নাহ।
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        #  children নামক একটা লিস্টে যা প্যারামিটার নিছলাম তা tuple এর মত iterate করবো , এর জন্য ওপ্রের parse_contents() function call করছি।
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        # লাস্ট্ব এ children list টা রিটার্ন কোঁরে দিবো।
        return children

# html.Div(id='output-div'), এই ফাংশন নিচের অংশটুকু কাজ করে
# এখনে থেকেই আমরা আসলে গ্রাফ টা রিটার্ন করতেছি

# @app.callback(Output('output-div', 'children'),
#               Input('submit-button', 'n_clicks'),
#               State('stored-data', 'data'),
#               State('xaxis-data', 'value'),
#               State('yaxis-data', 'value'))
# def make_graphs(n, data, x_data, y_data):
#     if n is None:
#         return dash.no_update
#     else:
#         line_fig = px.line(data, x=x_data, y=y_data, markers=True)
#
#         return dcc.Graph(figure=line_fig)
#

if __name__ == '__main__':
    app.run_server(debug=True)

