import shutil, os
import pandas as pd
import xlrd
# from xml2xlsx import xml2xlsx
import xml.etree.ElementTree as ET
import numpy as np

NUM_COUNTIES = 155
vote_types = ['Election_Day_Votes','Advanced_Voting_Votes','Absentee_by_Mail_Votes','Provisional_Votes','Total_Votes']


def process_county_sheet(df,i):
    id = 'County'
    if 'County' not in df.columns:
        id = 'Precinct'
    length = len(df[id].tolist())
    county_list = [ga_counties[i] for j in range(length)]
    df = df.rename(columns={id:"Precinct"})
    df['County'] = county_list
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
excluded = ['Camden','Chattooga','Grady','Greene']
ga_counties = []
for i in range(len(fips)):
    if int(fips[i]) > 13000 and int(fips[i]) < 14000 and names[i] not in excluded:
        ga_counties.append(names[i])
ga_counties.sort()
parent = '/Users/akshaygowrish/Documents'
dest_folder = parent + '/surf2021/Data'
source_folder = '/Users/akshaygowrish/Downloads/'

full_table = pd.DataFrame()



for i in range(NUM_COUNTIES):
    print(ga_counties[i])
    dest = dest_folder + '/_' + ga_counties[i] + '_'
    dest = dest + str(i)
    dest = dest + '_jan.xls'
    source_file = dest_folder + '/_' + ga_counties[i] + '_' + str(i) + '_jan.xls'
    df0 = pd.read_excel(dest,sheet_name=0,header=3)
    contests = ['Senate','SenateSpecial','PublicService4']
    df = pd.read_excel(dest,sheet_name=1)
    for j in range(2,5):
        dfcandidates = pd.read_excel(dest,sheet_name=j,header=1)
        dfresults = pd.read_excel(dest,sheet_name=j,header=2)
        dfresults = process_race_sheet(dfcandidates,dfresults,contests[j-2])
        df = pd.concat([df,dfresults],axis=1)
    df = process_county_sheet(df,i)
    full_table = pd.concat([full_table,df])

county = full_table['County']
full_table.drop(labels=['County'], axis=1,inplace = True)
full_table.insert(0, 'County', county)
print(full_table.columns)
dem = full_table['Total_Votes_Ossoff_Dem_Senate'].tolist()
rep = full_table['Total_Votes_Perdue_Rep_Senate'].tolist()
print(np.sum(dem),np.sum(rep))
dem = full_table['Total_Votes_Warnock_Dem_SenateSpecial'].tolist()
rep = full_table['Total_Votes_Loeffler_Rep_SenateSpecial'].tolist()
print(np.sum(dem),np.sum(rep))

rv = full_table['Voter Turnout'].tolist()
count = 0
anticount = 0
for item in rv:
    if item == '0.00 %':
        count += 1
    else:
        anticount += 1

# full_table.to_csv(dest_folder + "/ga_jan2021_results.csv")