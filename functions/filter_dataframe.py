import pandas as pd


def filter_dataframe(
    df: pd.DataFrame,
    years: list,
    locations: list,
    frequency: str
) -> pd.DataFrame:
    """
    Filters the dataframe by the inputs supplied by the user
    and returns a filtered dataframe.
    """

    max_date = df.query('Bilagstype == "J_type"')['Bilagsdato'].max()

    f1 = df['Bilagsdato'].dt.year.isin(years)
    f2 = df['Lokasjon'].isin(locations)
    f3 = df['Bilagsdato'] <= max_date
    f4 = df['Bilagstype'] == 'J_type'

    new_df = df.loc[f1 & f2 & f3 & f4].copy(deep=True)

    if frequency == 'Q' and all([years, locations]):

        # If the user wants quarterly numbers we only want to
        # return full quarters. The dictionary shows the month-numbers
        # to exclude based on current month.
        months_table = {
            1: [1],
            2: [1, 2],
            3: [None],
            4: [4],
            5: [4, 5],
            6: [None],
            7: [7],
            8: [7, 8],
            9: [None],
            10: [10],
            11: [10, 11],
            12: [None],
        }

        new_df['Måned'] = new_df['Bilagsdato'].dt.month
        max_year = new_df['År'].max()
        # Find the highest month number in the current year.
        max_month = new_df.query('År == @max_year')['Måned'].max()
        month_lookup = months_table[max_month]

        df1 = new_df.query('År != @max_year')
        # include the transactions in the current year but not those
        # in the current quarter
        df2 = new_df.query('År == @max_year and not Måned.isin(@month_lookup)')

        new_df = df2.append(df1)

    return new_df
