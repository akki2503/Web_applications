import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import cv2
import base64
from dash.dependencies import Input, Output
from PIL import Image
from io import BytesIO as _BytesIO

# Load data
df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])
options = ['grayscale', 'hsv']

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('Dash - Image Transformations'),
                                 html.P('Transforming Images with Plotly - Dash.'),
                                 html.P('Pick one transformation from below'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='optionselector', options=get_options(options),
                                                      value='grayscale',
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='optionselector',
                                                      clearable=False
                                                    
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(id='image', className='eight columns div-for-charts bg-grey',
                             children=[
                                dcc.Graph(id='interactive-image', style={'height': '80vh'})])
                 ])])

def grayscale(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return img

def hsv(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return img

# Callback for timeseries price
@app.callback(Output('image', 'children'),
              [Input('optionselector', 'value')])
def update_graph(selected_dropdown_value):
    image = cv2.imread('data/IMG_20190406_135457.jpg')

    if selected_dropdown_value=='grayscale':
        img = grayscale(image)
    if selected_dropdown_value=='hsv':
        img = hsv(image)

    im_pil = Image.fromarray(img)
    buff = _BytesIO()
    im_pil.save(buff, format='png')
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")

    return dcc.Graph(
                        id='interactive-image',
                        figure={
                                'data': [],
                                'layout': {
                                            'margin': go.layout.Margin(l=40, b=40, t=26, r=10),
                                            'xaxis': {
                                                        'range': (0, 400),
                                                        'scaleanchor': 'y',
                                                        'scaleratio': 1,
                                                        'showgrid': False
                                                    },
                                            'yaxis': {
                                                        'range': (0, 400),
                                                        'showgrid': False

                                                    },
                                            'images': [{
                                                        'xref': 'x',
                                                        'yref': 'y',
                                                        'x': 0,
                                                        'y': 0,
                                                        'yanchor': 'bottom',
                                                        'sizing': 'stretch',
                                                        'sizex': 400,
                                                        'sizey': 400,
                                                        'layer': 'below',
                                                        'source': 'data:image/png;base64, ' + encoded,
                                                     }],
                                            }
                                }

                    )

if __name__ == '__main__':
    app.run_server(debug=True)
