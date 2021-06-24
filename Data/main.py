import shutil, os
import pandas as pd
import xlrd
from xml2xlsx import xml2xlsx
import xml.etree.ElementTree as ET
import numpy as np

NUM_COUNTIES = 159
vote_types = ['Election_Day_Votes','Advanced_Voting_Votes','Absentee_by_Mail_Votes','Provisional_Votes','Total_Votes']


def process_county_sheet(df,i):
    id = 'County'
    if 'County' not in df.columns:
        id = 'Precinct'
    length = len(df[id].tolist())
    county_list = [ga_counties[i] for j in range(length)]
    df = df.rename(columns={id:"Precinct"})
    df[id] = county_list
    df = df.drop([length-1])
    return df

def process_race_sheet(df2,df,race):
    candidates = []
    parties = []
    for col in df2.columns:
        if col[0:8] != 'Unnamed:':
            name = col.split()
            lastname = name[-2]
            if lastname == '(I)':
                lastname = name[-3]
            candidates.append(lastname)
            parties.append(name[-1][1:-1])
    race_suffix = race
    if 'County' in df.columns:
        df = df.drop(['County','Registered Voters'],axis=1)
    else:
        df = df.drop(['Precinct','Registered Voters'],axis=1)
    new_cols = []
    columns = df.columns
    for i in range(len(columns)):
        col = columns[i]
        cand_index = i // 5
        type_index = i % 5
        if i == (len(columns)-1):
            new_cols.append('Total'+'_'+race_suffix)
        else:
            new_cols.append(vote_types[type_index] + '_' +  candidates[cand_index] + '_' + parties[cand_index] + '_' + race_suffix)
    df.columns=new_cols
    return df

counties = pd.read_csv('/Users/akshaygowrish/Downloads/US_counties/uscounties.csv')
names = counties['county']
fips = counties['county_fips']
ga_counties = []
for i in range(len(fips)):
    if int(fips[i]) > 13000 and int(fips[i]) < 14000:
        ga_counties.append(names[i])
ga_counties.sort()
parent = '/Users/akshaygowrish/Downloads'
dest_folder = parent + '/GA_Nov_Data'

full_table = pd.DataFrame()

for i in range(NUM_COUNTIES):
    print(ga_counties[i])
    dest = dest_folder + '/_' + ga_counties[i] + '_'
    dest = dest + str(i)
    dest2 = dest + '_nov.xlsx'
    dest = dest + '_nov.xls'
    # print(dest)
    df0 = pd.read_excel(dest,sheet_name=0,header=3)
    contests = ['President','Senate','SenateSpecial','PublicService1','PublicService4']
    df = pd.read_excel(dest,sheet_name=1)
    for j in range(2,7):
        dfcandidates = pd.read_excel(dest,sheet_name=j,header=1)
        dfresults = pd.read_excel(dest,sheet_name=j,header=2)
        dfresults = process_race_sheet(dfcandidates,dfresults,contests[j-2])
        df = pd.concat([df,dfresults],axis=1)
    df = process_county_sheet(df,i)
    full_table = pd.concat([full_table,df])

dem = full_table['Total_Votes_Trump_Rep_President'].tolist()
rep = full_table['Total_Votes_Biden_Dem_President'].tolist()
lib = full_table['Total_Votes_Jorgensen_Lib_President'].tolist()
print(np.sum(dem),np.sum(rep),np.sum(lib))
dem = full_table['Total_Votes_Ossoff_Dem_Senate'].tolist()
rep = full_table['Total_Votes_Perdue_Rep_Senate'].tolist()
lib = full_table['Total_Votes_Hazel_Lib_Senate'].tolist()
print(np.sum(dem),np.sum(rep),np.sum(lib))
full_table.to_csv(dest_folder + "/ga_nov2020_results.csv")