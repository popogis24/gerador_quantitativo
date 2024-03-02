
class Tradutor:
    def __init__(self, sheet):
        self.sheet = sheet


    def tradutor(self):
        dicionario = {
        'adt_nm_adu': 'Nome da adutora',
        'adt_status': 'Status',
        'adt_uf': 'UF da adutora',
        'PROCESSO': 'Processo',
        'ANO': 'Ano',
        'FASE': 'Fase',
        'SUBS': 'Substância',
        'AREA_HA': 'Área do processo (ha)',
        'DSProcesso': 'Descrição do processo',
        'Codigo_OAC': 'Código OAC',
        'Comparacao': 'Comparação',
        'CIAD': 'CIAD',
        'Denominaca': 'Denominação',
        'NOME_EOL': 'Nome',
        'DEN_AEG': 'Denominação',
        'POT_MW': 'Potência (mW)', 
        'CEG': 'CEG',
        'nome_proje': 'Nome do projeto',
        'OPERACAO': 'Operação',
        'Import_bio': 'Importância biológica',
        'Prior_acao': 'Prioridade da ação',
        'COD_Area': 'Código da área',
        'Nome_area': 'Nome da área',
        'NOME': 'Nome',
        'municipio_': 'Município',
        'num_familia': 'Número de famílias',
        'ImportBio': 'Importância biológica',
        'Prioridade': 'Prioridade',
        'COD_area': 'Código da área',
        'NOME_AP': 'Nome da APCB',
        'IMP': 'Importância',
        'PRIO': 'Prioridade',
        'nome_base': 'Nome da base',
        'munic': 'Município',
        'razao_soci': 'Razão social',
        'Bioma': 'Bioma',
        'nome_bacia': 'Nome da bacia',
        'nomenclatu': 'Nomenclatura',
        'nome_setor': 'Nome do setor',
        'Caverna': 'Caverna',
        'Municipio': 'Município',
        'Localidade': 'Localidade',
        'tip_situac': 'Tipo de situação',
        'bitola': 'Bitola',
        'Distrib': 'Distribuição',
        'Nome_Dut_1': 'Nome',
        'Categoria': 'Categoria',
        'nm_unidade': 'Nome da unidade',
        'HID_NM': 'Nome da hidrovia',
        'HID_DS_CUR': 'Descrição',
        'Nome_1': 'Nome',
        'NM_LOCALID': 'Nome da localidade',
        'Tensao': 'Tensão',
        'Ano_opera': 'Ano de operação',
        'NM_MUNICIP': 'Município',
        'SIGLA_UF': 'Sigla UF',
        'LOCALIDADE': 'Localidade',
        'Nome_Duto': 'Nome do duto',
        'NOME_ter': 'Nome',
        'GRAU_DE_PO': 'Grau de potencialidade',
        'CLASSE': 'Classe',
        'Tipo_Trech': 'Tipo de trecho',
        'Unidade_Fe': 'UF da rodovia',
        'Codigo_Rod': 'Código da rodovia',
        'Nome_Tipo': 'Nome',
        'Codigo_BR': 'Código da BR',
        'nome': 'Nome',
        'Identifica': 'Identificação',
        'nm_comunid': 'Nome da comunidade',
        'nm_municip': 'Município',
        'nr_process': 'Número do processo',
        'fase': 'Fase',
        'responsave': 'Responsável',
        'terrai_nom': 'Nome da Terra Indígena',
        'etnia_nome': 'Nome da etnia',
        'Extensao' : 'Extensão (km)',
        'Area' : 'Área (ha)',
        'Eixo_X' : 'Eixo X',
        'Eixo_Y' : 'Eixo Y',
        'Paralelism' : 'Paralelismo (Metros)',
        'Distancia' : 'Distância (km)',
        'Vertices' : 'Vértices',
        'OBS' : 'Observação',
        'identifica' : 'Identificação',
        'legenda' : 'Legenda',
        'NOME_UC1' : 'Nome da UC',
        'GRUPO4' : 'Grupo',
        'CATEGORI3' : 'Categoria',
        'ESFERA5' : 'Esfera',
        'ANO_CRIA6' : 'Ano de criação',
        'ImportBio_' : 'Importância biológica',
        'NM_UF' : 'UF',
        'NM_MUN' : 'Município'
        }

        for row in self.sheet.iter_rows():
            for cell in row:
                if cell.value in dicionario.keys():
                    cell.value = dicionario[cell.value]