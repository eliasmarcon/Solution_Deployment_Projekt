# import dash
# import dash_bootstrap_components as dbc
# import plotly.graph_objects as go
# import plotly.express as px
# import pandas as pd
# import requests

# import utilitiespg1

# from dash import html
# from dash import dcc
# from dash.dependencies import Input, Output, State
# from datetime import datetime, timedelta


# # App Main
# app = dash.Dash(__name__)

# # Style Components
# # Fix sidebar to the left side
# SIDEBAR_STYLE = {
#     "position": "fixed", "top": "5rem", "left": 0, "bottom": 0,
#     "width": "20rem", "padding": "2rem 1rem", "background-color": "#f8f9fa",
# }

# # Place main content on the right
# CONTENT_STYLE = {
#     "display": "inline-block", "margin-left": "21rem", "margin-right": "2rem", "padding": "2rem 1rem"
# }


# ######################################################################
# #################### Data Processing Section #########################
# ######################################################################

# # Load Dataset
# df = pd.read_csv("./Dataset/Dataset.csv", delimiter = ",")


# # Generate Filter Options Organisation
# def generate_options(dataframe, column, sorted = False):

#     listoptions = list(dataframe[column].unique())
    
    
#     listoptions.sort()
    
#     options = []

#     for sym in listoptions:

#         options.append({'label': sym, 'value': sym})

#     return options


# # Get Filtered Dataframe based on User Input
# def getFilteredDataframe(organisation : str = "Twitter", year1 : int = df.year.min(), year2 : int = df.year.max(), sector : str = 'web', method : str = 'hacked'):

#     df_temp = df[(df['year'].between(year1, year2)) & (df['organisation'] == organisation) & (df['sector'] == sector) & (df['method'] == method)].sort_values(by = ['year'])
    
#     return df_temp




# html.H6('Select Sector of your choice.'),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-sector-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-sector',
#                             options = utilities.generate_options(df, 'sector'), value = 'web', className = 'postselector', #multi = True
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 ),
#                 html.Div( 
#                     className = 'div-for-method-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-method',
#                             options = utilities.generate_options(df, 'method'), value = 'hacked', className = 'postselector', #multi = True
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 )
#             ]
#         ),


# ######################################################################
# ######################### Style Section ##############################
# ######################################################################

# # Create Slidebar
# sidebar_1 = html.Div(
#     [
#         html.H3('Select organisation of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className ='div-user-controls',
#             children= [
#                 html.Div( 
#                     className='div-for-land-dropdown',
#                     children=[ 
#                         dcc.Dropdown(
#                             id = 'select-organisation',
#                             options = generate_options(df, 'organisation'), value = 'Twitter', className = 'postselector'
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H3('Select Year of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-year-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-year',
#                             options = generate_options(df, 'year'), value = '2004', className = 'postselector'
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 ),
#                 html.Div( 
#                     className = 'div-for-year2-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-year2',
#                             options = generate_options(df, 'year'), value = '2022', className = 'postselector'
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 )
#             ]
#         ),
#         html.H3('Select Sector and Method of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-sector-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-sector',
#                             options = generate_options(df, 'sector'), value = 'web', className = 'postselector', #multi = True
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 ),
#                 html.Div( 
#                     className = 'div-for-method-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-method',
#                             options = generate_options(df, 'method'), value = 'hacked', className = 'postselector', #multi = True
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 )
#             ]
#         ),
#         html.H3('Select Method of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-method2-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-method2',
#                             options = generate_options(df, 'method'), value = 'hacked', className = 'postselector', #multi = True
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H3('Select Data Sensitivity of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-sensitivity-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-sensitivity',
#                             options = generate_options(df, 'data_sensitivity_text'), className = 'postselector', #multi = True #value = 'Full details', 
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H3('Fast API'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-date-picker',
#                     children = [ 

#                         html.P('Drücken Sie den Button um eine Prediction zu erhalten!', style = {'textAlign': 'justify'}),
#                         # html.P('Ausgewählte Zeitperiode in Tagen: ' + str(len(df))),
#                         html.Div(id = "zeitraum_id"),
#                         html.Div(id = "bundesland_id"),
#                         html.Br(),
#                         dbc.Button(id = 'API_Button', children = 'Calculate with API'),
#                         html.Hr(),
#                         html.Div(id = "API_Call")
#                     ],
#                 ),
#             ]
#         )
#     ],

#     style = SIDEBAR_STYLE # Include style to fix position
# )

# # Create Slidebar 2
# sidebar_2 = html.Div(
#     [
#         html.H2('Select organisation of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className ='div-user-controls',
#             children= [
#                 html.Div( 
#                     className='div-for-land-dropdown',
#                     children=[ 
#                         dcc.Dropdown(
#                             id = 'select-organisation',
#                             options = generate_options(df, 'organisation'), value = 'Twitter', className = 'postselector'
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H2('Select Year of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-year-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-year',
#                             options = generate_options(df, 'year'), value = '2004', className = 'postselector'
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 ),
#                 html.Div( 
#                     className = 'div-for-year2-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-year2',
#                             options = generate_options(df, 'year'), value = '2022', className = 'postselector'
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 )
#             ]
#         ),
#         html.H2('Select Sector and Method of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-sector-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-sector',
#                             options = generate_options(df, 'sector'), value = 'web', className = 'postselector', #multi = True
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 ),
#                 html.Div( 
#                     className = 'div-for-method-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-method',
#                             options = generate_options(df, 'method'), value = 'hacked', className = 'postselector', #multi = True
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 )
#             ]
#         ),
#         html.H2('Select Method of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-method2-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-method2',
#                             options = generate_options(df, 'method'), value = 'hacked', className = 'postselector', #multi = True
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H2('Select Data Sensitivity of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-sensitivity-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-sensitivity',
#                             options = generate_options(df, 'data_sensitivity_text'), className = 'postselector', #multi = True #value = 'Full details', 
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H2('Fast API'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-date-picker',
#                     children = [ 

#                         html.P('Drücken Sie den Button um eine Prediction zu erhalten!', style = {'textAlign': 'justify'}),
#                         # html.P('Ausgewählte Zeitperiode in Tagen: ' + str(len(df))),
#                         html.Div(id = "zeitraum_id"),
#                         html.Div(id = "bundesland_id"),
#                         html.Br(),
#                         dbc.Button(id = 'API_Button', children = 'Calculate with API'),
#                         html.Hr(),
#                         html.Div(id = "API_Call")
#                     ],
#                 ),
#             ]
#         )
#     ],

#     style = SIDEBAR_STYLE # Include style to fix position
# )

# # Create Slidebar 3
# sidebar_3 = html.Div(
#     [
#         html.H2('Select organisation of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className ='div-user-controls',
#             children= [
#                 html.Div( 
#                     className='div-for-land-dropdown',
#                     children=[ 
#                         dcc.Dropdown(
#                             id = 'select-organisation',
#                             options = generate_options(df, 'organisation'), value = 'Twitter', className = 'postselector'
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H2('Select Year of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-year-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-year',
#                             options = generate_options(df, 'year'), value = '2004', className = 'postselector'
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 ),
#                 html.Div( 
#                     className = 'div-for-year2-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-year2',
#                             options = generate_options(df, 'year'), value = '2022', className = 'postselector'
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 )
#             ]
#         ),
#         html.H2('Select Sector and Method of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-sector-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-sector',
#                             options = generate_options(df, 'sector'), value = 'web', className = 'postselector', #multi = True
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 ),
#                 html.Div( 
#                     className = 'div-for-method-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-method',
#                             options = generate_options(df, 'method'), value = 'hacked', className = 'postselector', #multi = True
#                         )
#                     ],
#                     style = {'width': '49%', 'display': 'inline-block'}
#                 )
#             ]
#         ),
#         html.H2('Select Method of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-method2-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-method2',
#                             options = generate_options(df, 'method'), value = 'hacked', className = 'postselector', #multi = True
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H2('Select Data Sensitivity of your choice.'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-sensitivity-picker',
#                     children = [ 
#                          dcc.Dropdown(
#                             id = 'select-sensitivity',
#                             options = generate_options(df, 'data_sensitivity_text'), className = 'postselector', #multi = True #value = 'Full details', 
#                         )
#                     ],
#                 ),
#             ]
#         ),
#         html.H2('Fast API'),
#         html.Hr(),
#         html.Div( 
#             className = 'div-user-controls',
#             children= [
#                 html.Div( 
#                     className = 'div-for-date-picker',
#                     children = [ 

#                         html.P('Drücken Sie den Button um eine Prediction zu erhalten!', style = {'textAlign': 'justify'}),
#                         # html.P('Ausgewählte Zeitperiode in Tagen: ' + str(len(df))),
#                         html.Div(id = "zeitraum_id"),
#                         html.Div(id = "bundesland_id"),
#                         html.Br(),
#                         dbc.Button(id = 'API_Button', children = 'Calculate with API'),
#                         html.Hr(),
#                         html.Div(id = "API_Call")
#                     ],
#                 ),
#             ]
#         )
#     ],

#     style = SIDEBAR_STYLE # Include style to fix position
# )

# # Create Main Content Area
# content_1 = html.Div(
#     id = "page-content", 
#     children = [
#                     html.Div(
#                         className='div-for-text',
#                         children=[
#                             html.H1('Worlds biggest Data Breaches & Hacks'), 
#                             html.P('''A basic Dashboard with Dash and Plotly, showing the worlds biggest data breaches.''')
#                         ]
#                     ),
#                     html.Div(
#                         children = [dcc.Graph(id = 'KPI_Fälle_Zeitperiode')],
#                         style={'width': '49%', 'display': 'inline-block'}
#                     ),
#                     html.Div(
#                         children = [dcc.Graph(id = 'KPI_Lost_records')],
#                         style = {'width': '49%', 'display': 'inline-block'}
#                     )
#                 ],

#     style = CONTENT_STYLE # Include style to fix position
# )

# # Create Main Content Area 2
# content_2 = html.Div(
#     id = "page-content", 
#     children = [
#                     html.Div(
#                         className='div-for-text',
#                         children=[
#                             html.H1('Worlds biggest Data Breaches & Hacks Company'), 
#                             html.P('''A basic Dashboard with Dash and Plotly, showing the worlds biggest data breaches.''')
#                         ]
#                     ),
#                     html.Div(
#                         children = [dcc.Graph(id = 'KPI_Fälle_pro_Jahr')],
#                         style={'width': '100%', 'height' : '50%', 'display': 'inline-block'}
#                     ),
#                     html.Div(
#                         #children = [dcc.Graph(id = 'Tests_Zeitraum')],
#                         style = {'width': '100%', 'display': 'inline-block'}
#                     )
#                 ],

#     style = CONTENT_STYLE # Include style to fix position
# )

# # Create Main Content Area 3
# content_3 = html.Div(
#     id = "page-content", 
#     children = [
#                     html.Div(
#                         className='div-for-text',
#                         children=[
#                             html.H1('Worlds biggest Data Breaches & Hacks Comparison'), 
#                             html.P('''A basic Dashboard with Dash and Plotly, showing the worlds biggest data breaches.''')
#                         ]
#                     ),
#                     html.Div(
#                         children = [dcc.Graph(id = 'KPI_Fälle_pro_Jahr')],
#                         style={'width': '100%', 'height' : '50%', 'display': 'inline-block'}
#                     ),
#                     html.Div(
#                         #children = [dcc.Graph(id = 'Tests_Zeitraum')],
#                         style = {'width': '100%', 'display': 'inline-block'}
#                     )
#                 ],

#     style = CONTENT_STYLE # Include style to fix position
# )


# # Define the app
# #app.layout = html.Div([sidebar, content])
# app.layout = html.Div([
#     dcc.Tabs(
#         id = "tabs-with-classes",
#         value = 'tab-1',
#         parent_className = 'custom-tabs',
#         className = 'custom-tabs-container',
#         children = [
#                         dcc.Tab(
#                             label = 'Tab one',
#                             value = 'tab-1',
#                             className = 'custom-tab',
#                             selected_className = 'custom-tab--selected'
#                         )
#                         # dcc.Tab(
#                         #     label = 'Tab two',
#                         #     value = 'tab-2',
#                         #     className = 'custom-tab',
#                         #     selected_className = 'custom-tab--selected'
#                         # ),
#                         # dcc.Tab(
#                         #     label = 'Tab three, multiline',
#                         #     value = 'tab-3', className = 'custom-tab',
#                         #     selected_className='custom-tab--selected'
#                         # )
#                     ]),
#     html.Div(id = 'tabs-content-classes')
# ])

# @app.callback(Output('tabs-content-classes', 'children'),
#               Input('tabs-with-classes', 'value'))
# def render_content(tab):

#     if tab == 'tab-1':

#         return html.Div([sidebar_1, content_1])

#     # elif tab == 'tab-2':

#     #     return html.Div([sidebar_2, content_2])

#     # elif tab == 'tab-3':

#     #     return html.Div([sidebar_3, content_3])




# ##############################################
# ######### Utilities file######################
# ##############################################


# # check if the year is smaller
# def checkYear(dataframe, start_year, end_year):

#     if int(start_year) < int(end_year):

#         temp = start_year
#         start_year = end_year
#         end_year = temp

#     df_year = dataframe[(dataframe['year'] >= int(start_year)) & (dataframe['year'] <= int(end_year))]

#     return df_year


# ##############################################
# ######### KPI Fälle Jahr & Zeitperiode #######
# ##############################################

# def getVorfälleYear(df, start_year, end_year):

#     df_year = checkYear(df, start_year, end_year)

#     if int(start_year) == int(end_year):

#         length_year_before = len(df[df['year'] == int(start_year - 1)])

#         fig = go.Figure(go.Indicator(
#                                         mode = "number+delta",
#                                         value = len(df_year),
#                                         #number = {'prefix': "$"},
#                                         delta = {'position': "bottom", 'reference': length_year_before},
#                                         domain = {'x': [0, 1], 'y': [0, 1]}
#                                     )
#                         )

#         fig.update_layout(title = {'text' : "Vorfälle innerhalb des Jahres!"}, paper_bgcolor = "lightgray")

#     else:

#         fig = go.Figure(go.Indicator(
#                                         mode = "number+delta",
#                                         value = len(df_year),
#                                         domain = {'x': [0, 1], 'y': [0, 1]}
#                                     )
#                         )

#         fig.update_layout(title = {'text' : "Vorfälle innerhalb des gewählten Zeitraums!"}, paper_bgcolor = "lightgray")

#     return fig



# ##############################################
# #### KPI Lost Records Jahr & Zeitperiode #####
# ##############################################

# def getLostRecordsYear(df, start_year, end_year):

#     df_year = checkYear(df, start_year, end_year)

#     if int(start_year) == int(end_year):

#         records_year_before = df[df['year'] == int(start_year - 1)]['records_lost'].sum()

#         print(df_year['records_lost'].sum())
#         print(records_year_before)

#         fig = go.Figure(go.Indicator(
#                                         mode = "number+delta",
#                                         value = df_year['records_lost'].sum(),
#                                         #number = {'subfix': "$"},
#                                         delta = {'position': "bottom", 'reference': records_year_before},
#                                         domain = {'x': [0, 1], 'y': [0, 1]}
#                                     )
#                         )

#         fig.update_layout(title = {'text' : "Vorfälle innerhalb des Jahres!"}, paper_bgcolor = "lightgray")
#         fig.update_traces(texttemplate = '%{text:.8f}', textposition = 'outside', textfont_size = 12, textangle = 0)

#     else:

#         fig = go.Figure(go.Indicator(
#                                         mode = "number+delta",
#                                         value = df_year['records_lost'].sum(),
#                                         domain = {'x': [0, 1], 'y': [0, 1]}
#                                     )
#                         )

#         fig.update_layout(title = {'text' : "Vorfälle innerhalb des gewählten Zeitraums!"}, paper_bgcolor = "lightgray")
    
#     # df_Tests = getFilteredDataframe2("", start_date, end_date)

#     # df_Tests = df_Tests.groupby(['Bundesland']).sum().reset_index().sort_values(by = ['Tests_daily'])

#     # fig = px.bar(df_Tests, x = 'Bundesland', y = 'Tests_daily', color = 'Bundesland', text = 'Tests_daily')
#     # fig.update_traces(texttemplate = '%{text:.3s}', textposition = 'outside', textfont_size = 12, textangle = 0)
#     # fig.update_layout(title = {'text' : "Durchgeführte Tests im ausgewählten Zeitraum!"})

#     return fig

















































# ######################################################################
# #################### Function Plot Section ###########################
# ######################################################################

# # KPI Fälle Zeitperiode / Jahr
# @app.callback( 
#     Output('KPI_Fälle_Zeitperiode', 'figure'),
#     Input('select-year', 'value'),
#     Input('select-year2', 'value'))
# def generateKPIVorfälle(start_year : int, end_year : int):

#     fig = utilitiespg1.getVorfälleYear(df, start_year, end_year)

#     return fig

# # KPI Lost records Zeitperiode / Jahr
# @app.callback( 
#     Output('KPI_Lost_records', 'figure'),
#     Input('select-year', 'value'),
#     Input('select-year2', 'value'))
# def generateKPIVorfälle(start_year : int, end_year : int):

#     fig = utilitiespg1.getLostRecordsYear(df, start_year, end_year)

#     return fig









# # Run the app
# def start():    
#     # app.run_server(host = '0.0.0.0', port = 80)
#     return 'Done!'

# if __name__ == '__main__':
#     # start()
#     #app.run_server(host = '0.0.0.0', port = 80)
#     app.run_server(debug=True, port = "8051")




