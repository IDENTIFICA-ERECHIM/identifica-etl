"""
Funções de extração e transformação para as séries do IPEA

Autor: Gabriel
Data de criação: 18/11/2026
"""


import requests
import pandas as pd

CODIGO_ERECHIM_IPEA = '4307005'

BASE_IPEA = 'https://www.ipeadata.gov.br/api/odata4'

def baixar_serie(cod_serie: str, nome_coluna_valor):
    url = f"{BASE_IPEA}/ValoresSerie(SERCODIGO='{cod_serie}')"

    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar: {cod_serie}") from e

    df = pd.DataFrame(r.json()['value'])

    df = df[
        (df['NIVNOME'] == 'Municípios') & (df['TERCODIGO'].astype(str) == CODIGO_ERECHIM_IPEA)
    ]

    # buscar a unidade de medida nos metadados
    url_meta = f"{BASE_IPEA}/Metadados('{cod_serie}')"

    try:
        r_meta = requests.get(url_meta, timeout=60)
        r_meta.raise_for_status()
    except Exception as e:
        raise RuntimeError(f'Erro ao consultar metadados da serie: {cod_serie}') from e

    metadados = r_meta.json()['value']
    unidade = metadados[0].get('UNINOME') if metadados else None

    print(f"Serie IPEA extraida: {cod_serie}")

    return pd.DataFrame({
        'ano': pd.to_datetime(df['VALDATA'].str[:10]).dt.year.to_numpy(),
        'cod_serie': cod_serie,
        nome_coluna_valor: pd.to_numeric(df['VALVALOR'], errors='coerce').to_numpy(),
        'uni_medida': unidade
    })

def transform(df: pd.DataFrame, indicador: str):
    # converter o dataframe para o formato longo
    colunas_fixas = ['ano', 'cod_serie', 'uni_medida']
    nome_valor = [c for c in df.columns if c not in colunas_fixas][0]

    return (
        df.rename(columns={nome_valor: 'valor'})
        .assign(nome_variavel=nome_valor, indicador=indicador)
        [['ano', 'indicador', 'nome_variavel', 'cod_serie', 'valor', 'uni_medida']]
    )

def concatenar_dfs(*dfs):
    return pd.concat(dfs, ignore_index=True)
