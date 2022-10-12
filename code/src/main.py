import pandas as pd



"""1.1"""
def part_1():
    cases_train = pd.read_csv('../data/cases_2021_train.csv')
    cases_train.groupby('outcome').size()

    cases_train.loc[cases_train['outcome'].isin(['Recovered', 'recovered']), 'outcome_group'] = 'recovered'

    cases_train.loc[cases_train['outcome'].isin(
        ['Dead', 'Death', 'Deceased', 'Died', 'death', 'died']), 'outcome_group'] = 'deceased'

    cases_train.loc[cases_train['outcome'].isin(['Alive', 'Receiving Treatment', 'Stable', 'Under treatment',
                                                 'recovering at home 03.03.2020', 'released from quarantine',
                                                 'stable', 'stable condition']), 'outcome_group'] = 'nonhospitalized'

    cases_train.loc[
        cases_train['outcome'].isin(['Discharged', 'Discharged from hospital', 'Hospitalized', 'critical condition',
                                     'discharge', 'discharged']), 'outcome_group'] = 'hospitalized'

    cases_train.groupby('outcome_group').size()

    cases_train = cases_train.drop(['outcome'], axis=1)

    cases_train.to_csv('../data/cases_2021_train.csv')


def main():
    part_1()


if __name__ == "__main__":
    main()
