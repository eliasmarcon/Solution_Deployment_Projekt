import plotly.graph_objects as go
import plotly.express as px
import utilities



##############################################
############## KPI Style Sheet #####ää########
##############################################

kpi_height = 200
title_size = 15
number_size = 40
chart_height = 400



# filter multiple Sectors 
def getMultipleSectors(df, sector):

    if len(sector) == 0:

        return df
    
    elif type(sector) == str:

        df_temp = df[df['sector_1'] == sector]

    else:

        df_temp = df[df['sector_1'].isin(sector)]

    return df_temp

##############################################
########## KPI Anzahl Generealisiert #########
##############################################
def getKPIDatensetgroeße(df, start_year, end_year, column, titlename):

    df_year = utilities.checkYear(df, start_year, end_year)

    df = df_year[column].unique() 

    fig = go.Figure(go.Indicator(
                                    mode = "number+delta",
                                    number = {"font": {"size": number_size}},
                                    value = len(df),
                                    domain = {'x': [0, 1], 'y': [0, 1]}
                            )
                    )

    fig.update_layout(title = {'text' : "Unique <br> " + titlename}, height = kpi_height)
    fig.update_layout(title = dict(font = dict(size = title_size)), title_x = 0.5)

    return fig


##############################################
######### KPI Fälle Jahr & Zeitperiode #######
##############################################
def getVorfälleYear(df, start_year, end_year):

    df_year = utilities.checkYear(df, start_year, end_year)

    if int(start_year) == int(end_year):

        length_year_before = len(df[df['year'] == int(start_year - 1)])

        fig = go.Figure(go.Indicator(
                                        mode = "number+delta",
                                        value = len(df_year),
                                        number = {"font": {"size": number_size}},
                                        delta = {'position': "bottom", 
                                                 'reference': length_year_before, 
                                                 'valueformat' : '.2%',
                                                 'relative': True},
                                        domain = {'x': [0, 1], 'y': [0, 1]}
                                    )
                        )

        fig.update_layout(title = {'text' : "Lost Records innerhalb des Jahres!"}, height = kpi_height)

    else:

        fig = go.Figure(go.Indicator(
                                        mode = "number+delta",
                                        number = {"font": {"size": number_size}},
                                        value = len(df_year),
                                        domain = {'x': [0, 1], 'y': [0, 1]}
                                    )
                        )

        fig.update_layout(title = {'text' : "Count of breaches<br>in selected period"}, height = kpi_height)

    fig.update_layout(title = dict(font = dict(size = title_size)), title_x = 0.5)

    return fig



##############################################
#### KPI Lost Records Jahr & Zeitperiode #####
##############################################
def getLostRecordsYear(df, start_year, end_year):

    df_year = utilities.checkYear(df, start_year, end_year)

    if int(start_year) == int(end_year):

        records_year_before = df[df['year'] == int(start_year - 1)]['records_lost'].sum()

        fig = go.Figure(go.Indicator(
                                        mode = "number+delta",
                                        value = df_year['records_lost'].sum(),
                                        number = {"font": {"size": number_size}},
                                        delta = {'position': "bottom", 
                                                 'reference': records_year_before,
                                                 'valueformat' : '.2%',
                                                 'relative': True},
                                        domain = {'x': [0, 1], 'y': [0, 1]}
                                    )
                        )

        fig.update_layout(title = {'text' : "Vorfälle innerhalb des Jahres!"}, height = kpi_height)

    else:

        fig = go.Figure(go.Indicator(
                                        mode = "number+delta",
                                        number = {"font": {"size": number_size}},
                                        value = df_year['records_lost'].sum(),
                                        domain = {'x': [0, 1], 'y': [0, 1]}
                                    )
                        )

        fig.update_layout(title = {'text' : "Sum of stolen data<br>in selected period"}, showlegend=False, title_x = 0.5, height = kpi_height)

    fig.update_layout(title = dict(font = dict(size = title_size)), title_x = 0.5)

    return fig



##############################################
########### Get Barchart pro Jahr ############
##############################################
def getBarchartProJahr(df, start_year, end_year):

    df_year = utilities.checkYear(df, start_year, end_year)
    df = df_year.groupby(['year']).sum().reset_index().sort_values(by = ['year'])

    # print(df.dtypes)

    fig = px.bar(df, x = 'year', y = 'records_lost', text = ['{:.2} Mrd'.format(x / 1000000000) for x in df['records_lost']])
    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(title = {'text' : "Sum of stolen data in selected period"}, yaxis_range = [0, max(df.records_lost) * 1.1], showlegend=False, title_x = 0.5)

    return fig



##############################################
####### Get Barchart pro Jahr & Sektor #######
##############################################
def getBarchartProJahrSektor(df, start_year, end_year):

    df_year = utilities.checkYear(df, start_year, end_year)
    df = df_year.groupby(['year', 'sector_1']).sum().reset_index().sort_values(by = ['year'])

    fig = px.bar(df, x = 'year', y = 'records_lost', color = 'sector_1', text = ['{:.2} Mrd'.format(x / 1000000000) for x in df['records_lost']], height=chart_height)
    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(title = {'text' : "Sum of stolen data by sector in selected period"}, yaxis_range = [0, max(df.records_lost) * 1.2], title_x = 0.5, legend_title_text = '')
    fig.update_yaxes(title = None)
    return fig



##############################################
### Get Barchart größten Unternehmen Leaks ###
##############################################
def getBarchartLeaksUnternehmen(df, start_year, end_year):

    df_year = utilities.checkYear(df, start_year, end_year)

    df = df_year.groupby(['organisation']).sum().reset_index().sort_values(by = ['records_lost'])
    df = df[-10:]

    fig = px.bar(df, x = "organisation", y = 'records_lost', color = "organisation", text = ['{:.2} Mrd'.format(x / 1000000000) for x in df['records_lost']], height=chart_height)
    fig.update_traces(textposition = 'inside', textfont_size = 12, textangle = 0)
    fig.update_layout(title = {'text' : "Sum of stolen data<br>in selected period"}, showlegend=False, title_x = 0.5, xaxis_showticklabels=False)
    fig.update_yaxes(title = None)
    return fig



##############################################
############### Get Piechart #################
##############################################
def getPieChart(df, start_year, end_year, column, titlename):

    df_year = utilities.checkYear(df, start_year, end_year)
    df = df_year.groupby(column).size().reset_index(name = 'anzahl')
    fig = px.pie(df, values = df.anzahl, names = df[column], hole = .7, height=chart_height)

    fig.update_layout(legend = dict(orientation = "h"), title_text = titlename + "<br>distribution", title_x=0.5)

    return fig

