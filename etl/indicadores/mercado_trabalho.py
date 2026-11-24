"""
Extração dos indicadores 15-28, referentes ao mercado de trabalho

Autor: Gabriel
Data de criação: 19/11/2026
"""

import operator

import etl.fontes.ipea as ipea
import etl.fontes.sidra as sidra
import etl.utils as utils

def indicadores_015a020():
    """
    IND-015: Pessoal ocupado total
    Composição: Tabela 9509 do SIDRA
        - variáveis:
            707: Pessoal ocupado total (Pessoas)
        - classificacoes: Não

    IND-016: Pessoal ocupado assalariado
    Composição: Tabela 9509 do SIDRA (avaliar migrar para a RAIS no futuro)
        - variáveis:
            708: Pessoal ocupado assalariado (Pessoas)
        - classificacoes: Não

    IND-017: Empresas e outras organizações atuantes
    Composição: Tabela 9509 do SIDRA
        - variáveis:
            367: Número de empresas e outras organizações atuantes (Unidades)
        - classificacoes: Não

    IND-018: Unidades locais
    Composição: Tabela 9509 do SIDRA
        - variáveis:
            706: Número de unidades locais (Unidades)
        - classificacoes: Não

    IND-019: Salários e outras remunerações
    Composição: Tabela 9509 do SIDRA
        - variáveis:
            662: Salários e outras remunerações (Mil Reais)
        - classificacoes: Não

    IND-020: Salário médio mensal
    Composição: Tabela 9509 do SIDRA
        - variáveis:
            10143: Salário médio mensal em reais (Reais)
        - classificacoes: Não
    """
    return sidra.pipeline_sidra(
        tabela='9509',
        variaveis_indicadores={
            '707'  : 'IND-015',
            '708'  : 'IND-016',
            '367'  : 'IND-017',
            '706'  : 'IND-018',
            '662'  : 'IND-019',
            '10143': 'IND-020',
        }
    )

def indicadores_021e022():
    """
    IND-021: Rendimento médio do trabalho
    Composição: Tabela 10280 do SIDRA
        - variáveis:
            13536: Valor do rendimento nominal médio mensal de todos os trabalhos das pessoas de 14 anos ou mais de idade, ocupadas na semana de referência, com rendimento de trabalho (Reais)

    IND-022: Rendimento mediano do trabalho
    Composição: Tabela 10280 do SIDRA
        - variáveis:
            13537: Valor do rendimento nominal mediano mensal de todos os trabalhos das pessoas de 14 anos ou mais de idade, ocupadas na semana de referência, com rendimento de trabalho (Reais)

    - classificacoes (ambos):
        2: Sexo
        11913: Posição na ocupação e categoria do emprego no trabalho principal
    """
    return sidra.pipeline_sidra(
        tabela='10280',
        variaveis_indicadores={
            '13536': 'IND-021',
            '13537': 'IND-022',
        },
        classificacoes=('2', '11913'),
    )

def indicador_023():
    """
    IND-023: Ocupação/emprego por atividade econômica
    Composição: Tabela 9528 do SIDRA
        - variáveis:
            708: Pessoal ocupado assalariado (Pessoas)
        - classificacoes:
            12762: Classificação Nacional de Atividades Econômicas (CNAE 2.0)

    Obs: Avaliar usabilidade de RAIS depois
    """
    return sidra.pipeline_sidra(
        tabela='9528',
        variaveis_indicadores={
            '708': 'IND-023'
        },
        classificacoes=('12762',),
    )

def indicadores_024a026():
    """
    IND-024: Admissões
    Composição: série ADMISNC do IPEA (avaliar RAIS/caged)

    IND-025: Desligamentos
    Composição: série DESLIGNC do IPEA (avaliar RAIS/caged)

    IND-026: Saldo de empregos
    Composição: cálculo próprio (ADMISNC - DESLIGNC)
    """
    # ind024
    admissoes = ipea.transform(
        ipea.baixar_serie(cod_serie='ADMISNC', nome_coluna_valor='admissoes'),
        indicador="IND-024"
    )

    # ind025
    desligamentos = ipea.transform(
        ipea.baixar_serie(cod_serie='DESLIGNC', nome_coluna_valor='desligamentos'),
        indicador="IND-025"
    )

    movimentacao_trabalhista = ipea.concatenar_dfs(admissoes, desligamentos)

    # ind026
    movimentacao_trabalhista = utils.adicionar_calculo(
        df=movimentacao_trabalhista,
        var_a='admissoes',
        var_b='desligamentos',
        nome_variavel='saldo_empregos',
        indicador='IND-026',
        op=operator.sub,
        uni_medida='Vínculos',
        casas=0,
    )

    return movimentacao_trabalhista

def indicador_027():
    """
    IND-027: Taxa de formalização
    Composição: Tabela 10266 do SIDRA (avaliar a usabilidade da RAIS para este indicador)
        - variáveis:
            4090: Pessoas de 14 anos ou mais de idade ocupadas na semana de referência (Pessoas)
        - classificacoes:
            2: Sexo
            86: Cor ou raça
            526: Condição de contribuição para instituto de previdência oficial no trabalho principal
            11805: Seção de atividade do trabalho principal
    """
    return sidra.pipeline_sidra(
        tabela='10266',
        variaveis_indicadores={
            '4090': 'IND-027'
        },
        classificacoes=('2', '86', '526', '11805'),
    )

def indicador_028():
    """
    IND-028: Escolaridade/qualificação da força de trabalho
    Composição: Tabela 10263 do SIDRA
        - variáveis:
            4090: Pessoas de 14 anos ou mais de idade ocupadas na semana de referência (Pessoas)
        - classificacoes:
            2: Sexo
            86: Cor ou raça
            1568: Nível de instrução
            12031: Número de trabalhos
    """
    return sidra.pipeline_sidra(
        tabela='10263',
        variaveis_indicadores={
            '4090': 'IND-028'
        },
        classificacoes=('2', '86', '1568', '12031'),
    )
