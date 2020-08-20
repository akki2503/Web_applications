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
image = cv2.imread('data/IMG_20190406_135457.jpg')

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
                                                      className='optionselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(id='image', className='eight columns div-for-charts bg-grey',
                             children=[
                                dcc.Graph(id='interactive-image', style={'height': '80vh'})])
                                #  dcc.Graph(id='image', config={'displayModeBar': False}, animate=True)
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
    # trace1 = []
    df_sub = df
    image = cv2.imread('data/IMG_20190406_135457.jpg')
    HTML_IMG_SRC_PARAMETERS = 'data:image/png;base64, '
    for option in selected_dropdown_value:
        if option=='grayscale':
            img = grayscale(image)
            cv2.imwrite('/assets/grayscale.jpg', img)
        else:
            img = hsv(image)
            cv2.imwrite('/assets/hsv.jpg', img)
        
        # fig = go.Figure()
        # fig.add_layout_image(img)
        # trace1.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                #  y=df_sub[df_sub['stock'] == stock]['value'],
                                #  mode='lines',
                                #  opacity=0.7,
                                #  name=stock,
                                #  textposition='bottom center'))
        # traces = [trace1]
        # data = [val for sublist in traces for val in sublist]
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
                                            'scaleratio': 1
                                        },
                                        'yaxis': {
                                            'range': (0, 400)
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
