import numpy as np
import math
import sklearn
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
import pandas as pd

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor
import statistics

source = '/Users/akshaygowrish/Documents/surf2021/'
TRAIN_COLUMN = 'Vote_Share_Ossoff_Dem_Senate'
TEST_COLUMN = 'Vote_Share_Biden_Dem_President'
TRAIN_COLUMN = 'Turnout_Senate'
TEST_COLUMN = 'Turnout_President'

df = pd.read_csv(source + '/Data/combined_results_demographics.csv')
df = df.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
columns = list(df.columns)
print(columns[-35])

selected = columns[-66:-46]
selected.append(columns[1])
'''for i in [-8,-7,-6]:
    selected.append(columns[i])
for race in ['SenateSpecial','PublicService1','PublicService4']:
    selected.append('Turnout_' + race)'''
for i in range(1,36):
    selected.append(columns[-i])
print(selected)
X = df[selected]

'''rv_list = df['Registered Voters'].tolist()
for race in ['President','Senate','SenateSpecial','PublicService1','PublicService4']:
    total_race = df['Total_' + race].tolist()
    turnout = []
    for i in range(len(rv_list)):
        if rv_list[i] == 0:
            turnout.append(0)
        else:
            turnout.append(total_race[i]/rv_list[i])
    df['Turnout_' + race] = turnout
print(df)
df.to_csv(source + '/Data/novresults_demographics.csv')'''

y_train = df[TRAIN_COLUMN]
y_test = df[TEST_COLUMN]


med = statistics.median(y_train)
n_scores = [abs(med-y_train[i]) for i in range(len(y_train))]
# report performance
print('MAE: %.3f (%.3f)' % (np.mean(n_scores), np.std(n_scores)))
# random forest for making predictions for regression
from sklearn.ensemble import RandomForestRegressor
# define the model
model = RandomForestRegressor(n_estimators = 1000, random_state = 42)
# fit the model on the whole dataset
model = model.fit(X, y_train)

predictions = model.predict(X)
n_scores = [abs(predictions[i]-y_train[i]) for i in range(len(y_train))]
# report performance
print('MAE: %.3f (%.3f)' % (np.mean(n_scores), np.std(n_scores)))
df2 = pd.DataFrame.from_dict({'orig': y_train.tolist() ,'pred':predictions})

model = model.fit(X, y_train)
predictions = model.predict(X)
n_scores = [abs(predictions[i]-y_test[i]) for i in range(len(y_test))]
# report performance
print('MAE: %.3f (%.3f)' % (np.mean(n_scores), np.std(n_scores)))
df2 = pd.DataFrame.from_dict({'orig': y_test.tolist() ,'pred':predictions})



df2['County'] = df['County'].tolist()
df2['Precinct'] = df['Precinct'].tolist()
df2['diff'] = abs(df2['pred']-df2['orig'])
df2['Registered Voters'] = df['Registered Voters'].tolist()
df2['Ballots Cast'] = df['Ballots Cast'].tolist()
df2['Jan Registered Voters'] = df['Jan Registered Voters'].tolist()
df2['Jan Ballots Cast'] = df['Jan Ballots Cast'].tolist()
df2 = df2.sort_values(['diff'])
print(df2)
diff = df2['diff'].tolist()
county = df2['County'].tolist()
precinct = df2['Precinct'].tolist()
print("Precincts with Largest Deviations from Prediction")
print("County","Precinct","Difference between Prediction and Actual")
for i in range(len(diff)):
    if diff[i] < -0.20:
       print(county[i], precinct[i], diff[i])


# df2 = df2.sort_values(['County'])
print(np.mean(df2['diff'].tolist()),np.std(df2['diff'].tolist()))
df2.to_csv(source+'/Models/results_voterturnout.csv')
'''plt.hist(df2['diff'].tolist(),bins=[-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,0,0.05,0.1,0.15,0.2,0.25,0.3])
plt.xlabel("Difference from Prediction")
plt.ylabel("Count")
plt.savefig(source + "/Figures/expected_biden_histogram")
plt.show()'''
# plt.plot(df2['orig'].tolist())
plt.scatter(df2['orig'].tolist(),df2['pred'].tolist())
# plt.scatter([i for i in range(len(df2['diff'].tolist()))],df2['diff'].tolist())
plt.xlabel("Index of Precinct (Sorted by Number of Biden Votes)")
plt.ylabel("Difference from Prediction")
plt.savefig(source + "/Figures/expected_biden_share")
plt.show()