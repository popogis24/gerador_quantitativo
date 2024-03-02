import os
import arcpy
import arcpy.management as mn
import arcpy.analysis as an
#from refact_gerador.config import settings
from database.fields_to_dissolve import FieldsToDissolve
arcpy.env.overwriteOutput = True


class FieldsToKeep:
    def __init__(self, feature_class=str):
        self.feature_class = feature_class

    def fields_to_keep(self):
        dissolve = FieldsToDissolve(self.feature_class)
        field_to_dissove_from_feature_class = dissolve.fields_to_dissolve_from_feature_class()
        filename = os.path.basename(self.feature_class)
        fields_to_keep = []
        if filename == 'Adutoras_SNIRH_ANA_2021':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y','Paralelismo']
        elif filename == 'Aerodromos_ANAC_2022':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Aerogeradores_ANEEL_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'APCB_Amazonia':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'APCB_Caatinga':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices',"NM_MUN",'OBS']
        elif filename == 'APCB_Cerrado_Pantanal':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'APCB_Mata_Atlantica':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'APCB_ZonaCosteira':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Areas_Quilombolas_INCRA':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Area','Extensao','OBS']
        elif filename == 'Areas_Urbanizadas_IBGE_2019':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Area','Extensao','OBS']
        elif filename == 'Assentamentos_INCRA':
            fields_to_keep = field_to_dissove_from_feature_class+['Distancia','Vertices','Area','Extensao','OBS']
        elif filename == 'Aves_Migratorias_Areas_Ameacadas_CEMAVE_2022':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Aves_Migratorias_Areas_Concentracao_CEMAVE_2022':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Bases_de_Combustíveis_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Bases_de_GLP_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Biomas_IBGE_2019_250000':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Area']
        elif filename == 'Blocos_Disponiveis_OPC_1009_ANP':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Cavidades_CANIE_2022':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Centrais_Geradoras_Hidrelétricas_CGH_ANEEL':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'CGH_Base_Existente_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'CGH_Expansao_Planejada_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Conservacao_Aves_IBAS':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Dutos_de_escoamento_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'Dutovias_MINFRA_2018':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'EOL_Base_Existente_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'EOL_Expansao_Planejada_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Ferrovias_MINFRA':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'Gasodutos_de_distribuição_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'Gasodutos_de_transporte_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'Geologia_IBGE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Area']
        elif filename == 'Geomorfologia_IBGE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Area']
        elif filename == 'Hidrovias_ANTAQ':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'IBAs_MataAtlantica_SaveBrasil_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Lei_Mata_Atlantica_MMA':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Localidades_IBGE_2010':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'LT_Existente_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'LT_Planejada_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'Municipios_IBGE_2022':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Area','Vertices']
        elif filename == 'Ocorrencias_Fossiliferas_CPRM':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'PCH_Base_Existente_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'PCH_Expansao_Planejada_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Pedologia_IBGE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Area']
        elif filename == 'Pequenas_Centrais_Hidrelétricas_PCH_ANEEL':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Pivo_Central_Irrigacao_ANA_2019':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Plantas_de_biodiesel_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Plantas_de_etanol_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Polos_de_processamento_de_gás_natural_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Potencial_Cavidades_ICMBio':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Area']
        elif filename == 'Reserva_Biodiversidade_Mata_Atlantica_RBMA':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Area']
        elif filename == 'Rodovia_Estadual_DNIT':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'Rodovia_Federal_DNIT':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Vertices','Paralelism']
        elif filename == 'RPPNs_ICMBio':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Sitios_Arqueologicos_IPHAN':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Subestações_Base_Existente_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Subestacoes_Expansao_Planejada_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Terminais_de_Petroleo_e_Derivados_EPE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Territorios_Quilombolas_INCRA_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Terras_Indigenas_FUNAI':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Trecho_Drenagem_ANA_2013':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Eixo_X','Eixo_Y']
        elif filename == 'UHE_Base_Existente_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Unidades_de_Conservacao_MMA':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Extensao','Area','Vertices','OBS']
        elif filename == 'Usina_Fotovoltaica_UFV_ANEEL_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Usina_Termeletricas_UTE_ANEEL_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Usinas_Hidrelétricas_UHE_ANEEL_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'UTE_Biomassa_Existente_EPE_2023':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Vegetacao_IBGE':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Extensao','Area']
        elif filename == 'Vilas_IBGE_2021':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Distancia','Vertices','Eixo_X','Eixo_Y']
        elif filename == 'Processos_Minerarios_ANM':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','Area','Extensao','Vertices']
        elif filename == 'Capitais':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','NM_MUN','Distancia']
        elif filename == 'Sedes_municipais':
            fields_to_keep = field_to_dissove_from_feature_class+['NM_UF','NM_MUN','Distancia']
        #if filename in temas_extra:
        #    fd = fields_extras.split(';')
        #    fields_to_keep = field_to_dissove_from_feature_class+list(fd)+['OBS']
        #    arcpy.AddMessage(fields_to_keep)
        #if circuito_duplo == 'true':
        #    fields_to_keep.append('Circuito')
            
        return fields_to_keep
