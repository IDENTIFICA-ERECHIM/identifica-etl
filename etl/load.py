from os import replace

import pandas as pd

import db.db as db

def load_df(df: pd.DataFrame, nome_tabela: str):
    df.to_sql(
        name=nome_tabela,
        con=db.get_engine(),
        if_exists='replace',
        index=False
    )
