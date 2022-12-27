import pandas as pd

##############################################
############# layout constants ###############
##############################################

kpi_height = 200
title_size = 15
number_size = 40
chart_height = 300
chart_height_3 = 400

##############################################
############# helper Functions ###############
##############################################

# load dataset
def loadData():

    df = pd.read_csv("./Dataset/Dataset.csv", delimiter = ",")

    return df

# generate filter options organization
def generate_options(dataframe, column):

    listoptions = list(dataframe[column].unique())
    
    listoptions.sort()
    
    options = []

    for sym in listoptions:

        options.append({'label': sym, 'value': sym})

    return options


# check if the year is smaller
def checkYear(dataframe, start_year, end_year):

    if int(start_year) > int(end_year):

        temp = start_year
        start_year = end_year
        end_year = temp

    df_year = dataframe[(dataframe['year'] >= int(start_year)) & (dataframe['year'] <= int(end_year))]

    return df_year