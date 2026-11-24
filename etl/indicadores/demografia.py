"""
Extração dos indicadores 0-14, referentes à demografia

Autor: Gabriel
Data de criação: 18/11/2026
"""

import operator

import pandas as pd

import etl.fontes.ipea as ipea
import etl.fontes.sidra as sidra
import etl.utils as utils

def indicadores_001e002():
    """
    IND-001: População residente total
    Composição: série ESTIMA_PO do IPEA

    IND-002: Taxa de crescimento populacional
    Composição: cálculo próprio.
    """
    #ind001
    ipea_populacao = ipea.baixar_serie(
        cod_serie='ESTIMA_PO', nome_coluna_valor='populacao'
    )

    ipea_populacao = ipea.transform(
        ipea_populacao, indicador="IND-001"
    )

    #ind002
    ipea_populacao = utils.adicionar_taxa_crescimento(
        df=ipea_populacao, variavel_base='populacao', indicador="IND-002"
    )

    return ipea_populacao

def indicadores_003e004():
    """
    IND-003: População urbana e rural
    Composição:
        série POPUR do IPEA (população urbana)
        série POPRU do IPEA (população rural)
        série POPTOT do IPEA (população total)

    IND-004: Taxa de urbanização
    Composição: cálculo próprio
    """

    # ind003
    pop_urbana = ipea.transform(
        ipea.baixar_serie(cod_serie="POPUR", nome_coluna_valor='populacao_urbana'),
        indicador="IND-003"
    )

    pop_rural = ipea.transform(
        ipea.baixar_serie(cod_serie="POPRU", nome_coluna_valor='populacao_rural'),
        indicador="IND-003"
    )

    pop_total = ipea.transform(
        ipea.baixar_serie(cod_serie="POPTOT", nome_coluna_valor='populacao_total'),
        indicador="IND-003"
    )

    populacao_urbana_e_rural = ipea.concatenar_dfs(
        pop_urbana, pop_rural, pop_total
    )

    # ind004
    populacao_urbana_e_rural = utils.adicionar_calculo(
        df=populacao_urbana_e_rural,
        var_a='populacao_urbana',
        var_b='populacao_total',
        nome_variavel='taxa_urbanizacao',
        indicador='IND-004',
        op=operator.truediv,
        uni_medida='%',
        fator=100,
    )

    return populacao_urbana_e_rural

def indicador_005_1():
    """
    IND-005: Distribuição da população por grupos etários
    Composição: várias séries do ipea
    Obs: Cobre mais anos, mas possuem menos especificação de idades
    """
    series = [
        ('POP0_4M',   '0-4',   'Homens'),
        ('POP0_4F',   '0-4',   'Mulheres'),
        ('POP5_9M',   '5-9',   'Homens'),
        ('POP5_9F',   '5-9',   'Mulheres'),
        ('POP10_14M', '10-14', 'Homens'),
        ('POP10_14F', '10-14', 'Mulheres'),
        ('POP15_19M', '15-19', 'Homens'),
        ('POP15_19F', '15-19', 'Mulheres'),
        ('POP20_24M', '20-24', 'Homens'),
        ('POP20_24F', '20-24', 'Mulheres'),
        ('POP25_29M', '25-29', 'Homens'),
        ('POP25_29F', '25-29', 'Mulheres'),
        ('POP30_39M', '30-39', 'Homens'),
        ('POP30_39F', '30-39', 'Mulheres'),
        ('POP40_49M', '40-49', 'Homens'),
        ('POP40_49F', '40-49', 'Mulheres'),
        ('POP50_59M', '50-59', 'Homens'),
        ('POP50_59F', '50-59', 'Mulheres'),
        ('POP60_69M', '60-69', 'Homens'),
        ('POP60_69F', '60-69', 'Mulheres'),
        ('POP70M_M',  '70+',   'Homens'),
        ('POP70M_F',  '70+',   'Mulheres'),
    ]

    partes = [
        ipea.transform( ipea.baixar_serie(cod, 'populacao'), 'IND-005')
        .assign(faixa_etaria=faixa, sexo=sexo) for cod, faixa, sexo in series
    ]

    populacao_idade_sexo_faixas = ipea.concatenar_dfs(*partes)

    total = (
        populacao_idade_sexo_faixas
        .groupby(['ano', 'indicador', 'nome_variavel', 'faixa_etaria', 'uni_medida'], as_index=False, dropna=False)['valor']
        .sum(min_count=2)
        .assign(sexo='Total', cod_serie=None)
    )

    populacao_idade_sexo_faixas = ipea.concatenar_dfs(populacao_idade_sexo_faixas, total)

    return populacao_idade_sexo_faixas


def indicador_005_2():
    """
    IND-005: Distribuição da população por grupos etários
    Composição: Tabela 9514 do SIDRA
        - variáveis:
            93: População residente (Pessoas)
            1000093: População residente - percentual do total geral
        - classificacoes:
            2: sexo
            287: idade

    Obs: Cobre somente um ano, mas possui mais especificação de idades
    """
    return sidra.pipeline_sidra(
        tabela='9514',
        variaveis_indicadores={
            '93'     : 'IND-005',
            '1000093': 'IND-005',
        },
        classificacoes=('2', '287')
    )

def indicador_006():
    """
    IND-006: Índice de envelhecimento
    Composição: Tabela 10097 do SIDRA (Índice de envelhecimento [...] por localização e situação do domicílio)
        - variáveis:
            9175: Índice de envelhecimento (Idosos: 60 anos ou mais de idade) (Razão)
        - classificacoes:
            2661: Localização do domicílio
            1: Situação do domicílio
    """

    return sidra.pipeline_sidra(
        tabela='10097',
        variaveis_indicadores={
            '9175': 'IND-006'
        },
        classificacoes=('2661', '1')
    )

def indicador_007():
    """
    IND-007: Idade mediana
    Composição: Tabela 9515 do SIDRA
        - variáveis:
            10613: Idade mediana (Anos)
        - classificacoes: Não
    """
    return sidra.pipeline_sidra(
        tabela='9515',
        variaveis_indicadores={
            '10613': 'IND-007'
        }
    )


def indicador_008():
    """
    IND-008: Razão de dependência
    Composição: Cálculo pŕoprio, com os dados do indicador 005_1
    """
    total = indicador_005_1().query("sexo == 'Total'")

    criancas = ['0-4', '5-9', '10-14']
    ativa  = ['15-19', '20-24', '25-29', '30-39', '40-49', '50-59']
    idosos = ['60-69', '70+']

    pop_criancas = total[total['faixa_etaria'].isin(criancas)].groupby('ano')['valor'].sum(min_count=3)
    pop_ativa = total[total['faixa_etaria'].isin(ativa)].groupby('ano')['valor'].sum(min_count=6)
    pop_idosa = total[total['faixa_etaria'].isin(idosos)].groupby('ano')['valor'].sum(min_count=2)

    razao_dependencia = pd.DataFrame({
        'pop_criancas_0-14': pop_criancas,
        'pop_ativa_15-59': pop_ativa,
        'pop_idosa_60mais': pop_idosa,
    }).reset_index()

    razao_dependencia['razao_dependencia'] = round(
        (razao_dependencia['pop_criancas_0-14'] + razao_dependencia['pop_idosa_60mais']) / razao_dependencia['pop_ativa_15-59'] * 100,
        2
    )

    unidades = {
        'pop_criancas_0-14': 'Habitante',
        'pop_ativa_15-59':   'Habitante',
        'pop_idosa_60mais':  'Habitante',
        'razao_dependencia': '%',
    }

    # converter para formato longo
    razao_dependencia = (
        razao_dependencia
        .melt(id_vars='ano', var_name='nome_variavel', value_name='valor')
        .assign(
            indicador='IND-008',
            cod_serie=None,
            uni_medida=lambda d: d['nome_variavel'].map(unidades),
        )
        .dropna(subset=['valor'])
        [['ano', 'indicador', 'nome_variavel', 'cod_serie', 'valor', 'uni_medida']]
    )

    return razao_dependencia


def indicador_009():
    """
    IND-009: População por sexo / razão de sexo
    Composição:
        - População por sexo: séries POPF e POPM do IPEA
        - Razão de sexo: calculada dividindo homens por mulheres e multiplicando por 100 (mostra quantos homens existem para cada 100 mulheres.)
    """
    popm = ipea.transform(
        ipea.baixar_serie(cod_serie="POPM", nome_coluna_valor='pop_masculina'), indicador="IND-009"
    )

    popf = ipea.transform(
        ipea.baixar_serie(cod_serie="POPF", nome_coluna_valor='pop_feminina'), indicador="IND-009"
    )

    populacao_sexo = ipea.concatenar_dfs(popm, popf)

    populacao_sexo = utils.adicionar_calculo(
        df=populacao_sexo,
        var_a='pop_masculina',
        var_b='pop_feminina',
        nome_variavel='razao_sexo',
        indicador='IND-009',
        op=operator.truediv,
        uni_medida='Homens p/ 100 mulheres',
        fator=100,
    )

    return populacao_sexo

def indicador_010():
    """
    IND-010: Densidade demográfica
    Composição:
        - Densidade demografica: calculada dividindo a populacao total pela area
    """
    pop_total = indicadores_003e004().query("nome_variavel == 'populacao_total'")

    area = ipea.transform(
        ipea.baixar_serie("AREA", nome_coluna_valor='area_geo'), indicador="IND-010"
    )

    densidade_demografica = ipea.concatenar_dfs(pop_total, area)

    densidade_demografica = utils.adicionar_calculo(
        df=densidade_demografica,
        var_a='populacao_total',
        var_b='area_geo',
        nome_variavel='densidade_demografica',
        indicador='IND-010',
        op=operator.truediv,
        uni_medida='Habitante/km²',
    )

    return densidade_demografica.query("indicador == 'IND-010'")


def indicador_011_1():
    """
    IND-011: Perfil migratório, naturalidade e nacionalidade do município
    Composição: Tabela 10160 do SIDRA
        - variáveis:
            13435: Pessoas de 5 anos ou mais de idade que não residiam no município 5 anos antes da data de referência
        - classificacoes:
            2: Sexo
            58: Grupo de idade
    """
    return sidra.pipeline_sidra(
        tabela='10160',
        variaveis_indicadores={
            '13435': 'IND-011'
        },
        classificacoes=('2', '58'),
    )

def indicador_011_2():
    """
    IND-011: Perfil migratório, naturalidade e nacionalidade da UF
    Composição: Tabela 10159 do SIDRA
        - variáveis:
            13339: Pessoas de 5 anos ou mais de idade que não residiam na Unidade da Federação 5 anos antes da data de referência
        - classificacoes:
            2083: Lugar de residência 5 anos antes da data de referência: Sexo
    """
    return sidra.pipeline_sidra(
        tabela= '10159',
        variaveis_indicadores={
            '13339': 'IND-011'
        },
        classificacoes=('2083',),
    )

def indicador_011_3():
    """
    IND-011: Perfil migratório, naturalidade e nacionalidade internacional
    Composição: Tabela 10161 do SIDRA
        - variáveis:
            13340: Pessoas de 5 anos ou mais de idade que não residiam no Brasil 5 anos antes da data de referência
        - classificacoes:
            2: Sexo
            2084: País de residência 5 anos antes da data de referência
    """
    return sidra.pipeline_sidra(
        tabela='10161',
        variaveis_indicadores={
            '13340': 'IND-011'
        },
        classificacoes=('2', '2084'),
    )

def indicador_012():
    """
    IND-012: Nascidos vivos
    Composição: Tabela 2680 do SIDRA
        - variáveis:
            218: Nascidos vivos ocorridos no ano
        - classificacoes:
            240: idade da mãe

    FUTURAMENTE USAR DATASUS (SINASC) para este indicador
    """
    return sidra.pipeline_sidra(
        tabela='2680',
        variaveis_indicadores={
            '218': 'IND-012'
        },
        classificacoes=('240',),
    )

def indicador_013():
    pass

def indicador_014():
    pass
