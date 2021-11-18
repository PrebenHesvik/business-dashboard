from .pivot_func import pivot
from flatten_dict import flatten
from ..components_modules import acct_dict


def group_by_location(df, show, frequency, cat_1, cat_2, cat_3, cat_4):

    if not any([cat_4 == '', cat_4 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]

    elif not any([cat_3 == '', cat_3 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3]
        if not isinstance(accounts, int):
            accounts = flatten(accounts).values()

    elif not any([cat_2 == '', cat_2 == 'Alle']):
        # User has selected an option in selection boxes 1 + 2
        accounts = flatten(acct_dict[cat_1][cat_2]).values()

    elif cat_2 == 'Alle':
        # User has selected an option in selection box 1
        accounts = flatten(acct_dict[cat_1]).values()

    elif cat_1 == 'Alle':
        # Page has just been loaded and the user has not
        # selected an option in selection box 1
        accounts = flatten(acct_dict).values()

    return pivot(df, accounts, show, frequency, 'Lokasjon')


# def group_by_location(df, show, frequency, cat_1, cat_2, cat_3, cat_4):

#     string = '-'.join([cat_1, cat_2, cat_3, cat_4])
#     print(string)

#     if not any([cat_4 == '', cat_4 == 'Alle']):
#         accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]
#         df_pivot = pivot(df, accounts, show, frequency, 'Lokasjon')

#     elif not any([cat_3 == '', cat_3 == 'Alle']):
#         accounts = acct_dict[cat_1][cat_2][cat_3]
#         if not isinstance(accounts, int):
#             account_list = flatten(accounts).values()
#             df_pivot = pivot(df, account_list, show, frequency, 'Lokasjon')
#         else:
#             df_pivot = pivot(df, accounts, show, frequency, 'Lokasjon')

#     elif not any([cat_2 == '', cat_2 == 'Alle']):
#         # User has selected an option in selection boxes 1 + 2
#         d = acct_dict[cat_1][cat_2]
#         accounts = flatten(d).values()
#         df_pivot = pivot(df, accounts, show, frequency, 'Lokasjon')

#     elif cat_2 == 'Alle':
#         # User has selected an option in selection box 1
#         d = acct_dict[cat_1]
#         accounts = flatten(d).values()
#         df_pivot = pivot(df, accounts, show, frequency, 'Lokasjon')

#     elif cat_1 == 'Alle':
#         # Page has just been loaded and the user has not
#         # selected an option in selection box 1
#         accounts = flatten(acct_dict).values()
#         df_pivot = pivot(df, accounts, show, frequency, 'Lokasjon')

#     return df_pivot
