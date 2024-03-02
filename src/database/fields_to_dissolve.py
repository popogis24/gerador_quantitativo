import os
import arcpy

class FieldsToDissolve:
    def __init__(self, feature_class):
        self.feature_class = feature_class

    def fields_to_dissolve_from_feature_class(self):
        filename = os.path.basename(self.feature_class)
        fields_interesse = []
        if filename == 'Adutoras_SNIRH_ANA_2021':
            fields_interesse = ['adt_nm_adu','adt_status']
        elif filename == 'Aerodromos_ANAC_2022':
            fields_interesse = ['Codigo_OAC','CIAD','Denominaca']
        elif filename == 'Aerogeradores_ANEEL_2023':
            fields_interesse = ['NOME_EOL','DEN_AEG','POT_MW','CEG','OPERACAO']
        elif filename == 'APCB_Amazonia':
            fields_interesse = ['Import_bio','Prior_acao','COD_Area']
        elif filename == 'APCB_Caatinga':
            fields_interesse = ['Import_bio','Prior_acao','COD_area','Nome_area']
        elif filename == 'APCB_Cerrado_Pantanal':
            fields_interesse = ['Import_bio','Prior_acao','COD_area','NOME']
        elif filename == 'APCB_Mata_Atlantica':
            fields_interesse = ['ImportBio_','Prioridade','COD_area']
        elif filename == 'APCB_ZonaCosteira':
            fields_interesse = ['NOME_AP','IMP','PRIO']
        elif filename == 'Areas_Quilombolas_INCRA':
            fields_interesse = ['nm_comunid','nm_municip','responsave']
        elif filename == 'Areas_Urbanizadas_IBGE_2019':
            fields_interesse = ['Densidade','Tipo','Comparacao']
        elif filename == 'Assentamentos_INCRA':
            fields_interesse = ['nome_proje','municipio','capacidade','num_famili']
        elif filename == 'Aves_Migratorias_Areas_Ameacadas_CEMAVE_2022':
            fields_interesse = [] #não tem campos de interesse, verificar se não vai ter bug
        elif filename == 'Aves_Migratorias_Areas_Concentracao_CEMAVE_2022':
            fields_interesse = [] #não tem campos de interesse, verificar se não vai ter bug
        elif filename == 'Bases_de_Combustíveis_EPE':
            fields_interesse = ['nome_base','munic']
        elif filename == 'Bases_de_GLP_EPE':
            fields_interesse = ['nome_base','munic','razao_soci']
        elif filename == 'Biomas_IBGE_2019_250000':
            fields_interesse = ['Bioma']
        elif filename == 'Blocos_Disponiveis_OPC_1009_ANP':
            fields_interesse = ['nome_bacia','nomenclatu','nome_setor']
        elif filename == 'Cavidades_CANIE_2022':
            fields_interesse = ['Caverna','Municipio','Localidade']
        elif filename == 'Centrais_Geradoras_Hidrelétricas_CGH_ANEEL':
            fields_interesse = ['NOME']
        elif filename == 'CGH_Base_Existente_EPE':
            fields_interesse = ['NOME']
        elif filename == 'CGH_Expansao_Planejada_EPE':
            fields_interesse = ['Nome']
        elif filename == 'Conservacao_Aves_IBAS':
            fields_interesse = ['Nome_1']
        elif filename == 'Dutos_de_escoamento_EPE':
            fields_interesse = ['Nome_Dut_1','Categoria']
        elif filename == 'Dutovias_MINFRA_2018':
            fields_interesse = ['Nome_Duto']
        elif filename == 'EOL_Base_Existente_EPE':
            fields_interesse = ['Nome']
        elif filename == 'EOL_Expansao_Planejada_EPE':
            fields_interesse = ['nome']
        elif filename == 'Ferrovias_MINFRA':
            fields_interesse = ['tip_situac','bitola']
        elif filename == 'Gasodutos_de_distribuição_EPE_2023':
            fields_interesse = ['Distrib']
        elif filename == 'Gasodutos_de_transporte_EPE_2023':
            fields_interesse = ['Nome_Dut_1','Categoria']
        elif filename == 'Geologia_IBGE':
            fields_interesse = ['nm_unidade']
        elif filename == 'Geomorfologia_IBGE':
            fields_interesse = ['nm_unidade']
        elif filename == 'Hidrovias_ANTAQ':
            fields_interesse = ['HID_NM','HID_DS_CUR']
        elif filename == 'IBAs_MataAtlantica_SaveBrasil_2023':
            fields_interesse = ['Nome_1','Bioma']
        elif filename == 'Lei_Mata_Atlantica_MMA':
            fields_interesse = [] #não tem campos de interesse, verificar se não vai ter bug
        elif filename == 'Localidades_IBGE_2010':
            fields_interesse = ['NM_LOCALID']
        elif filename == 'LT_Existente_EPE_2023':
            fields_interesse = ['Nome','Tensao','Ano_opera']
        elif filename == 'LT_Planejada_EPE_2023':
            fields_interesse = ['Nome','Tensao']
        elif filename == 'Municipios_IBGE_2022':
            fields_interesse = ['NM_MUN']
        elif filename == 'Ocorrencias_Fossiliferas_CPRM':
            fields_interesse = ['LOCALIDADE']
        elif filename == 'PCH_Base_Existente_EPE_2023':
            fields_interesse = ['NOME']
        elif filename == 'PCH_Expansao_Planejada_EPE_2023':
            fields_interesse = ['nome']
        elif filename == 'Pedologia_IBGE':
            fields_interesse = ['legenda']
        elif filename == 'Pequenas_Centrais_Hidrelétricas_PCH_ANEEL':
            fields_interesse = ['NOME']
        elif filename == 'Pivo_Central_Irrigacao_ANA_2019':
            fields_interesse = ['NM_MUNICIP']
        elif filename == 'Plantas_de_biodiesel_EPE':
            fields_interesse = ['Nome']
        elif filename == 'Plantas_de_etanol_EPE':
            fields_interesse = ['Nome']
        elif filename == 'Polos_de_processamento_de_gás_natural_EPE':
            fields_interesse = ['Nome']
        elif filename == 'Potencial_Cavidades_ICMBio':
            fields_interesse = ['GRAU_DE_PO']
        elif filename == 'Reserva_Biodiversidade_Mata_Atlantica_RBMA':
            fields_interesse = ['CLASSE']
        elif filename == 'Rodovia_Estadual_DNIT':
            fields_interesse =['Unidade_Fe','Codigo_Rod']
        elif filename == 'Rodovia_Federal_DNIT':
            fields_interesse =['Codigo_BR']
        elif filename == 'RPPNs_ICMBio':
            fields_interesse = ['nome']
        elif filename == 'Sitios_Arqueologicos_IPHAN':
            fields_interesse = ['identifica']
        elif filename == 'Subestacoes_Base_Existente_EPE_2023':
            fields_interesse = ['Nome','Tensao','Ano_Opera']
        elif filename == 'Subestacoes_Expansao_Planejada_EPE_2023':
            fields_interesse = ['Nome','Tensao','Ano_Opera']
        elif filename == 'Terminais_de_Petroleo_e_Derivados_EPE':
            fields_interesse = ['nome_ter','munic']
        elif filename == 'Territorios_Quilombolas_INCRA_2023':
            fields_interesse = ['nm_comunid','nm_municip','nr_process','fase','responsave']
        elif filename == 'Terras_Indigenas_FUNAI':
            fields_interesse = ['terrai_nom','municipio_','etnia_nome']
        elif filename == 'Trecho_Drenagem_ANA_2013':
            fields_interesse = []#não tem campos de interesse, verificar se não vai ter bug
        elif filename == 'UHE_Base_Existente_EPE_2023':
            fields_interesse = ['NOME']
        elif filename == 'Unidades_de_Conservacao_MMA':
            fields_interesse =['NOME_UC1','CATEGORI3','ESFERA5','GRUPO4','ANO_CRIA6']
        elif filename == 'Usina_Fotovoltaica_UFV_ANEEL_2023':
            fields_interesse = ['nome','munic']
        elif filename == 'Usina_Termeletricas_UTE_ANEEL_2023':
            fields_interesse = ['nome']
        elif filename == 'Usinas_Hidrelétricas_UHE_ANEEL_2023':
            fields_interesse = ['NOME']
        elif filename == 'UTE_Biomassa_Existente_EPE_2023':
            fields_interesse = ['nome']
        elif filename == 'Vegetacao_IBGE':
            fields_interesse = ['legenda']
        elif filename == 'Vilas_IBGE_2021':
            fields_interesse = ['nome']
        elif filename == 'Processos_Minerarios_ANM':
            fields_interesse = ['PROCESSO','ANO','FASE','NOME','SUBS','AREA_HA','DSProcesso']
        elif filename == 'Capitais':
            fields_interesse = ['Nome','Tipo_Capit']
        elif filename == 'Sedes_municipais':
            fields_interesse = ['Nome_Sede']

        return fields_interesse