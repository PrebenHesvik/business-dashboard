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
