import sys
import time

import etl.load as loader

import etl.indicadores.demografia as demografia
import etl.indicadores.mercado_trabalho as mercado_trabalho
import etl.indicadores.sociais as sociais
import etl.indicadores.economicos as economicos

TABELAS = {
     # demografia (1-14)
    'populacao_estimada':                     demografia.indicadores_001e002,
    'populacao_urbana_rural':                 demografia.indicadores_003e004,
    'populacao_idade_sexo_faixas':            demografia.indicador_005_1,
    'populacao_idade_sexo_faixas_especifico': demografia.indicador_005_2,
    'envelhecimento':                         demografia.indicador_006,
    'idade_mediana':                          demografia.indicador_007,
    'razao_dependencia':                      demografia.indicador_008,
    'populacao_sexo':                         demografia.indicador_009,
    'densidade_demografica':                  demografia.indicador_010,
    'mig_municipio':                          demografia.indicador_011_1,
    'mig_uf':                                 demografia.indicador_011_2,
    'mig_internacional':                      demografia.indicador_011_3,
    'nascidos_vivos':                         demografia.indicador_012,
    # 'obitos_sus_erechim_residencia':        demografia.indicador_013,
    # 'populacao_projetada':                  demografia.indicador_014,

    # mercado de trabalho (15-28)
    'indicadores_empresariais':               mercado_trabalho.indicadores_015a020,
    'rendimentos_trabalho':                   mercado_trabalho.indicadores_021e022,
    'ocupacao_atividade':                     mercado_trabalho.indicador_023,
    'movimentacao_trabalhista':               mercado_trabalho.indicadores_024a026,
    'taxa_formalizacao':                      mercado_trabalho.indicador_027,
    'qualificacao_forca_trabalhista':         mercado_trabalho.indicador_028,

    # sociais (29-48)
    'alfabetizacao_15p':                      sociais.indicador_029,
    'analfabetismo_15p':                      sociais.indicador_030,
    'freq_escolar':                           sociais.indicador_031,
    'nivel_instrucao':                        sociais.indicador_032,
    # indicador 33 ainda nao extraido
    'domicilios_ocupados':                    sociais.indicador_034,
    'media_moradores_domicilio':              sociais.indicador_035,
    'condicao_ocupacao_domicilio':            sociais.indicador_036,
    'abastecimento_agua':                     sociais.indicador_037,
    'esgotamento_sanitario':                  sociais.indicador_038,
    'coleta_destinacao_residuos_solidos':     sociais.indicador_039,
    'tempo_deslocamento_trabalho':           sociais.indicador_040,
    'deslocamento_intermunicipal':            sociais.indicador_041,
    'desloc_trabalho_meio_de_transporte':     sociais.indicador_042,
    'pessoas_deficiencia':                    sociais.indicador_043,
    # indicadores 44 e 45 ainda nao extraidos
    'taxa_homicidios':                        sociais.indicador_046,
    'taxa_suicidios':                         sociais.indicador_047,
    'rend_dom_per_capita':                    sociais.indicador_048,

    # economicos (49-70)
    'pib_e_vab':                              economicos.indicadores_049_051a054,
    'pib_per_capita':                         economicos.indicador_050,
    'empresas_cnae':                          economicos.indicadores_055e056,
    'producao_agricola':                      economicos.indicadores_057a060,
    'quant_rebanhos':                         economicos.indicador_061,
    'info_leite':                             economicos.indicador_062,
    'silvicultura':                           economicos.indicador_063_1,
    'extrativismo':                           economicos.indicador_063_2,
    'exportacoes_importacoes':                economicos.indicadores_064a066,
    'credito_rural':                          economicos.indicadores_067e068,
    'hospedagem':                             economicos.indicador_069,
    'invest_publico_municipal':               economicos.indicador_070,
}


def etl():
    falhas = []

    for nome_tabela, fn_extrair_df in TABELAS.items():
        print(f"===== Extraindo dados para compor a tabela: {nome_tabela} =====")
        print(f"Função sendo executada: {fn_extrair_df.__name__}\n")

        try:
            df = fn_extrair_df()
            print(f"Indicadores: {df['indicador'].unique()}")
            loader.load_df(df, nome_tabela)
        except Exception as e:
            print(f"  ERRO em {nome_tabela}: {e!r}")
            falhas.append(nome_tabela)

        print("\n")

    print("==== Falhas? ====")

    if falhas:
        print(f"\n{len(falhas)} tabela(s) falharam: {', '.join(falhas)}")
        return 1
    else:
        print("Nenhuma falha na extração!")

    return 0


def main() -> int:
    inicio = time.perf_counter()

    try:
        return etl()
    finally:
        fim     = time.perf_counter()
        demorou = fim - inicio

        horas = int(demorou // 3600)
        mins  = int(demorou % 3600 // 60)
        segs = demorou % 60

        print(f"\no ETL demorou {horas}h {mins}min {segs:.2f}s para finalizar.")


if __name__ == "__main__":
    sys.exit(main())
