import math
import numpy as np
import pandas as pd

race_indices = {'American Indian or Alaskan ':0, \
    'Asian or Pacific Islander':1, \
        'Black not of Hispanic Origin':2, \
            'Hispanic':3, \
                'Other':4, \
                    'Unknown':5, \
                        'White not of Hispanic Origin':6}

race_map = {'American Indian or Alaskan ':'Native', \
    'Asian or Pacific Islander':'Asian', \
        'Black not of Hispanic Origin':'Black', \
            'Hispanic':'Hispanic', \
                'Other':'Other', \
                    'Unknown':'Unknown', \
                        'White not of Hispanic Origin':'White'}

gender_indices = {'Male':0,'Female':1,'Unknown':2}

source = '/Users/akshaygowrish/Documents/surf2021/Data/'
jan_data = pd.read_csv(source + 'ga_jan2021_results.csv')
nov_data = pd.read_csv(source + 'novresults_demographics.csv')

outer_map = {}

jan_counties = jan_data['County'].tolist()
jan_precincts = jan_data['Precinct'].tolist()
nov_counties = nov_data['County'].tolist()
nov_precincts = nov_data['Precinct'].tolist()

jan_map = {}
cols = jan_data.columns
selected_columns = cols[4:]
for i in range(len(jan_counties)):
    curr_county = jan_counties[i]
    curr_precinct = jan_precincts[i]
    if curr_county not in jan_map:
        jan_map.update({curr_county:{}})
    jan_map[curr_county].update({curr_precinct:[0 for j in range(35)]})
    row = jan_data.loc[[i]]
    for j in range(35):
        column = selected_columns[j]
        jan_map[curr_county][curr_precinct][j] = row[column].tolist()[0]
        if column == 'Voter Turnout':
            jan_map[curr_county][curr_precinct][j] = float(row[column].tolist()[0][:-1])



to_remove = []

jan_array = np.zeros((len(nov_counties)-57,35))

count = 0
for i in range(len(nov_counties)):
    curr_county = nov_counties[i]
    curr_precinct = nov_precincts[i]
    if curr_county not in jan_map:
        to_remove.append(i)
    elif curr_precinct not in jan_map[curr_county]:
        to_remove.append(i)
    else:
        jan_array[count] = jan_map[curr_county][curr_precinct]
        count += 1


nov_data = nov_data.drop(index=to_remove)
nov_data = nov_data.drop(columns=['Unnamed: 0'])

count = 0
rv = nov_data['Registered Voters'].tolist()
for i in range(len(jan_array)):
    if jan_array[i][1] == 0:
        count += 1
        if rv[i] == 0:
            jan_array[i][1] = 0
        else:
            jan_array[i][1] = jan_array[i][0]/rv[i]

for i in range(len(selected_columns)):
    column_name = selected_columns[i]
    nov_data['Jan ' + column_name] = jan_array[:,i]

nov_data.to_csv(source + 'combined_results_demographics.csv')