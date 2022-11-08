import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import openpyxl
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

df = pd.read_excel('Наставники.xlsx').drop('Отметка времени', axis=1)
data = pd.read_excel('наставники1.xlsx')

blok = data["Блок"].unique()
otdel = data['Отдел'].unique()
fio = data["ФИО"].unique()

df = df.rename(columns={'Заинтересованность в конечном результате':'Заинтересованность','Скорость и качество обратной связи':'Обратная связь'})
df2 = df.melt(id_vars=['Выберите своего наставника'], var_name='Компетенции', value_name='Баллы')
name = df['Выберите своего наставника'].unique()
dct_pos = {'Тоноян Грант Егишевич':'Начальник отдела ведения нормативно-справочной информации',
           'Стасюк Владислав Николаевич':'Начальник отдела формирования регистров и отчетности',
           'Логинова Елена Александровна':'Начальник отдела организации интеграционного взаимодействия',
           'Жириль Александр Николаевич':'Начальник отдела технологического обеспечения',
           'Волкова Светлана Алексеевна':'Начальник отдела централизованного учета операций с учреждениями и юридическими лицами',
           'Чижов Сергей Сергеевич':'Начальник отдела консолидированной бух. отчетности подведомственных учреждений и анализа',
           'Монашев Петр Игоревич':'Начальник отдела внутреннего контроля и аудита',
           'Емельянов Павел Викторович':'Начальник отдела сопровождения пользователей',
           'Дикарева Наталья Викторовна':'Начальник отдела централизованного учета операций государственного сектора',
           'Кухаренков Алексей Сергеевич':'Начальник отдела централизованного учета нефинансовых активов',
           'Курелов Амин Хан-Гереевич':'Начальник отдела централизованного учета кассовых поступлений и выбытий',
           'Королева Юлия Вячеславовна':'Начальник отдела централизованного начисления заработной платы и иных выплат'}

rating = pd.DataFrame(dct_pos.items(), columns=['Наставник', 'Должность'], index=range(1, len(dct_pos)+1))
for i in range(len(dct_pos)):
    x = rating.iloc[i, 0]
    rating.loc[i+1, ['Общая оценка']] = df[df['Выберите своего наставника'] == x].mean().mean()
rating = rating.sort_values('Общая оценка', ascending=False)

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H3('Наставники Межрегионального бухгалтерского управления Федерального Казначейства', style = {"margin-bottom": "0px", 'color': 'white'}),
                html.H5('', style = {"margin-top": "0px", 'color': 'white'}),

            ]),
        ], className = "six column", id = "title")

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.P('Выберите блок:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'блок',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Административно-хозяйственный блок',
                         placeholder = '',
                         options = [{'label': c, 'value': c} for c in blok], className = 'dcc_compon'),

            html.P('Выберите отдел:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'отдел',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True, 'color': 'black'},
                         placeholder = 'Выбрать Отдел',
                         options = [], className = 'dcc_compon'),

            html.P('Выберите ФИО:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id='ФИО',
                         multi=False,
                         clearable=True,
                         disabled=False,
                         style={'display': True},
                         placeholder='Выбрать ФИО',
                         options=[], className='dcc_compon'),
        ], className="create_container twelve column")

    ], className="row flex-display"),

    html.Div([
        html.Div([
            html.Img(id='img', width='250px', className='my_img'),
            html.P(id='pos', className='fix_label', style={'color': 'white'})
        ], className = "create_container three columns"),


        html.Div([
            dcc.Graph(id = 'bar_line_1',
                      config = {'displayModeBar': 'hover'}, figure={'layout':{'plot_bgcolor':'red'}}),

        ], className = "create_container six columns"),

        html.Div([
            dcc.Graph(id = 'pie',
                      config = {'displayModeBar': 'hover'}, figure={}, className='my_pie'),
            html.Div(id='donut_chart_text1',
                     className='donut_chart_text'),
            html.Div('Общая оценка', className='donut_text', style={'color':'white', 'fontSize': 30})
        ], className = "create_container three columns"),

    ], className = "row flex-display"),

        html.Div([
        html.Div([
            html.Div([
                html.P('Общий рейтинг', className = 'fix_label', style = {'color': 'white', 'fontSize': 30}),
                html.Table([
                    html.Thead(
                        html.Tr([
                            html.Th('Место', style={'width': '30px', 'textAlign': 'center', 'fontSize': 20}),
                            html.Th('ФИО',
                                    style={'width': '120px', 'fontSize': 20},
                                    className='crypto_column'
                                    ),
                            html.Th('Должность', style={'width': '120px', 'fontSize': 20}),
                            html.Th('Общая оценка', style={'width': '90px', 'fontSize': 20})
                        ], className='header_hover')
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td(html.Img(src = app.get_asset_url('first-place.png'),
                                 style = {'height': '80px', 'text-Align': 'center'},
                                 className = 'coin')
                                    ),
                            html.Td(html.Div([
                                html.P('{}'.format(rating.iloc[0, 0]),
                                       className='logo_text', style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                       )
                            ], className='logo_image'),
                            ),
                            html.Td(
                                html.H6('{}'.format(rating.iloc[0, 1]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),

                            ),
                            html.Td(
                                html.H6('{0:,.2}'.format(rating.iloc[0, 2]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                    ),
                        ),
                        ], className='hover_only_row'),
                        html.Tr([
                            html.Td(html.Img(src = app.get_asset_url('second-place.png'),
                                 style = {'height': '80px', 'text-Align': 'center'},
                                 className = 'coin'),
                                    ),
                            html.Td(html.Div([
                                html.P('{}'.format(rating.iloc[1, 0]),
                                       className='logo_text', style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               })
                            ], className='logo_image'),
                            ),
                            html.Td(
                                html.H6('{}'.format(rating.iloc[1, 1]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),

                            ),
                            html.Td(
                                html.H6('{0:,.2}'.format(rating.iloc[1, 2]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),
                            ),
                        ], className='hover_only_row'),
                        html.Tr([
                            html.Td(html.Img(src = app.get_asset_url('third-place.png'),
                                 style = {'height': '80px', 'text-Align': 'center'},
                                 className = 'coin'),
                                    ),
                            html.Td(html.Div([
                                html.P('{}'.format(rating.iloc[2, 0]),
                                       className='logo_text', style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               })
                            ], className='logo_image'),
                            ),
                            html.Td(
                                html.H6('{}'.format(rating.iloc[2, 1]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),

                            ),
                            html.Td(
                                html.H6('{0:,.2}'.format(rating.iloc[2, 2]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),
                            ),
                        ], className='hover_only_row'),
                        html.Tr([
                            html.Td(html.P('4', style={'textAlign': 'center',
                                                       'color': 'white',
                                                       'fontSize': 20,
                                                       'margin-top': '10px',
                                                       }),
                                    ),
                            html.Td(html.Div([
                                html.P('{}'.format(rating.iloc[3, 0]),
                                       className='logo_text', style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               })
                            ], className='logo_image'),
                            ),
                            html.Td(
                                html.H6('{}'.format(rating.iloc[3, 1]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),

                            ),
                            html.Td(
                                html.H6('{0:,.2}'.format(rating.iloc[3, 2]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),
                            ),
                        ], className='hover_only_row'),
                        html.Tr([
                            html.Td(html.P('5', style={'textAlign': 'center',
                                                       'color': 'white',
                                                       'fontSize': 20,
                                                       'margin-top': '10px',
                                                       }),
                                    ),
                            html.Td(html.Div([
                                html.P('{}'.format(rating.iloc[4, 0]),
                                       className='logo_text', style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               })
                            ], className='logo_image'),
                            ),
                            html.Td(
                                html.H6('{}'.format(rating.iloc[4, 1]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),

                            ),
                            html.Td(
                                html.H6('{0:,.2}'.format(rating.iloc[4, 2]),
                                        style={'textAlign': 'left',
                                               'color': 'white',
                                               'margin-top': '10px',
                                               'fontSize': 20,
                                               }
                                        ),
                            ),
                        ], className='hover_only_row'),
                    ])
                ], className='table_style'),
            ], className='table_width'),
        ], className="create_container 12 columns"),

    ], className="row flex-display"),
], id = "mainContainer", style = {"display": "flex", "flex-direction": "column"})

@app.callback(
    Output('отдел', 'options'),
    Input('блок', 'value'))
def get_options(blok):
    ter = data[data["Блок"] == blok]
    return [{'label': i, 'value': i} for i in ter['Отдел'].unique()]

@app.callback(
    Output('отдел', 'value'),
    Input('отдел', 'options'))
def get_value(otdel):
    return [k['value'] for k in otdel][0]

@app.callback(
    Output('ФИО', 'options'),
    Input('отдел', 'value'))
def get_options_1(otdel):
    ter1 = data[data['Отдел'] == otdel]
    return [{'label': i, 'value': i} for i in ter1['ФИО'].unique()]

@app.callback(
    Output('ФИО', 'value'),
    Input('ФИО', 'options'))
def get_value_1(fio):
    return [j['value'] for j in fio][0]

# Create combination of bar and line  chart (show number of attack and death)
@app.callback(Output('bar_line_1', 'figure'),
              Input('ФИО', 'value'))

def update_graph(w_countries):
    # Data for line and bar
    fig1 = px.bar(df2[df2['Выберите своего наставника'] == w_countries].groupby('Компетенции').mean().round(2),
                  range_x=[0, 10],
                  labels={  # replaces default labels by column name
                      "value": "Количество баллов", "variable": "", "Компетенции":'Качества наставника'},
                  color_discrete_map={  # replaces default color mapping by value
                      "Баллы":"#DEB340"},
                  orientation='h'
                  )
    fig1.update_layout(transition_duration=500,
                       paper_bgcolor="#aabdcc",
                       plot_bgcolor="#aabdcc",
                       font=dict(
                           family="sans-serif",
                           size=20,
                           color='white'),
                       showlegend = False
                       )
    fig1.update_traces(textfont = dict(
                            family = "Arial Black",
                            size = 20,
                            color = "black"),
                        texttemplate='%{y}: %{x}')
    fig1.update_yaxes(visible = False)
    return fig1

@app.callback(Output('img', 'src'),
              Input('ФИО', 'value'))

def update_graph(mentor):
    src = r'assets/' + mentor + '.png'
    return src

@app.callback(Output('pos', 'children'),
              Input('ФИО', 'value'))

def update_pos(mentor):
    children = dct_pos[mentor]
    return children

# Create pie chart (total casualties)
@app.callback(Output('pie', 'figure'),
              Input('ФИО', 'value'))
def update_pie(select_mentor):
        df3 = df.copy()
        ball = df3[df3['Выберите своего наставника'] == select_mentor].mean().mean()
        max_ball = 10 - ball
        colors = ['#DEB340', '#2e3d52']

        return {
            'data': [go.Pie(labels = ['', ''],
                            values = [ball, max_ball],
                            marker = dict(colors = colors,
                                          line=dict(color='#DEB340', width=2)),
                            hoverinfo = 'skip',
                            textinfo = 'text',
                            hole = .7,
                            rotation = 0
                            )],

            'layout': go.Layout(
                plot_bgcolor = 'rgba(0,0,0,0)',
                paper_bgcolor = 'rgba(0,0,0,0)',
                margin = dict(t = 35, b = 10, r = 0, l = 0),
                showlegend = False,
                title={'text': '',
                       'y': 0.95,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                titlefont = {'color': 'white',
                             'size': 15},
            ),

        }
@app.callback(Output('donut_chart_text1', 'children'),
              Input('ФИО', 'value'))

def update_text(select_mentor):
        df4 = df.copy()
        ball = df4[df4['Выберите своего наставника'] == select_mentor].mean().mean()

        return [
            html.P('{:.2}'.format(ball),
                   style = {
                       'color': '#010915',
                       'fontSize': 100,
                       'font-weight': 'bold'
                   }),
        ]

if __name__ == '__main__':
    app.run_server(debug = True)
