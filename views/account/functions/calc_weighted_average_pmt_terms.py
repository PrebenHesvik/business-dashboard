import pandas as pd
from load_datasets import payment_terms

def supplier_pmt_terms(df, account):
    """
    Returns a DataFrame consisiting of supplier payment
    terms for a chosen account. The number of suppliers
    to calculate the payment terms for is capped at 10.

    :param df: DataFrame
    :type df: DataFrame
    :param account: account to filter df on
    :type account: str
    :return: returns a DataFrame
    :rtype: DataFrame
    """

    # filter by account and valid IFS partner ID
    data = df.loc[df['Konto'] == account]
    data = data.loc[data['Partner'].str.len() > 0]

    # map each PartnerID to a payment term
    data['Payment Terms'] = data['Partner'].map(payment_terms)

    # return payment terms of the 10 suppliers with the
    # highest invoice amounts
    return (
        data
        .groupby('Partner').agg(
            Sum=pd.NamedAgg('Sum', 'sum'),
            pmt_term=pd.NamedAgg('Payment Terms', 'last'))
        .sort_values('Sum', ascending=False)
        .drop(columns=['Sum'])
        .transpose()
    )

def wa_pmt_terms(df, accounts, frequency):
    """
    Returns weighted average payment terms
    for one or more accounts combined,
    for the selected number of periods.

    :param df: DataFrame
    :type df: DataFrame
    :param accounts: accounts to calculate the weighted
                     average payment terms on.
    :type accounts: int, list
    :param frequency: choose between yearly, quarterly,
                      or monthly aggregations.
    :type frequency: str
    :return: returns a weighted average payment term for
             each period.
    :rtype: dict
    """

    # filter by account and valid IFS partner ID
    accounts = [accounts] if isinstance(accounts, int) else accounts
    data = df.loc[df['Konto'].isin(accounts)]
    data = data.loc[df['Partner'].str.len() > 0]

    # map each PartnerID to a payment term
    data['Payment Terms'] = data['Partner'].map(payment_terms)

    # create pivot table consisting of sum of invoice sums
    # grouped by payment terms and time periods
    pivot = data.pivot_table(
        index='Payment Terms',
        columns=pd.Grouper(freq=frequency, key='Bilagsdato'),
        values='Sum', aggfunc='sum').fillna(0)

    # divide each column value by the sum of the
    # corresponding column values
    pivot = pivot.div(pivot.sum(), axis='columns')

    # multiply each value by the corresponding payment term
    pivot = pivot.multiply(pivot.index, axis='index')

    # return weighted payment terms for each time period
    return pivot.sum().to_dict()
