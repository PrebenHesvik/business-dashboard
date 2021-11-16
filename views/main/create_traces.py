from collections import namedtuple
import pandas as pd
from typing import List
from functions import filter_dataframe
from load_datasets import transactions, payment_terms


def change_format_to_date(df: pd.DataFrame):
    return [x.to_pydatetime().date() for x in df.columns]


def spend_trace(df: pd.DataFrame, frequency: str):
    """Spend amount in each period"""
    trace = (
        df
        .groupby(pd.Grouper(freq=frequency, key='Bilagsdato'))
        [['Sum']]
        .sum()
        .transpose()
    )
    trace.columns = change_format_to_date(trace)
    return trace


def invoices_trace(df: pd.DataFrame, frequency: str):
    """Number of invoices in each period"""
    trace = (
        df
        .drop_duplicates(subset=['Partner', 'Referansenummer'])
        .groupby(pd.Grouper(freq=frequency, key='Bilagsdato'))
        [['Partner']]
        .count()
        .transpose()
    )
    trace.columns = change_format_to_date(trace)
    return trace


def avg_invoice_amount_trace(
        spend_trace: pd.DataFrame,
        invoices_trace: pd.DataFrame):
    """Average invoice amount in each period"""
    data = spend_trace.iloc[0].div(invoices_trace.iloc[0])
    return pd.DataFrame(data).transpose()


def num_unique_suppliers_trace(df: pd.DataFrame, frequency: str):
    """Number of unique suppliers in each period"""
    trace = (
        df
        .groupby(pd.Grouper(freq=frequency, key='Bilagsdato'))
        [['Partner']]
        .nunique()
        .transpose()
    )
    trace.columns = change_format_to_date(trace)
    return trace


def supplier_spend_ranked(df: pd.DataFrame, limit: int):
    """Suppliers with whom we have the highest spend"""
    return (
        df
        .groupby('Partner')[['Sum']]
        .sum()
        .sort_values('Sum', ascending=False)
        .head(int(limit))
        .sort_values('Sum')
    )


def supplier_invoices_ranked(df: pd.DataFrame, limit: int):
    return (
        df
        .drop_duplicates(subset=['Partner', 'Referansenummer'])
        .groupby('Partner')
        [['Bilagstype']]
        .count()
        .sort_values('Bilagstype', ascending=False)
        .head(int(limit))
        .sort_values('Bilagstype', ascending=True)
    )


def category_spend_ranked(df: pd.DataFrame, limit: int):
    return (
        df
        .groupby('Kontobeskrivelse')
        [['Sum']]
        .sum()
        .sort_values('Sum', ascending=False)
        .head(int(limit))
        .sort_values('Sum')
    )


def category_invoices_ranked(df: pd.DataFrame, limit: int):
    return (
        df.drop_duplicates(subset=['Partner', 'Referansenummer'])
        .groupby('Kontobeskrivelse')[['Partner']]
        .count()
        .sort_values('Partner', ascending=False)
        .head(int(limit))
        .sort_values('Partner')
    )


def weighted_avg_payment_terms(df: pd.DataFrame, frequency: str):
    # 1. pivot table: sum of invoice sums for each time period, grouped
    # by payment terms
    pmt_terms = (
        df
        .drop_duplicates(
            subset=['Partner', 'Referansenummer'])
        .pivot_table(
            index='Payment Terms',
            columns=pd.Grouper(freq=frequency, key='Bilagsdato'),
            values='Sum', aggfunc='sum')
        .fillna(0)
    )

    # 2. divide each value in each column sum of column values
    pmt_terms = pmt_terms.div(pmt_terms.sum(), axis='columns')

    # 3. multiply index with corresponding column value for each columns
    # the calculate sum of each colums.
    weighted_pmt_terms = (
        pmt_terms
        .multiply(pmt_terms.index, axis='index')
        .sum()
    )

    col_name = ['Weighted Avg Payment Terms']
    trace = pd.DataFrame(weighted_pmt_terms, columns=col_name).transpose()
    trace.columns = change_format_to_date(trace)
    return trace


def create_traces(
    years: list[int],
    locations: list[str],
    frequency: str,
    limit: int
):
    # filter dataframe
    df = filter_dataframe(
        transactions,
        years,
        locations,
        frequency,
    )
    df['Payment Terms'] = df['Partner'].map(payment_terms)

    spend = spend_trace(df, frequency)
    invoices = invoices_trace(df, frequency)
    avg_invoice_amount = avg_invoice_amount_trace(spend, invoices)
    unique_suppliers = num_unique_suppliers_trace(df, frequency)
    supplier_spend = supplier_spend_ranked(df, limit)
    supplier_invoices = supplier_invoices_ranked(df, limit)
    category_spend = category_spend_ranked(df, limit)
    category_invoices = category_invoices_ranked(df, limit)
    weighted_avg_pmt_terms = weighted_avg_payment_terms(df, frequency)

    Trace = namedtuple('Trace', 'data title chart_type dynamic_height')

    return [
        Trace(spend, 'spend', 'both', False),
        Trace(invoices, 'antall faktura', 'both', False),
        Trace(avg_invoice_amount, 'gj.snitt fakturasum', 'both', False),
        Trace(unique_suppliers, 'antall benyttede leverandører', 'both', False),
        Trace(weighted_avg_pmt_terms,
              'vektede betalingsbetingelser', 'both', False),
        #Trace(rolling_spend_per_cat, 'Spend per kategori', 'both', False),
        Trace(supplier_spend, 'leverandører - spend', 'bar', True),
        Trace(supplier_invoices, 'leverandører - antall faktura', 'bar', True),
        Trace(category_spend, 'kategori - spend', 'bar', True),
        Trace(category_invoices, 'kategori - antall faktura', 'bar', True),
    ]
