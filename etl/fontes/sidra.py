"""
Funções de extração e transformação para as tabelas do SIDRA (IBGE)

Autor: Gabriel
Data de criação: 18/11/2026
"""

import pandas as pd
import sidrapy

from functools import cache

NIVEL_TERRITORIAL_MUNICIPIO = '6'
CODIGO_ERECHIM_IBGE = '4307005'


@cache
def extrair_tabela(tabela: str, variaveis: tuple[str, ...], classificacoes: tuple[str, ...] = ()) -> pd.DataFrame:
    parametros = dict(variable=','.join(variaveis))

    if classificacoes:
        parametros['classifications'] = {c: 'all' for c in classificacoes}

    try:
        df_bruto = sidrapy.get_table(
            table_code=tabela,
            territorial_level=NIVEL_TERRITORIAL_MUNICIPIO,
            ibge_territorial_code=CODIGO_ERECHIM_IBGE,
            period='all',
            **parametros
        )
    except Exception as e:
        raise RuntimeError(f'Erro ao extrair tabela: {tabela}') from e

    print(f"Tabela SIDRA (IBGE) Extraida: {tabela}")

    return df_bruto


def transform(tabela: str, df: pd.DataFrame, indicadores: dict[str, str], classificacoes: tuple[str, ...] = ()):
    n_classificacoes = len(classificacoes)

    colunas: dict[str, str] = {
        'D2N': 'ano',
        'V':   'valor',
        'MN':  'uni_medida',
        'D3N': 'nome_variavel',
        'D3C': 'cod_variavel'
    }

    for i in range(1, n_classificacoes + 1):
        colunas[f'D{i + 3}C'] = f'cod_categoria_{i}'
        colunas[f'D{i + 3}N'] = f'categoria_{i}'

    df = (df
        .iloc[1:]
        [list(colunas)]
        .rename(columns=colunas)
    )

    print(f"Tabela do SIDRA transformada: {tabela}")

    return df.assign(
        ano=df['ano'].astype(int),
        valor=pd.to_numeric(df['valor'].replace({'-': '0'}), errors='coerce'),
        indicador=df['cod_variavel'].map(indicadores)
    )

def pipeline_sidra(tabela: str,
                    variaveis_indicadores: dict[str, str],
                    classificacoes: tuple[str, str] = ()) -> pd.DataFrame:
    df_bruto = extrair_tabela(
        tabela=tabela,
        variaveis=tuple(variaveis_indicadores),
        classificacoes=classificacoes
    )

    df_transf = transform(
        tabela=tabela,
        df=df_bruto,
        indicadores=variaveis_indicadores,
        classificacoes=classificacoes
    )

    return df_transf
