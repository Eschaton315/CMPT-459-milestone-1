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
