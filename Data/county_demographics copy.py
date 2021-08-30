import os
import pandas as pd
import numpy as np
import math

NUM_GENDERS = 3
NUM_RACES = 7
NUM_AGES = 10
NUM_COUNTIES = 159

counties = pd.read_csv('/Users/akshaygowrish/Downloads/US_counties/uscounties.csv')
names = counties['county']
fips = counties['county_fips']
ga_counties = []
for i in range(len(fips)):
    if int(fips[i]) > 13000 and int(fips[i]) < 14000:
        ga_counties.append(names[i])
ga_counties.sort()

source = '/Users/akshaygowrish/Downloads/Active_Voters_by_Race_and_Gender_by_Age_Group_(By_County_with_Statewide_Totals)1.xlsx'
dest = '/Users/akshaygowrish/Documents/surf2021/Data/county_demographics.xlsx'
#os.rename(source,dest)
df = pd.read_excel(dest,sheet_name=0,header=8)
counties = df['COUNTY NAME'].tolist()
print(len(counties))
for i in range(len(counties)):
    if counties[i] != counties[i]:
        continue
df_arr = df.to_numpy()
print(df_arr)

cross_sections = np.zeros((NUM_GENDERS*NUM_RACES*NUM_AGES,NUM_COUNTIES))
for j in range(NUM_COUNTIES):
    print(j)
    for i in range(NUM_GENDERS*NUM_RACES*NUM_AGES):
        cross_sections[i][j] = df_arr[(j*(NUM_AGES+1))+(i % NUM_AGES)][(i // NUM_AGES) + 3]
print(cross_sections)

new_demographics = pd.DataFrame(columns=ga_counties)
# new_demographics.columns = ga_counties
for i in range(len(ga_counties)):
    new_demographics[ga_counties[i]] = cross_sections[:,i]
print(new_demographics)

