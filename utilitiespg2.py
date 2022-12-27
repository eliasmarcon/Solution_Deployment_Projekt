import plotly.graph_objects as go
import plotly.express as px
import utilities

# filter multiple Sectors 
def getMultipleSectors(df, sector):

    if len(sector) == 0:

        return df
    
    elif type(sector) == str:

        df_temp = df[df['sector_1'] == sector]

    else:

        df_temp = df[df['sector_1'].isin(sector)]

    return df_temp

#################################################
########## KPI unique number for column #########
#################################################
def getKPIDatensetgroeße(df, start_year, end_year, column, titlename):

    df_year = utilities.checkYear(df, start_year, end_year)

    df = df_year[column].unique() 

    fig = go.Figure(go.Indicator(
                                    mode = "number+delta",
                                    number = {"font": {"size": utilities.number_size}},
                                    value = len(df),
                                    domain = {'x': [0, 1], 'y': [0, 1]}
                            )
                    )

    fig.update_layout(title = {'text' : "Unique <br> " + titlename})
    fig.update_layout(title = dict(font = dict(size = utilities.title_size)), title_x = 0.5, height = utilities.kpi_height)

    return fig

#########################################################
######### KPI count of breaches in year & period  #######
#########################################################
def getVorfälleYear(df, start_year, end_year):

    df_year = utilities.checkYear(df, start_year, end_year)

    if int(start_year) == int(end_year):

        length_year_before = len(df[df['year'] == int(start_year - 1)])

        fig = go.Figure(go.Indicator(
                                        mode = "number+delta",
                                        value = len(df_year),
                                        number = {"font": {"size": utilities.number_size}},
                                        delta = {'position': "bottom", 
                                                 'reference': length_year_before, 
                                                 'valueformat' : '.2%',
                                                 'relative': True},
                                        domain = {'x': [0, 1], 'y': [0, 1]}
                                    )
                        )

        fig.update_layout(title = {'text' : "Count of breaches<br>in selected year"}, height = utilities.kpi_height)

    else:

        fig = go.Figure(go.Indicator(
                                        mode = "number+delta",
                                        number = {"font": {"size": utilities.number_size}},
                                        value = len(df_year),
                                        domain = {'x': [0, 1], 'y': [0, 1]}
                                    )
                        )

        fig.update_layout(title = {'text' : "Count of breaches<br>in selected period"}, height = utilities.kpi_height)

    fig.update_layout(title = dict(font = dict(size = utilities.title_size)), title_x = 0.5)

    return fig

##############################################
###### KPI stolen data in year & period ######
##############################################
def getLostRecordsYear(df, start_year, end_year):

    df_year = utilities.checkYear(df, start_year, end_year)

    if int(start_year) == int(end_year):

        records_year_before = df[df['year'] == int(start_year - 1)]['records_lost'].sum()

        fig = go.Figure(go.Indicator(
                                        mode = "number+delta",
                                        value = df_year['records_lost'].sum(),
                                        number = {"font": {"size": utilities.number_size}},
                                        delta = {'position': "bottom", 
                                                 'reference': records_year_before,
                                                 'valueformat' : '.2%',
                                                 'relative': True},
                                        domain = {'x': [0, 1], 'y': [0, 1]}
                                    )
                        )

        fig.update_layout(title = {'text' : "Sum of stolen data<br>in selected year"})

    else:

        fig = go.Figure(go.Indicator(
                                        mode = "number+delta",
                                        number = {"font": {"size": utilities.number_size}},
                                        value = df_year['records_lost'].sum(),
                                        domain = {'x': [0, 1], 'y': [0, 1]}
                                    )
                        )

        fig.update_layout(title = {'text' : "Sum of stolen data<br>in selected period"}, showlegend=False)

    fig.update_layout(title = dict(font = dict(size = utilities.title_size)), title_x = 0.5, height = utilities.kpi_height)

    return fig

##############################################
######## Barchart by year and sector #########
##############################################
def getBarchartProJahrSektor(df, start_year, end_year):

    df_year = utilities.checkYear(df, start_year, end_year)
    df = df_year.groupby(['year', 'sector_1']).sum().reset_index().sort_values(by = ['year'])

    fig = px.bar(df, x = 'year', y = 'records_lost', color = 'sector_1', text = ['{:.2} Mrd'.format(x / 1000000000) for x in df['records_lost']], height=utilities.chart_height_3)
    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(title = {'text' : "Sum of stolen data by sector in selected period"}, yaxis_range = [0, max(df.records_lost) * 1.2], title_x = 0.5, legend_title_text = '')
    fig.update_yaxes(title = None)
    return fig

##############################################
############ Piechart for column #############
##############################################
def getPieChart(df, start_year, end_year, column, titlename):

    df_year = utilities.checkYear(df, start_year, end_year)
    df = df_year.groupby(column).size().reset_index(name = 'anzahl')
    fig = px.pie(df, values = df.anzahl, names = df[column], hole = .7, height=utilities.chart_height_3)

    fig.update_layout(legend = dict(orientation = "h"), title_text = titlename + "<br>distribution", title_x=0.5)

    return fig