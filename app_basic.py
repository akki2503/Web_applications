import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import cv2
import base64
from dash.dependencies import Input, Output

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
                                                      multi=True, value=['grayscale'],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='optionselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 html.Img(src='data:image;base64,{}'.format('image'))
                             ])
                              ])
        ]

)

def grayscale(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return img

def hsv(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return img

# Callback for timeseries price
@app.callback(Output('image', 'encoded_image'),
              [Input('optionselector', 'value')])
def update_graph(selected_dropdown_value, image):
    # trace1 = []
    df_sub = df
    for option in selected_dropdown_value:
        if option=='grayscale':
            img = grayscale(image)
        else:
            img = hsv(image)
        
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
        # figure = {'data': img,
        #         'layout': go.Layout(
        #             colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
        #             template='plotly_dark',
        #             paper_bgcolor='rgba(0, 0, 0, 0)',
        #             plot_bgcolor='rgba(0, 0, 0, 0)',
        #             margin={'b': 15},
        #             hovermode='x',
        #             autosize=True,
        #             title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
        #             xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
        #         ),

        #         }
        encoded_image = base64.b64encode(img)
        # fig = px.imshow(img)
        # figure = fig.show()

    return encoded_image


if __name__ == '__main__':
    app.run_server(debug=True)
