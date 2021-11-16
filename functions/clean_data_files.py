import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
import base64
import io


def clean_account_descriptions_and_add_cols(df):
    """
    create a temp dataframe that contains two added columns; 'Avdeling' and 'Lokasjon'
    these two columns are based on substrings from column 'Koststedbeskrivelse'
    thse columns will be added to 'df' using map function.
    also some data cleaning done in this part of the code
    """

    data = df.drop_duplicates(subset=['Kostnadsted'])[
        ['Kostnadsted', 'Koststedbeskrivelse']]

    data['Koststedbeskrivelse'] = (data['Koststedbeskrivelse']
                                   .str.replace('.', ' ')
                                   .str.replace('Sandnes', 'Skurve')
                                   .str.replace('Fabrikk', 'Produksjon')
                                   .str.replace('felles', 'Felles'))

    data['Avdeling'] = data['Koststedbeskrivelse'].str.split().str.get(0)

    data['Lokasjon'] = data['Koststedbeskrivelse'].str.split().str.get(1)

    data['Lokasjon'] = np.where(data['Koststedbeskrivelse'].isin(
        ['HR', 'Økonomi', 'Innkjøp', 'FoU', 'Prosjektfakturering']),
        data['Koststedbeskrivelse'], data['Lokasjon'])

    cost_loc_desc = dict(zip(data['Kostnadsted'], data['Koststedbeskrivelse']))
    location_map = dict(zip(data['Kostnadsted'], data['Lokasjon']))
    department_map = dict(zip(data['Kostnadsted'], data['Avdeling']))

    return cost_loc_desc, location_map, department_map


def import_data(cols, filename, decoded):
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(io.StringIO(
            decoded.decode('latin1')), low_memory=False, sep=';', encoding='latin1')
        # except:
        #     df = pd.read_csv(io.StringIO(
        #         decoded.decode('utf-8')), low_memory=False, sep=',', encoding='utf-8')
        # finally:
        #     print('Could not import')

    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))

    # check that thew new file contains correct column names:
    missing_cols = [c for c in cols if c not in df.columns]

    # return missing cols list if it contains any items
    if missing_cols:
        return missing_cols
    else:
        return df[cols]


def clean_transactions(filename, decoded):
    cols = [
        'Bil.type', 'Bilagsdato', 'Beskrivelse av Konto',
        'Beskrivelse av Kost.sted', 'Beskrivelse av Partner',
        'Partner', 'Konto', 'Beløp', 'Kost.sted',
        'Referansenummer', 'Bil.nr', 'Linjenr'
    ]

    df = import_data(cols, filename, decoded)
    if isinstance(df, list):
        return df

    # rename columns
    rename_map = {
        'Bil.type': 'Bilagstype',
        'Bil.nr': 'Bilagsnummer',
        'Beskrivelse av Konto': 'Kontobeskrivelse',
        'Beskrivelse av Kost.sted': 'Koststedbeskrivelse',
        'Beløp': 'Sum',
        'Beskrivelse av Bærer': 'Bærerbeskrivelse',
        'Beskrivelse av Partner': 'Partnerbeskrivelse',
        'Kost.sted': 'Kostnadsted'}

    df.rename(columns=rename_map, inplace=True)

    # remove unrelated "bilagstyper"
    reject = [ 'MD', '2', '6', 'A',  'F', 'R', 'U', 'Q']
    df = df.loc[~df['Bilagstype'].isin(reject)]

    # change dtype of 'Bilagsdato
    df['Bilagsdato'] = pd.to_datetime(df['Bilagsdato'])

    # add column for year
    df['År'] = df['Bilagsdato'].dt.year

    # convert type if column is of type object
    if is_string_dtype(df['Sum']):
        df['Sum'] = df['Sum'].str.replace(',', '.').astype('float')

    # clean up dolumn 'Kostnadsted', and add columns 'Lokasjon', 'Avdeling'
    cost_desc, loc_map, dept_map = clean_account_descriptions_and_add_cols(df)
    df['Koststedbeskrivelse'] = df['Kostnadsted'].map(cost_desc)
    df['Avdeling'] = df['Kostnadsted'].map(dept_map)
    df['Lokasjon'] = df['Kostnadsted'].map(loc_map)

    locations = ['Hjørungavåg', 'Hønefoss', 'Skurve']
    df = df.loc[df['Lokasjon'].isin(locations)]

    df['Konto'] = df['Konto'].astype(np.int16)

    df['Partner'] = df['Partner'].astype('str')

    df = df[~df['Partner'].str.isdigit()]

    df['Referansenummer'] = df['Referansenummer'].astype('str')

    df['Bilagstype'] = df['Bilagstype'].astype('str') + '_type'

    # change dtypes to save memory
    category_types = ['Koststedbeskrivelse', 'Bilagstype',
                      'Kontobeskrivelse', 'Kostnadsted',
                      'Avdeling', 'Lokasjon']
    for cat in category_types:
        df[cat] = df[cat].astype('category')

    return df


def import_contracts(filename, decoded):

    cols = ['Navn', 'Sluttdato', 'Administrator',
            'Leverandør', 'Referansenummer']

    df = import_data(cols, filename, decoded)
    if isinstance(df, list):
        return df

    for col in cols:
        if col != 'Sluttdato':
            df[col] = df[col].astype('str')

    return df


def import_supplier_list(filename, decoded):
    cols = ['Payment Terms', 'Supplier ID', 'Supplier Name']

    df = import_data(cols, filename, decoded)
    if isinstance(df, list):
        return df

    pmt_dict = {
        '02': 45, 'F45': 60, 'F15': 30,
        'F30': 45, 'F28': 43, 'F20': 35,
    }

    df['Payment Terms'] = np.where(df['Payment Terms'].isin(pmt_dict.keys()),
                                   df['Payment Terms'].map(pmt_dict),
                                   df['Payment Terms'])

    df['Payment Terms'] = df['Payment Terms'].astype('int')

    dictionary = dict(zip(df['Supplier ID'], df['Payment Terms']))
    return dictionary


def inetto_production(filename, decoded):
    cols_0 = [
        'HD-vekt', 'HD-vekt', 'HD-vekt', 'Total Vekt',
        'Total Vekt', 'Total Vekt', 'Timer', 'Timer',
        'Timer'
    ]

    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(io.StringIO(
            decoded.decode('utf-8')), low_memory=False, header=[0, 1], index_col=0)

    else:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded), header=[0, 1], index_col=0)

    missing_cols = [
        col for col in cols_0 if col not in
        df.columns.get_level_values(0).tolist()
    ]

    if missing_cols:
        return missing_cols
    else:
        return df
