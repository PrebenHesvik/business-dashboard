import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
import io


def import_data(cols: list, filename: str, decoded) -> list | pd.DataFrame:
    """
    Returns the dataframe if all required columns are 
    present or else the missing columns are returned.
    """
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(io.StringIO(
            decoded.decode('latin1')), low_memory=False, sep=';', encoding='latin1')

    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))

    # Check that thew new file contains correct column names:
    missing_cols = [c for c in cols if c not in df.columns]

    # Return missing cols list if it contains any items
    return missing_cols or df[cols]


def clean_account_descriptions_and_add_cols(df: pd.DataFrame) -> tuple[dict, dict, dict]:
    """
    Create a temp dataframe that contains two added columns; 'Avdeling' and 'Lokasjon'
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


def import_and_clean_transactions(filename: str, decoded) -> pd.DataFrame:
    """Cleans the transaction file"""
    cols = [
        'Bil.type', 'Bilagsdato', 'Beskrivelse av Konto',
        'Beskrivelse av Kost.sted', 'Beskrivelse av Partner',
        'Partner', 'Konto', 'Beløp', 'Kost.sted',
        'Referansenummer', 'Bil.nr', 'Linjenr'
    ]

    df = import_data(cols, filename, decoded)
    if isinstance(df, list):
        return df

    # Rename columns
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

    # Remove unrelated "bilagstyper"
    reject = ['MD', '2', '6', 'A', 'F', 'R', 'U', 'Q']
    df = df.loc[~df['Bilagstype'].isin(reject)]

    # Change dtype of 'Bilagsdato
    df['Bilagsdato'] = pd.to_datetime(df['Bilagsdato'])

    # Add column for year
    df['År'] = df['Bilagsdato'].dt.year

    # Convert type if column is of type object
    # This seems to be a bug when exporting the
    # data from the ERP-system.
    if is_string_dtype(df['Sum']):
        df['Sum'] = df['Sum'].str.replace(',', '.').astype('float')

    # Clean up column 'Kostnadsted', and add columns 'Lokasjon', 'Avdeling'
    cost_desc, loc_map, dept_map = clean_account_descriptions_and_add_cols(df)
    df['Koststedbeskrivelse'] = df['Kostnadsted'].map(cost_desc)
    df['Avdeling'] = df['Kostnadsted'].map(dept_map)
    df['Lokasjon'] = df['Kostnadsted'].map(loc_map)

    # Filter locations
    locations = ['Hjørungavåg', 'Hønefoss', 'Skurve']
    df = df.loc[df['Lokasjon'].isin(locations)]

    # Reduce sice of column
    df['Konto'] = df['Konto'].astype(np.int16)

    # Change to string type
    df['Partner'] = df['Partner'].astype('str')

    # Remove invalid partner_nums
    # All nums should start with NO
    df = df[~df['Partner'].str.isdigit()]

    # Change dtype to str
    df['Referansenummer'] = df['Referansenummer'].astype('str')

    # Change dtype to str and add '_type' to each value
    df['Bilagstype'] = df['Bilagstype'].astype('str') + '_type'

    # Change dtypes to save memory
    category_types = ['Koststedbeskrivelse', 'Bilagstype',
                      'Kontobeskrivelse', 'Kostnadsted',
                      'Avdeling', 'Lokasjon']

    for cat in category_types:
        df[cat] = df[cat].astype('category')

    return df


def import_and_clean_supplier_list(filename: str, decoded) -> dict:
    """
    Imports the supplier list and returns a dict of 
    Supplier ID and the associated payment term.
    """
    cols = ['Payment Terms', 'Supplier ID', 'Supplier Name']

    df = import_data(cols, filename, decoded)
    if isinstance(df, list):
        return df

    # Convert some codes in the file to actual numbers
    pmt_dict = {
        '02': 45, 'F45': 60, 'F15': 30,
        'F30': 45, 'F28': 43, 'F20': 35,
    }

    df['Payment Terms'] = np.where(
        df['Payment Terms'].isin(pmt_dict.keys()),
        df['Payment Terms'].map(pmt_dict),
        df['Payment Terms'])

    # Change dtype of col to int
    df['Payment Terms'] = df['Payment Terms'].astype('int')

    return dict(zip(df['Supplier ID'], df['Payment Terms']))
