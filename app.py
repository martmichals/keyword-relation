import dash, re, base64, io
import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import time

# App instantiation
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX]
)

# Content for the singular query tab
single_query_tab = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                    dbc.Input(
                        id='input-k1',
                        type='text',
                        placeholder='Keyword 1',
                        style = {
                            'width': '25%',
                            'float': 'left',
                            'height': '52px'
                        }
                    ),
                    dbc.Input(
                        id='input-k2',
                        type='text',
                        placeholder='Keyword 2',
                        style = {
                            'width': '25%',
                            'marginLeft': '10px',
                            'float': 'left',
                            'height': '52px'
                        }
                    ),
                    dbc.Button(
                        'Submit Query', 
                        id='submit-singular-query',
                        outline=True, 
                        color='primary', 
                        className='mr-1',
                        style={
                            'overflow': 'hidden',
                            'marginLeft': '10px'
                        }
                    ),
                ],
                id='singular-input-section',
                style={
                    'width': '100%',
                }
            ),
            dbc.Spinner(
                html.Div(
                    id='singular-query-results',
                    style={
                        'width': '100%',
                        'marginTop': '50px'
                    }
                ),
                color='dark'
            )
        ]
    ),
    className='mt-3',
)

# Content for the mass query tab
multiple_query_tab = dbc.Card(
    dbc.CardBody(
        [
            html.P(
                'Files must be of the type *.csv, and have '
                'the columns (keyword1, keyword2).',
                className='lead',
            ),
            dcc.Upload(
                id='upload-queries',
                children=[
                    'Drag and Drop or Click to Browse',
                ], 
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                },
                multiple=False
            ),
            dbc.Spinner(
                html.Div(
                    id='multiple-query-results',
                    style={
                        'width': '100%',
                        'marginTop': '50px'
                    }
                ),
                color='dark'
            )
        ]
    ),
    className='mt-3',
)

# Put tabs together
tabs = dbc.Tabs(
    [
        dbc.Tab(single_query_tab, label='Singular Query'),
        dbc.Tab(multiple_query_tab, label='Multiple Queries'),
    ],
    style = {
        'margin': '10px'
    }
)

# App layout
app.layout = html.Div([
    # Website title
    html.Div([
            html.H1(
                'Keyword Queries', 
            ),
            html.P(
                'Given a keyword pair, this tool generates a description '
                'for how the words are related.',
                className='lead',
            )
        ],
        style = {
            'margin': '10px'
        }
    ),
    # Tabs for query submission
    tabs 
])

# Singular query submission
@app.callback(Output('singular-query-results', 'children'),
              Input('submit-singular-query', 'n_clicks'),
              State('input-k1', 'value'),
              State('input-k2', 'value'))
def render_content(n_clicks, k1, k2):
    # No input
    if n_clicks == None:
        return html.Div()

    # Erroneous input, immediately detectable
    if k1 is None or k2 is None or k1 == '' or k2 == '':
        return html.Div([
            dbc.Alert(
                'One or both of the keywords is empty.',
                color='danger'
            )
        ])
    
    # Launch function call to get word linking
    return html.Div([
        html.H3('Result'),
        html.P('This is the linking sentence')
    ])

# Input file parsing, and launching of query processing functions
#   Code for this section is based heavily on plotly documentation:
#   https://dash.plotly.com/dash-core-components/upload
def parse_contents(contents, filename):
    # Split contents
    content_type, content_string = contents.split(',')

    # Decode file contents
    decoded = base64.b64decode(content_string)
    try:
        # Assume that the user uploaded a CSV file
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8'))
            )

        # Format validation
        if df.columns[0] != 'keyword1' or df.columns[1] != 'keyword2':
            return dbc.Alert(
                'Column names ({}, {}) are not equal to (keyword1, keyword2).'.format(df.columns[0], df.columns[1]),
                color='danger'
            )
    except Exception as e:
        return dbc.Alert(
            'There was an error in processing the file.',
            color='danger'
        )

    return html.Div([
        html.H5(filename),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

# Multiple query submission via file upload
@app.callback(Output('multiple-query-results', 'children'),
              Input('upload-queries', 'contents'),
              State('upload-queries', 'filename')
            )
def update_output(contents, filename):
    # Children to return
    children = [
        html.P('Filename: {}'.format(filename))
    ]

    # Return without filename
    if filename is None:
        return children

    # Check if the file is a csv file
    if re.match(r'.*\.csv', filename) is not None:
        children.append(parse_contents(contents, filename))
        return children
    else:
        children.append(
            dbc.Alert(
                'The file is not a *.csv file.',
                color='danger'
            )
        )

    # Return the child
    time.sleep(1)
    return children

# Start application
if __name__ == '__main__':
    app.run_server(debug=True)