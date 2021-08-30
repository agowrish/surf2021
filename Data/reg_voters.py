import math
import numpy as np
import pandas as pd

source_folder = '/Users/akshaygowrish/Documents/surf2021/Data/'
demog = pd.read_excel(source_folder + 'PrecinctDemographics.xlsx',sheet_name=0)
results = pd.read_csv(source_folder + 'ga_nov2020_results.csv')
results_out = results[['County','Precinct','Registered Voters']]
demog_counties = []
demog_precincts = []
demog_rv = []

counties_raw = demog['County Name'].tolist()
precincts_raw = demog['County Precinct'].tolist()
rv_raw = demog['Total'].tolist()
curr_precinct = ''
for i in range(len(counties_raw)):
    if precincts_raw[i] != curr_precinct:
        demog_counties.append(counties_raw[i])
        demog_precincts.append(precincts_raw[i])
        demog_rv.append(0)
        curr_precinct = precincts_raw[i]
    demog_rv[-1] += rv_raw[i]
demog_out = pd.DataFrame(columns=['County','Precinct','Registered Voters'])
demog_out['County'] = demog_counties
demog_out['Precinct'] = demog_precincts
demog_out['Registered Voters'] = demog_rv
print(results_out)
print(demog_out)
results_out.to_csv(source_folder + 'novresults_basic.csv')
demog_out.to_csv(source_folder + 'demographics_basic.csv')