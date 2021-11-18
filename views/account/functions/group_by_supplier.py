from .pivot_func import pivot
from .groupby_func import groupby
from .transpose_sort_delete_func import transpose_sort_delete
from flatten_dict import flatten
from ..components_modules import acct_dict

def group_by_supplier(df, show, frequency, cat_1, cat_2, cat_3, cat_4):
    if not any([cat_4 == '', cat_4 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]

    elif not any([cat_3 == '', cat_3 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3]
        if not isinstance(accounts, int):
            accounts = flatten(accounts).values()

    elif not any([cat_2 == '', cat_2 == 'Alle']):
        d = acct_dict[cat_1][cat_2]
        accounts = flatten(d).values()

    elif cat_2 == 'Alle':
        d = acct_dict[cat_1]
        accounts = flatten(d).values()

    elif cat_1 == 'Alle':
        accounts = flatten(acct_dict).values()

    return pivot(df, accounts, show, frequency, 'Partnerbeskrivelse')

# def group_by_supplier(df, show, frequency, cat_1, cat_2, cat_3, cat_4):
#     if not any([cat_4 == '', cat_4 == 'Alle']):
#         accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]
#         df_group_by_sup = pivot(
#             df, accounts, show, frequency, 'Partnerbeskrivelse')

#     elif not any([cat_3 == '', cat_3 == 'Alle']):
#         accounts = acct_dict[cat_1][cat_2][cat_3]
#         if not isinstance(accounts, int):
#             account_list = flatten(accounts).values()
#             df_group_by_sup = pivot(
#                 df, account_list, show, frequency, 'Partnerbeskrivelse')
#         else:
#             df_group_by_sup = pivot(
#                 df, accounts, show, frequency, 'Partnerbeskrivelse')

#     elif not any([cat_2 == '', cat_2 == 'Alle']):
#         d = acct_dict[cat_1][cat_2]
#         accounts = flatten(d).values()
#         df_group_by_sup = pivot(
#             df, accounts, show, frequency, 'Partnerbeskrivelse')

#     elif cat_2 == 'Alle':
#         d = acct_dict[cat_1]
#         accounts = flatten(d).values()
#         df_group_by_sup = pivot(
#             df, accounts, show, frequency, 'Partnerbeskrivelse')

#     elif cat_1 == 'Alle':
#         accounts = flatten(acct_dict).values()
#         df_group_by_sup = pivot(
#             df, accounts, show, frequency, 'Partnerbeskrivelse')

#     return pivot(df, accounts, show, frequency, 'Partnerbeskrivelse')

