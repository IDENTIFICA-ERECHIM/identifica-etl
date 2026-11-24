"""
Extração dos indicadores 29-48, referentes a dados sociais

Autor: Gabriel
Data de criação: 19/11/2026
"""

import etl.fontes.ipea as ipea
import etl.fontes.sidra as sidra
import etl.utils as utils

def indicador_029():
    """
    IND-029: Taxa de alfabetização 15+
    Composição: Tabela 9543 do SIDRA
        - variáveis:
            2513: Taxa de alfabetização das pessoas de 15 anos ou mais de idade (%)
        - classificacoes:
            2: Sexo
            86: Cor ou raça
            287: Idade
    """
    return sidra.pipeline_sidra(
        tabela='9543',
        variaveis_indicadores={
            '2513': 'IND-029'
        },
        classificacoes=('2', '86', '287'),
    )

def indicador_030():
    """
    IND-030: Taxa de analfabetismo 15+
    Composição: Tabela 10135 do SIDRA
        - variáveis:
            10267: Taxa de analfabetismo das pessoas de 15 anos ou mais de idade (%)
        - classificacoes:
            2: Sexo
            86: Cor ou raça
            58: Grupo de idade
            839: Existência de deficiência
    """
    return sidra.pipeline_sidra(
        tabela='10135',
        variaveis_indicadores={
            '10267': 'IND-030'
        },
        classificacoes=('2', '86', '58', '839'),
    )

def indicador_031():
    """
    IND-031: Taxa de frequência escolar bruta
    Composição: Tabela 10056 do SIDRA
        - variáveis:
            3795: Taxa de frequência escolar bruta (%)
        - classificacoes:
            2: Sexo
            86: Cor ou raça
            58: Grupo de idade
    """
    return sidra.pipeline_sidra(
        tabela='10056',
        variaveis_indicadores={
            '3795': 'IND-031'
        },
        classificacoes=('2', '86', '58'),
    )

def indicador_032():
    """
    IND-032: Nível de instrução da população
    Composição: Tabela 3460 do SIDRA
        - variáveis:
            950: Pessoas de 15 anos ou mais de idade (Pessoas)
        - classificacoes:
            2: Sexo
            86: Cor ou raça
            58: Grupo de idade
            1568: Nível de instrução

    Obs: Cobre somente 2010.
    """
    return sidra.pipeline_sidra(
        tabela='3460',
        variaveis_indicadores={
            '950': 'IND-032'
        },
        classificacoes=('2', '86', '58', '1568'),
    )

def indicador_033():
    """
    IND-033: Matrículas, docentes, escolas e IDEB
    Composição: INEP
    """
    pass

def indicador_034():
    """
    IND-034: Domicílios particulares permanentes ocupados
    Composição: Tabela 4712 do SIDRA
        - variáveis:
            381: Domicílios particulares permanentes ocupados (Domicílios)
        - classificacoes: Não
    """
    return sidra.pipeline_sidra(
        tabela='4712',
        variaveis_indicadores={
            '381': 'IND-034'
        }
    )

def indicador_035():
    """
    IND-035: Média de moradores por domicílio
    Composição: Tabela 9877 do SIDRA
        - variáveis:
            9325: Média de moradores em domicílios particulares (Pessoas)
        - classificacoes:
            11561: Sexo da pessoa responsável pelo domicílio
            12237: Cor ou raça da pessoa responsável pelo domicílio
            11562: Grupos de idade da pessoa responsável pelo domicílio
    """
    return sidra.pipeline_sidra(
        tabela='9877',
        variaveis_indicadores={
            '9325': 'IND-035'
        },
        classificacoes=('11561', '12237', '11562'),
    )

def indicador_036():
    """
    IND-036: Condição de ocupação do domicílio
    Composição: Tabela 9928 do SIDRA
        - variáveis:
            381: Domicílios particulares permanentes ocupados (Domicílios)
        - classificacoes:
            63: Condição de ocupação do domicílio

            Obs: principais classificacoes = ['73554', '1055', '73553', '1058'] # Próprio, Alugado, Cedido, Outra condição

    Participação: cálculo próprio (domicílios da categoria / total de domicílios (codigo 95826) * 100)

    """
    condicao_ocupacao_domicilio = sidra.pipeline_sidra(
        tabela='9928',
        variaveis_indicadores={
            '381': 'IND-036'
        },
        classificacoes=('63',),
    )

    return utils.adicionar_participacao(
        df=condicao_ocupacao_domicilio,
        cod_total='95826',
        nome_variavel='participacao_condicao_ocupacao',
        indicador='IND-036',
    )

def indicador_037():
    """
    IND-037: Abastecimento de água
    Composição: Tabela 6803 do SIDRA
        - variáveis:
            381: Domicílios particulares permanentes ocupados (Domicílios)
        - classificacoes:
            1821: Existência de ligação à rede geral de distribuição de água e principal forma de abastecimento de água

    Percentual de domicílios ligados à rede geral: cálculo próprio
        - ligados à rede geral (72144 + 72145) / total de domicílios (72129) * 100
    """
    abastecimento_agua = sidra.pipeline_sidra(
        tabela='6803',
        variaveis_indicadores={
            '381': 'IND-037'
        },
        classificacoes=('1821',),
    )

    return utils.adicionar_percentual_categorias(
        df=abastecimento_agua,
        cods_num=['72144', '72145'],
        cod_den='72129',
        nome_variavel='percentual_domicilios_rede_geral',
        indicador='IND-037',
    )


def indicador_038():
    """
    IND-038: Esgotamento sanitário
    Composição: Tabela 6805 do SIDRA
        - variáveis:
            381: Domicílios particulares permanentes ocupados (Domicílios)
        - classificacoes:
            11558: Tipo de esgotamento sanitário

    Percentual de domicílios ligados à rede geral, rede pluvial ou fossa ligada à rede: cálculo próprio
        - rede geral, rede pluvial ou fossa ligada à red (46290) / total de domicílios (46292) * 100
    """
    esgotamento_sanitario = sidra.pipeline_sidra(
        tabela='6805',
        variaveis_indicadores={
            '381': 'IND-038'
        },
        classificacoes=('11558',),
    )

    return utils.adicionar_percentual_categorias(
        df=esgotamento_sanitario,
        cods_num=['46290'],   # Rede geral, rede pluvial ou fossa ligada à rede
        cod_den='46292',      # Total de domicílios
        nome_variavel='percentual_domicilios_esgoto_rede_geral',
        indicador='IND-038',
    )

def indicador_039():
    """
    IND-039: Coleta/destinação de resíduos sólidos
    Composição: Tabela 6892 do SIDRA
        - variáveis:
            381: Domicílios particulares permanentes ocupados (Domicílios)
        - classificacoes:
            67: Destino do lixo

    Percentual de domicílios com coleta adequada: cálculo próprio
        - coleta adequada (72120 + 72121) / total de domicílios (10972) * 100
    """
    coleta_destinacao_residuos_solidos = sidra.pipeline_sidra(
        tabela='6892',
        variaveis_indicadores={
            '381': 'IND-039'
        },
        classificacoes=('67',),
    )

    return utils.adicionar_percentual_categorias(
        df=coleta_destinacao_residuos_solidos,
        cods_num=['72120', '72121'],   # coleta adequada
        cod_den='10972',               # total de domicílios
        nome_variavel='percentual_domicilios_coleta_adequada',
        indicador='IND-039',
    )

def indicador_040():
    """
    IND-040: Tempo habitual de deslocamento ao trabalho
    Composição: Tabela 10333 do SIDRA
        - variáveis:
            13377: Pessoas de 10 anos ou mais de idade, ocupadas na semana de referência, que, no trabalho principal, trabalhavam fora do domicílio (Pessoas)
        - classificacoes:
            537: Tempo habitual de deslocamento do domicílio para o trabalho principal
            1568: Nível de instrução
            58: Grupo de idade
            86: Cor ou raça
    """
    return sidra.pipeline_sidra(
        tabela='10333',
        variaveis_indicadores={
            '13377': 'IND-040'
        },
        classificacoes=('537', '1568', '58', '86'),
    )

def indicador_041():
    """
    IND-041: Local/destino do trabalho e deslocamento intermunicipal
    Composição: Tabela 10331 do SIDRA
        - variáveis:
            13556: Pessoas de 10 anos ou mais de idade residentes em domicílios particulares, ocupadas na semana de referência, [...] que, no trabalho principal, trabalhavam fora do domicílio (Pessoas)
        - classificacoes:
            537: Tempo habitual de deslocamento do domicílio para o trabalho principal
            2: Sexo
            86: Cor ou raça
            386: Classes de rendimento nominal mensal domiciliar per capita
    """
    return sidra.pipeline_sidra(
        tabela='10331',
        variaveis_indicadores={
            '13556': 'IND-041'
        },
        classificacoes=('537', '2', '86', '386'),
    )

def indicador_042():
    """
    IND-042: Modo/meio de transporte
    Composição: Tabela 10332 do SIDRA
        - variáveis:
            13377: Pessoas de 10 anos ou mais de idade, ocupadas na semana de referência, que, no trabalho principal, trabalhavam fora do domicílio (Pessoas)
        - classificacoes:
            2088: Meio de transporte em que passa mais tempo para chegar ao local de trabalho
            1568: Nível de instrução
            86: Cor ou raça

    No futuro, complementar com dados operacionais da Prefeitura/Plano de Mobilidade
    """
    return sidra.pipeline_sidra(
        tabela='10332',
        variaveis_indicadores={
            '13377': 'IND-042'
        },
        classificacoes=('2088', '1568', '86'),
    )


def indicador_043():
    """
    IND-043: Pessoas com deficiência / prevalência
    Composição: Tabela 10125 do SIDRA
        - variáveis:
            12785: Pessoas de 2 anos ou mais de idade com deficiência (Pessoas)
            13403: Percentual de pessoas de 2 anos ou mais de idade com deficiência no total de pessoas de 2 anos ou mais de idade (%)
        - classificacoes:
            2: Sexo
            58: Grupo de idade
    """
    return sidra.pipeline_sidra(
        tabela='10125',
        variaveis_indicadores={
            '12785': 'IND-043',
            '13403': 'IND-043',
        },
        classificacoes=('2', '58'),
    )


def indicador_044():
    """
    IND-044: Mortalidade infantil, causas de óbito e internações
    Composição: DATASUS
        - Mortalidade infantil: óbitos de menores de 1 ano residentes (SIM) / nascidos vivos de mães residentes (SINASC) x 1.000
        - Causas de óbito: SIM (CAUSABAS + CODMUNRES)
        - Internações: SIH (MUNIC_RES + DIAG_PRINC)
    """
    pass

def indicador_045():
    """
    IND-045: Estabelecimentos, leitos, equipamentos e profissionais
    Composição: DATASUS
        - CNES-ST: Estabelecimentos
        - CNES-LT: Leitos
        - CNES-EQ: Equipamentos
        - CNES-PF: Profissionais
    """
    pass

def indicador_046():
    """
    IND-046: Taxa de homicídios
    Composição: série AVIOL12_THOMIC do IPEA
        - Unidade: homicídios por 100 mil habitantes
    """
    return ipea.transform(
        ipea.baixar_serie(cod_serie='AVIOL12_THOMIC', nome_coluna_valor='taxa_homicidios'),
        indicador="IND-046"
    )

def indicador_047():
    """
    IND-047: Taxa de suicídios
    Composição: série AVIOL12_TSUICID do IPEA
        - Unidade: óbitos por 100 mil habitantes
    """
    return ipea.transform(
        ipea.baixar_serie(cod_serie='AVIOL12_TSUICID', nome_coluna_valor='taxa_suicidios'),
        indicador="IND-047"
    )

def indicador_048():
    """
    IND-048: Rendimento domiciliar per capita
    Composição: Tabela 10295 do SIDRA
        - variáveis:
            13431: Valor do rendimento nominal médio mensal domiciliar per capita dos moradores em domicílios particulares permanentes ocupados, exclusive os cuja condição no domicílio era pensionista, empregado(a) doméstico(a) ou parente do(a) empregado(a) doméstico(a) (Reais)
        - classificacoes:
            2: Sexo
            86: Cor ou raça
            58: Grupo de idade
    """
    return sidra.pipeline_sidra(
        tabela='10295',
        variaveis_indicadores={
            '13431': 'IND-048'
        },
        classificacoes=('2', '86', '58'),
    )
