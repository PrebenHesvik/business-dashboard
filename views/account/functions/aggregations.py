from flatten_dict import flatten
from ..components_modules import acct_dict
from .pivot_func import pivot
from .groupby_func import groupby
from .transpose_sort_delete_func import transpose_sort_delete
from .weighted_avg_pmt_terms_func import wa_pmt_terms
from .supplier_pmt_terms_func import supplier_pmt_terms


def find_accounts_to_filter_by(categories):
    cat_1, cat_2, cat_3, cat_4 = categories
    d = None
    if not any([cat_4 == '', cat_4 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]

    elif not any([cat_3 == '', cat_3 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3]
        if not isinstance(accounts, int):
            accounts = flatten(accounts).values()

    elif not any([cat_2 == '', cat_2 == 'Alle']):
        # User has selected an option in selection boxes 1 + 2
        d = acct_dict[cat_1][cat_2]
        accounts = flatten(acct_dict[cat_1][cat_2]).values()

    elif cat_2 == 'Alle':
        # User has selected an option in selection box 1
        d = acct_dict[cat_1]
        accounts = flatten(acct_dict[cat_1]).values()

    elif cat_1 == 'Alle':
        # Page has just been loaded and the user has not
        # selected an option in selection box 1
        d = acct_dict
        accounts = flatten(acct_dict).values()

    return d, accounts


def group_by_supplier(df, show, frequency, categories):
    _, accounts = find_accounts_to_filter_by(categories)
    return pivot(df, accounts, show, frequency, 'Partnerbeskrivelse')


def group_by_location(df, show, frequency, categories):
    _, accounts = find_accounts_to_filter_by(categories)
    return pivot(df, accounts, show, frequency, 'Lokasjon')


def group_by_category(df, show, frequency, categories):
    d, accounts = find_accounts_to_filter_by(categories)
    if d is None:
        return pivot(df, accounts, show, frequency, 'Kontobeskrivelse')

    df_pivot = {}
    for key in d.keys():
        if not all(isinstance(d[key], int) for key in d.keys()):
            accounts = flatten(d[key]).values()
        data_group = groupby(df, accounts, show, frequency)
        df_pivot[key] = data_group
    return transpose_sort_delete(data=df_pivot)


def weighted_average_pmt_terms(df, frequency, categories, data_group_by_cat):
    d, accounts = find_accounts_to_filter_by(categories)
    if d is None or isinstance(d, int):
        return supplier_pmt_terms(df, accounts)

    dict_wa_pmt_terms = {}
    for key in d.keys():
        if not all(isinstance(d[key], int) for key in d.keys()):
            accounts = flatten(d[key]).values()
        data_wa_pmt_terms = wa_pmt_terms(df, accounts, frequency)
        dict_wa_pmt_terms[key] = data_wa_pmt_terms

    return transpose_sort_delete(
        data=dict_wa_pmt_terms,
        accounts=data_group_by_cat.columns
    )