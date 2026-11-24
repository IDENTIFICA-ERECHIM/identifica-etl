"""
Extração dos indicadores 49-70, referentes aos indicadores econômicos e cadeias produtivas

Autor: Gabriel
Data de criação: 19/11/2026
"""

import operator

import etl.fontes.ipea as ipea
import etl.fontes.sidra as sidra
import etl.utils as utils


def indicadores_049_051a054():
    """
    A Tabela 5938 do SIDRA é usada para todos

    IND-049: PIB municipal
        - variáveis:
            37: Produto Interno Bruto a preços correntes (Mil Reais)

    IND-051: VAB agropecuária
        - variáveis:
            513: Valor adicionado bruto a preços correntes da agropecuária (Mil Reais)

    IND-052: VAB indústria
        - variáveis:
            517: Valor adicionado bruto a preços correntes da indústria (Mil Reais)

    IND-053: VAB serviços
        - variáveis:
            6575: Valor adicionado bruto a preços correntes dos serviços, exclusive administração, defesa, educação e saúde públicas e seguridade social (Mil Reais)
            525: Valor adicionado bruto a preços correntes da administração, defesa, educação e saúde públicas e seguridade social (Mil Reais)
        - VAB serviços total = 6575 + 525, no mesmo ano

    IND-054: Participação setorial no VAB
        - variáveis:
            516: Participação da agropecuária no VAB total (%)
            520: Participação da indústria no VAB total (%)
            6574: Participação dos serviços, exclusive administração pública, no VAB total (%)
            528: Participação da administração pública no VAB total (%)
        - Participação dos serviços totais = 6574 + 528 (calcular quando necessário, não é armazenado)

    """
    return sidra.pipeline_sidra(
        tabela='5938',
        variaveis_indicadores={
            '37'  : 'IND-049',
            '513' : 'IND-051',
            '517' : 'IND-052',
            '6575': 'IND-053',
            '525' : 'IND-053',
            '516' : 'IND-054',
            '520' : 'IND-054',
            '6574': 'IND-054',
            '528' : 'IND-054',
        }
    )


def indicador_050():
    """
    IND-050: PIB per capita
    Composição: cálculo próprio
        - PIB: variável 37 da tabela 5938 do SIDRA (extraída em indicadores_049_051a054)
        - População: série ESTIMA_PO do IPEA
        - PIB per capita = (PIB x 1000) / população. Multiplica por 1000 porque o PIB está em Mil Reais
        - Só são calculados os anos presentes nas duas fontes
    """
    pib = indicadores_049_051a054().query("cod_variavel == '37'").assign(
        ano=lambda d: d['ano'].astype(int),
        nome_variavel='pib_total',
    )

    populacao = ipea.transform(
        ipea.baixar_serie(cod_serie='ESTIMA_PO', nome_coluna_valor='populacao'),
        indicador="IND-001"
    )

    pib_per_capita = ipea.concatenar_dfs(pib, populacao)

    pib_per_capita = utils.adicionar_calculo(
        df=pib_per_capita,
        var_a='pib_total',
        var_b='populacao',
        nome_variavel='pib_per_capita',
        indicador='IND-050',
        op=operator.truediv,
        uni_medida='Reais/habitante',
        fator=1000,
    )

    return pib_per_capita.query("nome_variavel == 'pib_per_capita'")

def indicadores_055e056():
    """
    A tabela 9528 do SIDRA é usada para todos

    IND-055: Empresas/unidades locais por CNAE
        - variáveis:
            706: Número de unidades locais (Unidades)

    IND-056: Pessoal ocupado por setor/CNAE
        - variáveis:
            707: Pessoal ocupado total (Pessoas)

    - classificacoes (ambos):
        12762: Classificação Nacional de Atividades Econômicas (CNAE 2.0)
    """
    return sidra.pipeline_sidra(
        tabela='9528',
        variaveis_indicadores={
            '706': 'IND-055',
            '707': 'IND-056',
        },
        classificacoes=('12762',),
    )

def indicadores_057a060():
    """
    A tabela 1612 do SIDRA é usada para todos

    IND-057: Área plantada e colhida
        - variáveis:
            109: Área plantada (Hectares)
            216: Área colhida (Hectares)

    IND-058: Quantidade produzida
        - variáveis:
            214: Quantidade produzida (unidade varia por categoria)

    IND-059: Rendimento médio da produção
        - variáveis:
            112: Rendimento médio da produção (Quilogramas por Hectare)

    IND-060: Valor da produção agrícola
        - variáveis:
            215: Valor da produção (Mil Reais; anos antigos em moedas anteriores)

    - classificacoes (todos):
        81: Produto das lavouras temporárias
    """
    return sidra.pipeline_sidra(
        tabela='1612',
        variaveis_indicadores={
            '109': 'IND-057',
            '216': 'IND-057',
            '214': 'IND-058',
            '112': 'IND-059',
            '215': 'IND-060',
        },
        classificacoes=('81',),
    )

def indicador_061():
    """
    IND-061: Efetivo dos rebanhos
    Composição:
        série QUANTBOVINOS do IPEA (bovinos)
        série QUANTSUINOS do IPEA (suínos)
        série QUANTOVINOS do IPEA (ovinos)
        série QUANTCAPRINOS do IPEA (caprinos)
        série QUANTEQUINOS do IPEA (equinos)
    """
    series = [
        ('QUANTBOVINOS',  'quant_bovinos'),
        ('QUANTSUINOS',   'quant_suinos'),
        ('QUANTOVINOS',   'quant_ovinos'),
        ('QUANTCAPRINOS', 'quant_caprinos'),
        ('QUANTEQUINOS',  'quant_equinos'),
    ]

    partes = [
        ipea.transform(ipea.baixar_serie(cod_serie=cod, nome_coluna_valor=nome), indicador='IND-061')
        for cod, nome in series
    ]

    return ipea.concatenar_dfs(*partes)

def indicador_062():
    """
    IND-062: Produção e valor do leite
    Composição:
        série QUANTLEITE do IPEA (Produção - leite - quantidade, em Litros)
        série VALORLEITE do IPEA (Produção - leite, em R$ a preços do ano 2010)
    """
    qleite = ipea.transform(
        ipea.baixar_serie(cod_serie='QUANTLEITE', nome_coluna_valor='quant_leite'),
        indicador='IND-062'
    )

    vleite = ipea.transform(
        ipea.baixar_serie(cod_serie='VALORLEITE', nome_coluna_valor='valor_leite'),
        indicador='IND-062'
    )

    return ipea.concatenar_dfs(qleite, vleite)

def indicador_063_1():
    """
    IND-063: Produção e valor da silvicultura/extrativismo
    Nesta função, vamos extrair dados da silvicultura

    Composição: Tabela 291 do SIDRA
        - variáveis:
            143: Valor da produção na silvicultura (Mil Reais; anos antigos em moedas anteriores)
        - classificacoes:
            194: Tipo de produto da silvicultura
    """
    return sidra.pipeline_sidra(
        tabela='291',
        variaveis_indicadores={
            '143': 'IND-063'
        },
        classificacoes=('194',),
    )

def indicador_063_2():
    """
    IND-063: Produção e valor da silvicultura/extrativismo
    Nesta função, vamos extrair dados do extrativismo

    Composição: Tabela 289 do SIDRA
        - variáveis:
            145: Valor da produção na extração vegetal (Mil Reais; anos antigos em moedas anteriores)
        - classificacoes:
            193: Tipo de produto extrativo

    Obs: Com os dados atuais, usar apenas o valor da produção. As quantidades devem ser
    acrescentadas se passarem a ter dados utilizáveis.
    """
    return sidra.pipeline_sidra(
        tabela='289',
        variaveis_indicadores={
            '145': 'IND-063'
        },
        classificacoes=('193',),
    )

def indicadores_064a066():
    """
    IND-064: Exportações
    Composição: série EXPORTACAO do IPEA (Exportações (FOB), em US$ FOB)

    IND-065: Importações
    Composição: série IMPORTACAO do IPEA (Importações (FOB), em US$ FOB)

    IND-066: Saldo comercial
    Composição: cálculo próprio (EXPORTACAO - IMPORTACAO, no mesmo ano)

    Obs: US$ FOB é o preço de uma mercadoria em dólares americanos no ponto de embarque (sem incluir frete/seguro)
    """
    # ind064
    exportacoes = ipea.transform(
        ipea.baixar_serie(cod_serie='EXPORTACAO', nome_coluna_valor='exportacoes'),
        indicador='IND-064'
    )

    # ind065
    importacoes = ipea.transform(
        ipea.baixar_serie(cod_serie='IMPORTACAO', nome_coluna_valor='importacoes'),
        indicador='IND-065'
    )

    exportacoes_importacoes = ipea.concatenar_dfs(exportacoes, importacoes)

    # ind066
    exportacoes_importacoes = utils.adicionar_calculo(
        df=exportacoes_importacoes,
        var_a='exportacoes',
        var_b='importacoes',
        nome_variavel='saldo_comercial',
        indicador='IND-066',
        op=operator.sub,
        uni_medida='US$ FOB',
        casas=0,
    )

    return exportacoes_importacoes

def indicadores_067e068():
    """
    IND-067: Estoque de crédito rural
    Composição: série CREAT do IPEA (Estoque de crédito rural, em R$ a preços do ano 2010)

    IND-068: Contratos de crédito rural
    Composição: série NCREAT do IPEA (Total de contratos de crédito rural, em Unidades)
    """
    estoque_cred_rural = ipea.transform(
        ipea.baixar_serie(cod_serie='CREAT', nome_coluna_valor='estoque_cred_rural'),
        indicador='IND-067'
    )

    contratos_cred_rural = ipea.transform(
        ipea.baixar_serie(cod_serie='NCREAT', nome_coluna_valor='contratos_cred_rural'),
        indicador='IND-068'
    )

    return ipea.concatenar_dfs(estoque_cred_rural, contratos_cred_rural)

def indicador_069():
    """
    IND-069: Estrutura de hospedagem
    Composição: Tabela 6589 do SIDRA
        - variáveis:
            1321: Número de estabelecimentos de hospedagem (Unidades)
            1322: Número de unidades habitacionais (Unidades)
            9296: Número de leitos (Unidades)
        - classificacoes:
            493: Tipos de estabelecimentos de hospedagem

    Obs: Dados são meio antigos (2016)
    """
    return sidra.pipeline_sidra(
        tabela='6589',
        variaveis_indicadores={
            '1321': 'IND-069',
            '1322': 'IND-069',
            '9296': 'IND-069',
        },
        classificacoes=('493',),
    )

def indicador_070():
    """
    IND-070: Investimento público municipal
    Composição: série DINVESTM do IPEA (Despesa de capital - investimento - municipal, em R$)
    """
    return ipea.transform(
        ipea.baixar_serie(cod_serie='DINVESTM', nome_coluna_valor='invest_publico_municipal'),
        indicador='IND-070'
    )
