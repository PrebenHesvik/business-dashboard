import pandas as pd
import datetime as dt
import numpy as np


def import_contracts(partner_map, contracts):
    # map supplier IDs to supplier names
    data = pd.read_excel(partner_map, sheet_name='tendsign')
    partner_map = dict(zip(data['Leverandør'], data['Partner']))

    # import contracts and filter out expired contracts
    df = pd.read_excel(contracts)
    df = df[df['Sluttdato'] > dt.datetime.today()]
    df.drop_duplicates(subset=['Leverandør'], inplace=True)
    df['Partner'] = df['Leverandør'].map(partner_map)
    return df[['Leverandør', 'Partner']]


def import_supplier_list(ifs_path):
    usecols = ['Payment Terms', 'Supplier ID', 'Supplier Name']
    df = pd.read_excel(ifs_path, sheet_name='data', usecols=usecols)

    pmt_dict = {
        '02': 45, 'F45': 60, 'F15': 30, 'F30': 45,
        'F28': 43, 'F20': 35,
    }

    df['Payment Terms'] = np.where(df['Payment Terms'].isin(pmt_dict.keys()),
                                   df['Payment Terms'].map(pmt_dict),
                                   df['Payment Terms'])

    df['Payment Terms'] = df['Payment Terms'].astype('int')

    return dict(zip(df['Supplier ID'], df['Payment Terms']))


# def import_invoices(path):
#     usecols = ['Bilagsdato', 'Partner', 'Partnerbeskrivelse',
#                'Sum', 'Referansenummer']

#     df = pd.read_excel(path, usecols=usecols)

#     df.drop_duplicates(inplace=True)

#     return df
