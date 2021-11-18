import pandas as pd


def groupby(df, accounts, show, frequency, group_by='grouper'):
    accounts = [accounts] if isinstance(accounts, int) else accounts
    data = df.loc[df['Konto'].isin(accounts)]

    if group_by == 'grouper':
        if 'Spend' in show:
            return data.groupby(
                pd.Grouper(freq=frequency, key='Bilagsdato'),
                observed=True)['Sum'].sum().to_dict()

        elif 'Faktura' in show:
            return data.groupby(
                pd.Grouper(freq=frequency, key='Bilagsdato'),
                observed=True)['Partner'].count().to_dict()
        else:
            return data.groupby(
                pd.Grouper(freq=frequency, key='Bilagsdato'),
                observed=True)['Partner'].nunique().to_dict()

    elif 'Spend' in show:
        return (
            data
            .groupby(group_by, observed=True)
            [['Sum']]
            .sum())

    elif 'Faktura' in show:
        return (
            data
            .drop_duplicates(subset=['Partner', 'Referansenummer'])
            .groupby(group_by, observed=True)[['Partner']]
            .count())
    else:
        return (
            data
            .groupby(group_by, observed=True)[['Partner']]
            .nunique())
