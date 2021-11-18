from .pivot_func import pivot
from .groupby_func import groupby
from .transpose_sort_delete_func import transpose_sort_delete
from flatten_dict import flatten
from ..components_modules import acct_dict


def group_by_category(df, show, frequency, cat_1, cat_2, cat_3, cat_4):

    if not any([cat_4 == '', cat_4 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]
        return pivot(df, accounts, show, frequency, 'Kontobeskrivelse')

    elif not any([cat_3 == '', cat_3 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3]
        if isinstance(accounts, int):
            return pivot(df, accounts, show, frequency, 'Kontobeskrivelse')
        account_list = flatten(accounts).values()
        return pivot(df, account_list, show, frequency, 'Kontobeskrivelse')

    elif not any([cat_2 == '', cat_2 == 'Alle']):
        d = acct_dict[cat_1][cat_2]
        if all(isinstance(d[key], int) for key in d.keys()):
            return pivot(df, d.values(), show, frequency, 'Kontobeskrivelse')

    elif cat_2 == 'Alle':
        d = acct_dict[cat_1]

    elif cat_1 == 'Alle':
        d = acct_dict

    df_pivot = {}
    for key in d.keys():
        accounts = flatten(d[key]).values()
        data_group = groupby(df, accounts, show, frequency)
        df_pivot[key] = data_group
    return transpose_sort_delete(data=df_pivot)



# def group_by_category(df, show, frequency, cat_1, cat_2, cat_3, cat_4):

#     df_pivot = {}
#     if not any([cat_4 == '', cat_4 == 'Alle']):
#         accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]
#         df_pivot = pivot(df, accounts, show, frequency, 'Kontobeskrivelse')

#     elif not any([cat_3 == '', cat_3 == 'Alle']):
#         accounts = acct_dict[cat_1][cat_2][cat_3]
#         if not isinstance(accounts, int):
#             account_list = flatten(accounts).values()
#             df_pivot = pivot(df, account_list, show, frequency, 'Kontobeskrivelse')
#         else:
#             df_pivot = pivot(df, accounts, show, frequency, 'Kontobeskrivelse')

#     elif not any([cat_2 == '', cat_2 == 'Alle']):
#         d = acct_dict[cat_1][cat_2]
#         if all(isinstance(d[key], int) for key in d.keys()):
#             # data for group_by_cat (returns df)
#             df_pivot = pivot(df, d.values(), show, frequency, 'Kontobeskrivelse')
#         else:
#             for key in d.keys():
#                 accounts = flatten(d[key]).values()
#                 data_group = groupby(df, accounts, show, frequency)
#                 df_pivot[key] = data_group

#     elif cat_2 == 'Alle':
#         d = acct_dict[cat_1]
#         for key in d.keys():
#             accounts = flatten(d[key]).values()
#             data_group = groupby(df, accounts, show, frequency)
#             df_pivot[key] = data_group

#     elif cat_1 == 'Alle':
#         accounts = flatten(acct_dict).values()
#         for key in acct_dict.keys():
#             accounts = flatten(acct_dict[key]).values()
#             data_group = groupby(df, accounts, show, frequency)
#             df_pivot[key] = data_group

#     if isinstance(df_pivot, dict):
#         df_pivot = transpose_sort_delete(data=df_pivot)

#     return df_pivot