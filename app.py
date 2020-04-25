
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


external_stylesheet= [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh',
        'crossorigin': 'anonymous'
    }
]

data = pd.read_csv('covid_19_clean_complete1.csv')
data1=pd.read_csv('IndividualDetails5.csv')

total=data1.shape[0]
mask=data1['current_status'].value_counts()

d_state=data1['detected_state'].value_counts().reset_index()


final=data.groupby('Country/Region')['Deaths'].max().sort_values(ascending=False).reset_index().head(30)


options=[
    {'label':'All','value':'All'},
    {'label':'China','value':'China'},
    {'label':'Iran','value':'Iran'},
    {'label':'US','value':'US'},
    {'label':'United Kingdom','value':'United Kingdom'},
    {'label':'Italy','value':'Italy'},
    {'label':'India','value':'India'}
]

status_info=[
    {'label':'All','value':'All'},
    {'label':'Recovered	','value':'Recovered'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Deceased','value':'Deceased'}

]
pie_option=[
    {'label':'All','value':'All'},
    {'label':'Maharashtra','value':'Maharashtra'},
    {'label':'Delhi','value':'Delhi'},
    {'label':'Kerala','value':'Kerala'},
    {'label':'Telangana','value':'Telangana'},
    {'label': 'West Bengal	', 'value': 'West Bengal'},
    {'label': 'Rajasthan', 'value': 'Rajasthan'},
    {'label': 'Tamil Nadu', 'value': 'Tamil Nadu'},
    {'label': 'Uttar Pradesh', 'value': 'Uttar Pradesh'}
]





app = dash.Dash(__name__, external_stylesheets=external_stylesheet)

app.layout=html.Div([
    html.Div([
        html.H1("Corono Virus Pandemic Reports",style={'margin-top':'5px'}),
        html.P("Covid19 India",style={'text-align':'left','margin-top':'-40px'})
    ],className='jumbotron'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(total),
                            html.H6("Total Test Case")
                        ],className='card-body')
                    ],className='card',style={'background-color':'purple','margin-top':'0.5rem'})
                ],className='col-md-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(mask[0]),
                            html.H6("Confirmed Case")
                        ],className='card-body')
                    ],className='card',style={'background-color':'#fc5555','margin-top':'0.5rem'})
                ],className='col-md-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(mask[1]),
                            html.H6("Recovered Case")
                        ],className='card-body')
                    ],className='card',style={'background-color':'#0FD604','margin-top':'0.5rem'})
                ],className='col-md-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(mask[2]),
                            html.H6("Death Case")
                        ],className='card-body')
                    ],className='card',style={'background-color':' #be0404','margin-top':'0.5rem'})
                ],className='col-md-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(mask[3]),
                            html.H6("Migrated")
                        ],className='card-body')
                    ],className='card',style={'background-color':'#7dc3fc','margin-top':'0.5rem'})
                ],className='col-md-12')
            ],className='row')
        ],className='col-md-2'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(id='scatter-plot',
                                        figure={'data':[go.Bar(x=final['Country/Region'],y=final['Deaths'])],
                                        'layout':go.Layout(title='Number of Death according to Country',xaxis={'title':'Country/Region'},yaxis={'title':'Number of Deaths'},paper_bgcolor='rgba(0,0,0,1)',plot_bgcolor='rgba(0,0,0,1)')})

                        ],className='card-body')
                    ],className='card')
                ],className='col-md-6'),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(id='pie', options=pie_option, value='All'),
                            dcc.Graph(id='pie1')
                        ],className='card-body')
                    ],className='card')
                ],className='col-md-6'),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(id='d_state',
                                      figure={'data':[go.Bar(x=d_state['index'],y=d_state['detected_state'])],
                                              'layout':go.Layout(title='No. of  case in Different state',xaxis={'title':'State'},yaxis={'title':'Number of patients'})})
                        ],className='card-body')
                    ],className='card')
                ],className='col-md-6 mt-3'),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(id='piker',options=options,value='All'),
                            dcc.Graph(id='line')
                        ],className='card-body')
                    ],className='card')
                ],className='col-md-6 mt-3')

            ],className='row')
        ],className='col-md-10')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                        dcc.Dropdown(id='pik',options=status_info,value='All'),
                        dcc.Graph(id='line2')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12 mt-3')
    ],className='row'),
    html.Div([],className='row')
],className='container-fluid')




@app.callback(Output('line','figure'), [Input('piker','value')])
def update_graph(type):
    if type=='All':
        mask = data.groupby('Date')['Deaths'].max().sort_values(ascending=True).reset_index()
        return {'data':[go.Line(x=mask['Date'],y=mask['Deaths'])],
                'layout':go.Layout(title='Number of Deaths Per Day',xaxis={'title':'Dates'},yaxis={'title':'Number of Deaths'},paper_bgcolor='rgba(0,0,0,1)',plot_bgcolor='rgba(0,0,0,1)')}
    else:
        mask = data[data['Country/Region'] == type]
        masks = mask.groupby('Date')['Deaths'].max().sort_values(ascending=True).reset_index()
        return {'data': [go.Line(x=masks['Date'], y=masks['Deaths'])],
                'layout': go.Layout(title='Number of Deaths Per Day',xaxis={'title':'Dates'},yaxis={'title':'Number of Deaths'},paper_bgcolor='rgba(0,0,0,1)',plot_bgcolor='rgba(0,0,0,1)')}


@app.callback(Output('line2','figure'), [Input('pik','value')])
def update_graph(type1):
    if type1=='All':
        masks=data1['detected_state'].value_counts().reset_index()
        return {'data':[go.Line(x=masks['index'],y=masks['detected_state'])],
                'layout':go.Layout(title='Number of Patients',xaxis={'title':'Number of Patients'},yaxis={'title':'states'})}
    else:
        status = data1[data1['current_status'] == type1]
        mask4 = status['detected_state'].value_counts().reset_index()
        return {'data': [go.Line(x=mask4['index'], y=mask4['detected_state'])],
                'layout': go.Layout(title='Number of Patients',xaxis={'title':'Number of patients'},yaxis={'title':'States'})}


@app.callback(Output('pie1','figure'), [Input('pie','value')])
def update_graph(type2):
    if type2=='All':
        p_mask = data1['current_status'].value_counts().reset_index()
        val1 = p_mask['current_status'][0]
        val2 = p_mask['current_status'][1]
        val3 = p_mask['current_status'][2]

        labels = ['Hospitalized', 'Recovered', 'Deceased']
        values = [val1, val2, val3]
        figure=go.Figure(data=[go.Pie(labels=labels, values=values)])
        return figure
    else:
        mask = data1[data1['detected_state'] == type2]
        p_mask = mask['current_status'].value_counts().reset_index()
        val1 = p_mask['current_status'][0]
        val2 = p_mask['current_status'][1]
        val3 = p_mask['current_status'][2]
        values = [val1, val2, val3]
        labels = ['Hospitalized', 'Recovered', 'Deceased']
        figure= go.Figure(data=[go.Pie(labels=labels, values=values)])
        return figure








if __name__ == '__main__':
    app.run_server(debug=True)
