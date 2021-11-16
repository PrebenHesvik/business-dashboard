import pathlib
import pandas as pd
import numpy as np

# import datasets
path_to_datasets = pathlib.Path.cwd().joinpath("datasets")
path_transactions = path_to_datasets.joinpath("transactions.parquet")
path_pmt_terms = path_to_datasets.joinpath("payment-terms.npy")

transactions = pd.read_parquet(path_transactions, engine='pyarrow')
payment_terms = np.load(path_pmt_terms, allow_pickle='TRUE').item()

options = {
    "year": sorted((transactions['Bilagsdato'].dt.year.unique().tolist())),
    "frequency": {"Årlig": "Y", "Kvartalsvis": "Q", "Månedlig": "M"},
    "factory": ["Fabrikk A", "Fabrikk B", "Fabrikk C"],
}
