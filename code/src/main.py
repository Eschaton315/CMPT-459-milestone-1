import pandas as pd
import numpy as np

cases_train = pd.read_csv('../data/cases_2021_train.csv')
cases_test = pd.read_csv('../data/cases_2021_test.csv')
location = pd.read_csv('../data/location_2021.csv')

if 'outcome' in cases_train:
    cases_train.groupby('outcome').size()

    """Creating outcome_group values"""
    cases_train.loc[cases_train['outcome'].isin(['Recovered', 'recovered']), 'outcome_group'] = 'recovered'

    cases_train.loc[cases_train['outcome'].isin(
        ['Dead', 'Death', 'Deceased', 'Died', 'death', 'died']), 'outcome_group'] = 'deceased'

    cases_train.loc[cases_train['outcome'].isin(['Alive', 'Receiving Treatment', 'Stable', 'Under treatment',
                                                 'recovering at home 03.03.2020', 'released from quarantine',
                                                 'stable',
                                                 'stable condition']), 'outcome_group'] = 'nonhospitalized'

    cases_train.loc[
        cases_train['outcome'].isin(['Discharged', 'Discharged from hospital', 'Hospitalized', 'critical condition',
                                     'discharge', 'discharged']), 'outcome_group'] = 'hospitalized'

    cases_train.groupby('outcome_group').size()

    """Removing outcome column"""
    cases_train = cases_train.drop(['outcome'], axis=1)

    cases_train.to_csv('../data/cases_2021_train.csv')

    print("task-1.1 complete")
else:
    print("'outcome' column already removed")


#1.4
#cleaning train data set
#drop rows with missing age values
cases_train.dropna(subset = ['age'], inplace = True)
cases_test.dropna(subset = ['age'], inplace = True)

ratio_count = 0
for x in cases_train.index:
    age = cases_train.loc[x,'age']
    if age[1:2] == ".":
        age = int(age[0:1])
    elif age[2:3] == ".":
        age = int(age[0:2])
    elif age[1:2] == "-":
        age = int(age[0:1])
    elif age[2:3] == "-":
        age = int(age[0:2])
    elif age[-1] == "h":
        age = int(age[0:1])
    else:
        age = int(age)
    cases_train.loc[x,'age'] = age

    if cases_train.loc[x,'sex'] != 'male' and cases_train.loc[x,'sex'] != 'female':
        if ((ratio_count % 3) == 0):
            cases_train.loc[x,'sex'] = 'female'
        else:
            cases_train.loc[x,'sex'] = 'male'
        ratio_count += 1

#cleaning test data set
ratio_count = 0
for x in cases_test.index:
    age = cases_test.loc[x,'age']
    if age[1:2] == ".":
        age = int(age[0:1])
    elif age[2:3] == ".":
        age = int(age[0:2])
    elif age[1:2] == "-":
        age = int(age[0:1])
    elif age[2:3] == "-":
        age = int(age[0:2])
    elif age[-1] == "h":
        age = int(age[0:1])
    else:
        age = int(age)
    cases_test.loc[x,'age'] = age

    if cases_test.loc[x,'sex'] != 'male' and cases_test.loc[x,'sex'] != 'female':
        if ((ratio_count % 3) == 0):
            cases_test.loc[x,'sex'] = 'female'
        else:
            cases_test.loc[x,'sex'] = 'male'
        ratio_count += 1


#1.5
#get rid of outliers values for fatality rate > 100%
for x in location.index:
    if location.loc[x, 'Case_Fatality_Ratio'] > 100:
        location.drop(x, inplace=True)


#1.6
#adding attributes to train data later for combinging with location data
cases_train["Confirmed"] = ''
cases_train["Deaths"] = ''
cases_train["Recovered"] = ''
cases_train["Active"] = ''
cases_train["Incident_Rate"] = ''
cases_train["Case_Fatality_Ratio"] = ''

#adding attributes to test data later for combinging with location data
cases_test["Confirmed"] = ''
cases_test["Deaths"] = ''
cases_test["Recovered"] = ''
cases_test["Active"] = ''
cases_test["Incident_Rate"] = ''
cases_test["Case_Fatality_Ratio"] = ''

#print(cases_train)
#print(cases_train.info())

#clean up country name in location data file
for y in location.index:
    if location.loc[y,'Country_Region'] == 'Korea, South':
        location.loc[y,'Country_Region'] = 'South Korea'
    elif location.loc[y,'Country_Region'] == 'US':
        location.loc[y,'Country_Region'] = 'United States'

#print(location.info())

#get rid of duplicate data for joining data later
country = "place holder 1"
for x in location.index:
    if location.loc[x,'Country_Region'] == country:
        location.drop(x, inplace = True)
    else:
        country = location.loc[x,'Country_Region']

#print(location.info())

#for testing purpose get rid of some data for now
cases_train.dropna(subset = ['additional_information'], inplace = True)

count = 0
for y in cases_train.index:
    for x in location.index:
        if location.loc[x, 'Country_Region'] == cases_train.loc[y, 'country']:
            print(count)
            cases_train.loc[y, 'Confirmed'] = location.loc[x, 'Confirmed']
            cases_train.loc[y, 'Deaths'] = location.loc[x, 'Deaths']
            cases_train.loc[y, 'Recovered'] = location.loc[x, 'Recovered']
            cases_train.loc[y, 'Active'] = location.loc[x, 'Active']
            cases_train.loc[y, 'Incident_Rate'] = location.loc[x, 'Incident_Rate']
            cases_train.loc[y, 'Case_Fatality_Ratio'] = location.loc[x, 'Case_Fatality_Ratio']
            #to check it's actually running
            count += 1
            break
#for testing purpose get rid of some data for now
cases_test.dropna(subset = ['additional_information'], inplace = True)

count = 0
for y in cases_test.index:
    for x in location.index:
        if location.loc[x, 'Country_Region'] == cases_test.loc[y, 'country']:
            print(count)
            cases_test.loc[y, 'Confirmed'] = location.loc[x, 'Confirmed']
            cases_test.loc[y, 'Deaths'] = location.loc[x, 'Deaths']
            cases_test.loc[y, 'Recovered'] = location.loc[x, 'Recovered']
            cases_test.loc[y, 'Active'] = location.loc[x, 'Active']
            cases_test.loc[y, 'Incident_Rate'] = location.loc[x, 'Incident_Rate']
            cases_test.loc[y, 'Case_Fatality_Ratio'] = location.loc[x, 'Case_Fatality_Ratio']
            #to check it's actually running
            count += 1
            break

cases_train.to_csv('cases_2021_test_processed.csv', encoding='utf-8', index=False)
cases_test.to_csv('cases_2021_train_processed.csv', encoding='utf-8', index=False)
