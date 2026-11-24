import operator
import pandas as pd


def print_df_inteiro(df: pd.DataFrame):
    print(df.to_string())


def adicionar_taxa_crescimento(df, variavel_base, indicador):
    base = df[df['nome_variavel'] == variavel_base]
    anterior = (base['ano'] - 1).map(base.set_index('ano')['valor'])

    taxa = base.assign(
        nome_variavel=f'taxa_crescimento_{variavel_base}',
        indicador=indicador,
        valor=round((base['valor'] / anterior - 1) * 100, 2),
        uni_medida='%',
        cod_serie=None,
    ).dropna(subset=['valor'])

    return pd.concat([df, taxa], ignore_index=True)


def adicionar_participacao(df, cod_total, nome_variavel, indicador, categoria='cod_categoria_1', casas=2):
    total = df[df[categoria] == cod_total].set_index('ano')['valor']

    nova = df.assign(
        valor=(df['valor'] / df['ano'].map(total) * 100).round(casas),
        nome_variavel=nome_variavel,
        indicador=indicador,
        cod_variavel=None,
        uni_medida='%',
    ).dropna(subset=['valor'])

    return pd.concat([df, nova], ignore_index=True)


def adicionar_percentual_categorias(df, cods_num, cod_den, nome_variavel, indicador,
                                    categoria='cod_categoria_1', casas=2):
    num = df[df[categoria].isin(cods_num)].groupby('ano')['valor'].sum(min_count=len(cods_num))
    den = df[df[categoria] == cod_den].set_index('ano')['valor']

    nova = (
        (num / den * 100).round(casas).dropna().rename('valor').reset_index()
        .assign(nome_variavel=nome_variavel, indicador=indicador,
                cod_variavel=None, uni_medida='%')
    )

    return pd.concat([df, nova], ignore_index=True)


def adicionar_calculo(df, var_a, var_b, nome_variavel, indicador, uni_medida,
                    op, fator=1, casas=2, ):
    for v in (var_a, var_b):
        if not (df['nome_variavel'] == v).any():
            raise KeyError(f"nome_variavel '{v}' não encontrada")

    a = df[df['nome_variavel'] == var_a].set_index('ano')['valor']
    b = df[df['nome_variavel'] == var_b].set_index('ano')['valor']

    nova = (
        (op(a, b) * fator).round(casas).dropna().rename('valor').reset_index()
        .assign(nome_variavel=nome_variavel, indicador=indicador,
                cod_serie=None, uni_medida=uni_medida)
    )

    return pd.concat([df, nova], ignore_index=True)
