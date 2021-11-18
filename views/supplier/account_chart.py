import pandas as pd

from chart_configs import (
    single_color,
    highlight_color,
)

def account_chart(df, account, supplier, keyword='Spend'):
    tbl = df.loc[df['Kontobeskrivelse'] == account]

    if keyword == 'Spend':
        tbl_grp = (
            tbl
            .groupby('Partner')[['Sum']]
            .sum()
            .sort_values('Sum', ascending=False)
            .head(n=10)
            .sort_values('Sum', ascending=True))

        tbl_grp['Sum'] = tbl_grp['Sum'].round(0)

        supplier_value = (
            tbl.loc[tbl['Partner'] == supplier]
            [['Sum']]
            .sum()
            .values[0])

    else:
        tbl_grp = (
            tbl
            .drop_duplicates(subset=['Partner', 'Referansenummer'])
            .groupby('Partner')[['Referansenummer']]
            .count()
            .sort_values('Referansenummer', ascending=False)
            .head(n=10)
            .sort_values('Referansenummer', ascending=True))

        supplier_value = (
            tbl.loc[tbl['Partner'] == supplier]
            .drop_duplicates(subset=['Partner', 'Referansenummer'])
            [['Partner']]
            .count()
            .values[0])

    if supplier not in tbl_grp.index.tolist():
        if keyword == 'Spend':
            d = {'Sum': [supplier_value]}
        else:
            d = {'Partner': [supplier_value]}
        new_df = pd.DataFrame(d, index=[supplier], dtype='int')
        tbl_grp = new_df.append(tbl_grp)

    title = f'{keyword} {account}'.upper().replace('KJØP', '')
    colors = [
        single_color[0] if x != tbl_grp.index.get_loc(supplier)
        else highlight_color
        for x in range(tbl_grp.size)
    ]

    return tbl_grp, title, colors