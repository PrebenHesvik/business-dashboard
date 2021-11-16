import pandas as pd
from .transpose_sort_delete_func import transpose_sort_delete


def pivot(df, accounts, show, frequency, column):
    """
    Filters a dataframe by one or more accounts and
    returns a pivot table of periodic spend,
    number of invoices or number of suppliers.
    The pivot table gets returned as a dictionary
    but is passed to function `transpose_sort_delete`
    where it is turned into a DataFrame and sorted by
    descending values.

    :param df: DataFrame to filter
    :type df: DataFrame
    :param accounts: the accounts to filter by
    :type accounts: int, list
    :param show: the metric to show (spend, invoices, supplier count)
    :type show: str
    :param frequency: weekly, monthly, yearly aggregation
    :type frequency: str
    :param column: the dataframe column to base the pivot_table on
    :type column: str
    :return: returns a DataFrame
    :rtype: DataFrame
    """

    accounts = [accounts] if isinstance(accounts, int) else accounts
    data = df.loc[df['Konto'].isin(accounts)]

    if 'Spend' in show:
        data = data.pivot_table(
            columns=column,
            index=pd.Grouper(freq=frequency, key='Bilagsdato'),
            values='Sum', aggfunc='sum').to_dict()

    elif 'Faktura' in show:
        data = (data
                .drop_duplicates(
                    subset=['Partner', 'Referansenummer'])
                .pivot_table(
                    columns=column,
                    index=pd.Grouper(freq=frequency, key='Bilagsdato'),
                    values='Partner', aggfunc='count').to_dict())

    else:
        data = data.pivot_table(
            columns=column,
            index=pd.Grouper(freq=frequency, key='Bilagsdato'),
            values='Partner', aggfunc=pd.Series.nunique).to_dict()

    return transpose_sort_delete(data)
