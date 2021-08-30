import math
import numpy as np
import pandas as pd

NUM_COUNTIES = 159

def matchdicts(mat,keys1,keys2,matching):
    if mat.size == 0:
        return matching
    flattened = mat.flatten()
    minval = min(flattened)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i][j] == minval:
                matching.update({keys1[i]:keys2[j]})
                # print(mat[i][j],len(list(matching.keys())))
                keys1 = np.delete(keys1,i)
                mat = np.delete(mat,i,0)
                keys2 = np.delete(keys2,j)
                mat = np.delete(mat,j,1)
                return matchdicts(mat,keys1,keys2,matching)


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
df = pd.read_csv(source + 'novresults_basic.csv')
demog_data = pd.read_csv(source + 'demographics_basic.csv')

outer_map = {}

counties = demog_data['County'].tolist()
precincts = demog_data['Precinct'].tolist()
count = demog_data['Registered Voters'].tolist()
precinct_results = df['Precinct']
county_results = df['County']
rv_2020 = df['Registered Voters']

unique_precincts = {}
for i in range(len(counties)):
    county = counties[i].upper()
    precinct = precincts[i]
    if county not in unique_precincts:
        unique_precincts.update({county:{}})
    if precinct not in unique_precincts[county]:
        unique_precincts[county].update({precinct:count[i]})
result_map = {}
for i in range(len(county_results)):
    if county_results[i] == county_results[i]:
        county = county_results[i].upper()
        precinct = precinct_results[i]
        if county not in result_map:
            result_map.update({county:{}})
        if precinct not in result_map[county]:
            result_map[county].update({precinct:rv_2020[i]})
        # result_map[county][precinct] += count[i]


source_folder = '/Users/akshaygowrish/Documents/surf2021/Data/'
demog = pd.read_excel(source_folder + 'PrecinctDemographics.xlsx',sheet_name=0)
results = pd.read_csv(source_folder + 'ga_nov2020_results.csv')
races = demog['Race'].tolist()
genders = demog['Gender'].tolist()
counties_raw = demog['County Name'].tolist()
precincts_raw = demog['County Precinct'].tolist()
rv_raw = demog['Total'].tolist()
curr_precinct = ''

matching_outer = {}

for i in range(NUM_COUNTIES):
    county = list(unique_precincts.keys())[i]
    if county not in result_map:
        continue
    keys1 = list(unique_precincts[county].keys())
    sum1 = sum(unique_precincts[county].values())
    keys2 = list(result_map[county].keys())
    sum2 = sum(result_map[county].values())
    mat = np.zeros((len(keys1),len(keys2)))
    for k in range(len(keys1)):
        for j in range(len(keys2)):
            mat[k][j] = abs(unique_precincts[county][keys1[k]]*sum2/sum1-result_map[county][keys2[j]])
    matching_outer.update({county:matchdicts(mat,keys1,keys2,{})})
    # print(matchdicts(mat,keys1,keys2,{}))

for i in range(len(counties_raw)):
    curr_county = counties_raw[i]
    if curr_county not in matching_outer:
        continue
    curr_precinct = precincts_raw[i]
    if curr_precinct not in matching_outer[curr_county]:
        continue
    curr_precinct = matching_outer[curr_county][precincts_raw[i]]
    if races[i] != races[i]:
        continue
    race_index = race_indices[races[i]]
    gender_index = gender_indices[genders[i]]
    if curr_county not in outer_map:
        outer_map.update({curr_county : {}})
    if curr_precinct not in outer_map[curr_county]:
        outer_map[curr_county].update({curr_precinct:[0 for j in range(21)]})
    outer_map[curr_county][curr_precinct][race_index*3 + gender_index] = rv_raw[i]

list_races = list(race_indices.keys())
list_gender = list(gender_indices.keys())
list_county = results['County'].tolist()
list_precinct = results['Precinct'].tolist()
results_length = len(list_precinct)
for i in range(21):
    race_index = i // 3
    gender_index = i % 3
    results[list_races[race_index] + ', ' + list_gender[gender_index]] = [0 for j in range(results_length)]
for j in range(results_length):
    county = list_county[j].upper()
    precinct = list_precinct[j]
    if precinct not in outer_map[county]:
        print(county,precinct)
        continue
    for i in range(21):
        race_index = i // 3
        gender_index = i % 3
        key = list_races[race_index] + ', ' + list_gender[gender_index]
        results[key][j] = outer_map[county][precinct][i]
results = results.drop(columns=['Unnamed: 0'])
print(results)
results.to_csv(source+'novresults_demographics.csv')