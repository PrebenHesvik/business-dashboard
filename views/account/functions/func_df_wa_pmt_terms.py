from .pivot_func import pivot
from .groupby_func import groupby
from .transpose_sort_delete_func import transpose_sort_delete
from .weighted_avg_pmt_terms_func import wa_pmt_terms
from .supplier_pmt_terms_func import supplier_pmt_terms
from flatten_dict import flatten
from ..components_modules import acct_dict

def weighted_average_pmt_terms(df, frequency, cat_1, cat_2, cat_3, cat_4, data_group_by_cat):

    if not any([cat_4 == '', cat_4 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]
        return supplier_pmt_terms(df, accounts)

    elif not any([cat_3 == '', cat_3 == 'Alle']):
        d = acct_dict[cat_1][cat_2][cat_3]
        if isinstance(d, int):
            return supplier_pmt_terms(df, d)

    elif not any([cat_2 == '', cat_2 == 'Alle']):
        d = acct_dict[cat_1][cat_2]

    elif cat_2 == 'Alle':
        d = acct_dict[cat_1]

    elif cat_1 == 'Alle':
        d = acct_dict

    dict_wa_pmt_terms = {}
    for key in d.keys():
        if all(isinstance(d[key], int) for key in d.keys()):
            for key, account in d.items():
                data_wa_pmt_terms = wa_pmt_terms(df, account, frequency)
                dict_wa_pmt_terms[key] = data_wa_pmt_terms
        else:
            accounts = flatten(d[key]).values()
            data_wa_pmt_terms = wa_pmt_terms(df, accounts, frequency)
            dict_wa_pmt_terms[key] = data_wa_pmt_terms

    return transpose_sort_delete(
            data=dict_wa_pmt_terms,
            accounts=data_group_by_cat.columns)



# def weighted_average_pmt_terms(df, frequency, cat_1, cat_2, cat_3, cat_4, data_group_by_cat):
#     dict_wa_pmt_terms = {}
#     if not any([cat_4 == '', cat_4 == 'Alle']):
#         accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]
#         df_wa_pmt_terms = supplier_pmt_terms(df, accounts)

#     elif not any([cat_3 == '', cat_3 == 'Alle']):
#         accounts = acct_dict[cat_1][cat_2][cat_3]
#         if isinstance(accounts, int):
#             return supplier_pmt_terms(df, accounts)
#         for account_name, account in accounts.items():
#             data_wa_pmt_terms = wa_pmt_terms(df, account, frequency)
#             dict_wa_pmt_terms[account_name] = data_wa_pmt_terms

#     elif not any([cat_2 == '', cat_2 == 'Alle']):
#         d = acct_dict[cat_1][cat_2]
#         if all(isinstance(d[key], int) for key in d.keys()):
#             for key, account in d.items():
#                 data_wa_pmt_terms = wa_pmt_terms(df, account, frequency)
#                 dict_wa_pmt_terms[key] = data_wa_pmt_terms
#         else:
#             for key in d.keys():
#                 accounts = flatten(d[key]).values()
#                 data_wa_pmt_terms = wa_pmt_terms(df, accounts, frequency)
#                 dict_wa_pmt_terms[key] = data_wa_pmt_terms

#     elif cat_2 == 'Alle':
#         d = acct_dict[cat_1]
#         for key in d.keys():
#             accounts = flatten(d[key]).values()
#             data_wa_pmt_terms = wa_pmt_terms(df, accounts, frequency)
#             dict_wa_pmt_terms[key] = data_wa_pmt_terms
#     elif cat_1 == 'Alle':
#         for key in acct_dict.keys():
#             accounts = flatten(acct_dict[key]).values()
#             data_wa_pmt_terms = wa_pmt_terms(df, accounts, frequency)
#             dict_wa_pmt_terms[key] = data_wa_pmt_terms
#     if dict_wa_pmt_terms:
#         df_wa_pmt_terms = transpose_sort_delete(
#             data=dict_wa_pmt_terms,
#             accounts=data_group_by_cat.columns)

#     return df_wa_pmt_terms
