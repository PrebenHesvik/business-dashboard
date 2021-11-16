import pandas as pd


def transpose_sort_delete(data, accounts=None):
    data = pd.DataFrame(data).fillna(0).transpose()
    if accounts is None:
        data['sum'] = data.sum(axis=1)
        data = data.sort_values(by='sum', ascending=False)[:8]
        data = data.drop(columns=['sum'])
        data = data.transpose()
    else:
        data = data.transpose()
        valid_cols = [acct for acct in accounts if acct in data.columns]
        data = data[valid_cols]

    data.index = [str(x.to_pydatetime().date()) for x in data.index]

    return data
