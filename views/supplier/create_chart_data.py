import pandas as pd


def supplier_spend_data(df, frequency, chart_size, ChartData):
    supplier_spend = (
        df
        .groupby(pd.Grouper(freq=frequency, key='Bilagsdato'))[['Sum']]
        .sum()
        .transpose()
        .rename(columns=lambda c: str(c.to_pydatetime().date()))
    )

    return ChartData(
        data=supplier_spend,
        title='spend',
        chart_type='line',
        marker_colors=None,
        orientation='v',
        width=chart_size[0]
    )


def supplier_invoices_data(df, frequency, chart_size, ChartData):
    invoices = (
        df
        .drop_duplicates(
            subset=['Partner', 'Referansenummer'])
        .groupby(pd.Grouper(
            freq=frequency,
            key='Bilagsdato'))[['Partner']]
        .count().transpose()
        .rename(columns=lambda c: str(c.to_pydatetime().date()))
    )

    return ChartData(
        data=invoices,
        title='antall faktura',
        chart_type='line',
        marker_colors=None,
        orientation='v',
        width=chart_size[0]
    )


def spend_grouped_by_location(df, frequency, chart_size, ChartData):
    spend_loc = (
        df
        .pivot_table(
            index='Lokasjon',
            columns=pd.Grouper(freq=frequency, key='Bilagsdato'),
            values='Sum',
            aggfunc='sum').transpose()
        .rename(index=lambda c: str(c.to_pydatetime().date()))
    )

    return ChartData(
        data=spend_loc,
        title='spend per fabrikk',
        chart_type='bar',
        marker_colors=None,
        orientation='v',
        width=chart_size[0]
    )

def invoice_grouped_by_location(df, frequency, chart_size, ChartData):
    inv_loc = (
            df
            .drop_duplicates(
                subset=['Partner', 'Referansenummer'])
            .pivot_table(
                index='Lokasjon',
                columns=pd.Grouper(freq=frequency, key='Bilagsdato'),
                values='Partner',
                aggfunc='count')
            .transpose()
            .rename(index=lambda c: str(c.to_pydatetime().date()))
        )

    return ChartData(
        data=inv_loc, title='antall faktura per fabrikk',
        chart_type='bar', marker_colors=None,
        orientation='v', width=chart_size[0])

def spend_grouped_by_account(df, frequency, chart_size, ChartData, return_just_pivot=False):
    spend_acct = (
        df
        .pivot_table(
            index='Kontobeskrivelse',
            columns=pd.Grouper(freq=frequency, key='Bilagsdato'),
            values='Sum',
            aggfunc='sum')
        .fillna(0)
    )

    spend_acct_sorted = (
        spend_acct
        .assign(total=spend_acct.sum(axis='columns'))
        .sort_values('total', ascending=False)
        .drop(columns=['total'])
        .head(5)
        .transpose()
        .rename(index=lambda c: str(c.to_pydatetime().date()))
    )
    if return_just_pivot:
        return spend_acct_sorted

    return ChartData(
            data=spend_acct_sorted, title='spend per konto',
            chart_type='bar', marker_colors=None,
            orientation='v', width=chart_size[1])

def num_invoices_grouped_by_account(df, frequency, chart_size, ChartData):
    inv_acct = (
        df
        .drop_duplicates(
            subset=['Partner', 'Referansenummer'])
        .pivot_table(
            index='Kontobeskrivelse',
            columns=pd.Grouper(freq=frequency, key='Bilagsdato'),
            values='Sum',
            aggfunc='sum')
        .fillna(0))

    inv_acct_sorted = (
        inv_acct
        .assign(total=inv_acct.sum(axis='columns'))
        .sort_values('total', ascending=False)
        .drop(columns=['total'])
        .head(5)
        .transpose()
        .rename(index=lambda c: str(c.to_pydatetime().date()))
    )

    return ChartData(
        data=inv_acct_sorted, title='antall faktura per konto',
        chart_type='bar', marker_colors=None,
        orientation='v', width=chart_size[1])
