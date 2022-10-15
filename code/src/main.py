import pandas as pd
import numpy as np

cases_train = pd.read_csv('../data/cases_2021_train.csv')
cases_test = pd.read_csv('../data/cases_2021_test.csv')
location = pd.read_csv('../data/location_2021.csv')

# 1.1

if 'outcome' in cases_train:
    cases_train.groupby('outcome').size()

    # Creating outcome_group values
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

    # Removing outcome column
    cases_train = cases_train.drop(['outcome'], axis=1)

    cases_train.to_csv('../data/cases_2021_train.csv')

    print("task-1.1 complete")
else:
    print("'outcome' column already removed")

# 1.4
# cleaning train data set
# drop rows with missing age values
cases_train.dropna(subset=['age'], inplace=True)
cases_test.dropna(subset=['age'], inplace=True)

ratio_count = 0
for x in cases_train.index:
    age = cases_train.loc[x, 'age']
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
    cases_train.loc[x, 'age'] = age

    if cases_train.loc[x, 'sex'] != 'male' and cases_train.loc[x, 'sex'] != 'female':
        if (ratio_count % 3) == 0:
            cases_train.loc[x, 'sex'] = 'female'
        else:
            cases_train.loc[x, 'sex'] = 'male'
        ratio_count += 1

# cleaning test data set
ratio_count = 0
for x in cases_test.index:
    age = cases_test.loc[x, 'age']
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
    cases_test.loc[x, 'age'] = age

    if cases_test.loc[x, 'sex'] != 'male' and cases_test.loc[x, 'sex'] != 'female':
        if (ratio_count % 3) == 0:
            cases_test.loc[x, 'sex'] = 'female'
        else:
            cases_test.loc[x, 'sex'] = 'male'
        ratio_count += 1

# 1.5
for x in location.index:
    confirmed = location.loc[x, 'Confirmed']
    deaths = location.loc[x, 'Deaths']
    recovered = location.loc[x, 'Recovered']
    active = location.loc[x, 'Active']
# get rid of outliers data for fatality rate > 100%
    if location.loc[x, 'Case_Fatality_Ratio'] > 100:
        location.drop(x, inplace=True)
# get rid of invalid data where numbers don't add up
    elif (deaths + recovered + active) != confirmed:
        location.drop(x, inplace=True)

# drop data where ages are not in valid range
for x in cases_test.index:
    if cases_test.loc[x, 'age'] < 0:
        cases_test.drop(x, inplace=True)
    elif cases_test.loc[x, 'age'] > 120:
        cases_test.drop(x, inplace=True)

for x in cases_train.index:
    if cases_train.loc[x, 'age'] < 0:
        cases_train.drop(x, inplace=True)
    elif cases_train.loc[x, 'age'] > 120:
        cases_train.drop(x, inplace=True)

# 1.6
# adding attributes to train data later for combining with location data
cases_train["Confirmed"] = ''
cases_train["Deaths"] = ''
cases_train["Recovered"] = ''
cases_train["Active"] = ''
cases_train["Incident_Rate"] = ''
cases_train["Case_Fatality_Ratio"] = ''

# adding attributes to test data later for combining with location data
cases_test["Confirmed"] = ''
cases_test["Deaths"] = ''
cases_test["Recovered"] = ''
cases_test["Active"] = ''
cases_test["Incident_Rate"] = ''
cases_test["Case_Fatality_Ratio"] = ''

# clean up country name in location data file
for y in location.index:
    if location.loc[y, 'Country_Region'] == 'Korea, South':
        location.loc[y, 'Country_Region'] = 'South Korea'
    elif location.loc[y, 'Country_Region'] == 'US':
        location.loc[y, 'Country_Region'] = 'United States'

# imputing missing country values with province if it applies
cases_train['country'] = cases_train['country'].fillna(cases_train['province'] + "*")
cases_test['country'] = cases_test['country'].fillna(cases_test['province'] + "*")

# get rid of duplicate data for joining data later
country = "aCountry"
for x in location.index:
    if location.loc[x, 'Country_Region'] == country:
        location.drop(x, inplace=True)
    else:
        country = location.loc[x, 'Country_Region']

print("Joining cases_train with Location...")
for y in cases_train.index:
    for x in location.index:
        if location.loc[x, 'Country_Region'] == cases_train.loc[y, 'country']:
            cases_train.loc[y, 'Confirmed'] = location.loc[x, 'Confirmed']
            cases_train.loc[y, 'Deaths'] = location.loc[x, 'Deaths']
            cases_train.loc[y, 'Recovered'] = location.loc[x, 'Recovered']
            cases_train.loc[y, 'Active'] = location.loc[x, 'Active']
            cases_train.loc[y, 'Incident_Rate'] = location.loc[x, 'Incident_Rate']
            cases_train.loc[y, 'Case_Fatality_Ratio'] = location.loc[x, 'Case_Fatality_Ratio']
            break
print("Done")

print("Joining cases_test with Location...")
for y in cases_test.index:
    for x in location.index:
        if location.loc[x, 'Country_Region'] == cases_test.loc[y, 'country']:
            cases_test.loc[y, 'Confirmed'] = location.loc[x, 'Confirmed']
            cases_test.loc[y, 'Deaths'] = location.loc[x, 'Deaths']
            cases_test.loc[y, 'Recovered'] = location.loc[x, 'Recovered']
            cases_test.loc[y, 'Active'] = location.loc[x, 'Active']
            cases_test.loc[y, 'Incident_Rate'] = location.loc[x, 'Incident_Rate']
            cases_test.loc[y, 'Case_Fatality_Ratio'] = location.loc[x, 'Case_Fatality_Ratio']
            break
print("Done")

cases_train.to_csv('../results/cases_2021_test_processed.csv', encoding='utf-8', index=False)
cases_test.to_csv('../results/cases_2021_train_processed.csv', encoding='utf-8', index=False)
location.to_csv('../results/location_2021_processed.csv', encoding='utf-8', index=False)

# remove above post 1.7

# 1.7

print("Creating Features csv...")

# getting files again
cases_train = pd.read_csv('../results/cases_2021_train_processed.csv')
cases_test = pd.read_csv('../results/cases_2021_test_processed.csv')

# removing unnamed rows
cases_train = cases_train.loc[:, ~cases_train.columns.str.contains('^Unnamed')]
cases_test = cases_test.loc[:, ~cases_test.columns.str.contains('^Unnamed')]

pd.set_option('display.max_columns', None)

# removing column that are not considered relevant features for classification
cases_train = cases_train.drop(['source', 'latitude', 'longitude', 'Deaths'], axis=1)
cases_test = cases_test.drop(['source', 'latitude', 'longitude', 'Deaths'], axis=1)

# create files for feature csv
cases_train.to_csv('../results/cases_2021_test_processed_features.csv', encoding='utf-8', index=False)
cases_test.to_csv('../results/cases_2021_train_processed_features.csv', encoding='utf-8', index=False)
print("Done")

# print(cases_train.isna().sum())
# print(cases_test.isna().sum())
