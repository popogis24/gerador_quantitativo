import os
import arcpy
import arcpy.management as mn
import arcpy.analysis as an
import openpyxl as op
import shutil


#from database.supported_themes import SupportedThemes
#from feature_formatting.format_feature_class import FormatFeatureClass
#from database.fields_to_dissolve import FieldsToDissolve
#from database.fields_to_keep import FieldsToKeep
#from geometric_analysis.near_analysis import NearAnalysis
#from geometric_analysis.interception_analysis import InterceptionAnalysis
#from table_conversion.xlsx_conversion import XLSXConversion

from database.supported_themes import SupportedThemes
from feature_formatting.format_feature_class import FormatFeatureClass
from database.fields_to_dissolve import FieldsToDissolve
from database.fields_to_keep import FieldsToKeep
from geometric_analysis.near_analysis import NearAnalysis
from geometric_analysis.interception_analysis import InterceptionAnalysis
from table_conversion.xlsx_conversion import XLSXConversion

#arcpy.env.overwriteOutput = True
#analyzed_product = arcpy.GetParameterAsText(0)#needed
#analyzed_product_area = arcpy.GetParameterAsText(1)#optional
#circuito_duplo = arcpy.GetParameterAsText(2)#optional
#geodesic = arcpy.GetParameterAsText(3)#bool optional
#theme_list = arcpy.GetParameterAsText(7)#needed
#extra_theme = arcpy.GetParameterAsText(4)#optional
#extra_theme_field = arcpy.GetParameterAsText(5)#optional
#extra_theme_analysis = arcpy.GetParameterAsText(6)#optional
#excel_file_folder = arcpy.GetParameterAsText(8)#needed

class Pipeline():
    def __init__(self, analyzed_product, analyzed_product_area, 
                 theme_list, extra_theme, extra_theme_field, 
                 extra_theme_analysis, geodesic, excel_file_folder, circuito_duplo):
        
        self.analyzed_product = analyzed_product
        self.analyzed_product_area = analyzed_product_area
        self.storage_dataset = self.create_dataset()
        self.workspace = self.create_workspace()
        self.theme_list = theme_list
        self.extra_theme = extra_theme
        self.extra_theme_field = extra_theme_field.split(";")
        self.extra_theme_analysis = extra_theme_analysis
        self.geodesic = geodesic
        self.excel_file_folder = excel_file_folder
        self.dissolved_product_area_path = self.dummy_dissolve()[0]
        self.dissolved_product_path = self.dummy_dissolve()[1]
        self.circuito_duplo = circuito_duplo
        
        self.workbook_distancia = os.path.join(self.excel_file_folder, "Distancia.xlsx")
        self.workbook_area = os.path.join(self.excel_file_folder, "Area.xlsx")
        self.workbook_extensao = os.path.join(self.excel_file_folder, "Extensao.xlsx")

    def create_workspace(self):
        os.makedirs('workspace', exist_ok=True)
        workspace_folder = os.path.join(os.getcwd(), 'workspace')
        return workspace_folder
    
    def create_dataset(self):
        if not os.path.exists(os.path.join(os.getcwd(), 'storage.gdb')):  
            mn.CreateFileGDB(out_folder_path=os.getcwd(), out_name='storage')
            mn.CreateFeatureDataset(out_dataset_path=os.path.join(os.getcwd(), 'storage.gdb'), out_name='dataset', spatial_reference=self.analyzed_product)
        return os.path.join(os.getcwd(), 'storage.gdb', 'dataset')

    
    def delete_workspace_folder(self):
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)


    def delete_dataset(self):
        url_storage = os.path.join(os.getcwd(), 'storage.gdb')
        if os.path.exists(url_storage):
            shutil.rmtree(url_storage) #####DAR UM JEITO DE DELETAR ESTA MERDA


    def save_workbook_if_not_exists(self, workbook, filepath):
        if not os.path.exists(filepath):
            workbook.save(filepath)

    def create_excel_directory(self):
        workbook = op.Workbook()
        file_names = ["Distancia.xlsx", "Area.xlsx", "Extensao.xlsx"]
        for file in file_names:
            self.save_workbook_if_not_exists(workbook, os.path.join(self.excel_file_folder, file))


    def themelist_check(self):
        for theme in self.theme_list:
            list_of_supported_themes = SupportedThemes.list_of_supported_themes()
            if os.path.basename(theme) not in list_of_supported_themes:
                arcpy.AddError(f"O tema {theme} não é suportado, verifique se o nome da camada está na lista de temas suportados, caso não esteja, utilize a função de temas extras")
                raise arcpy.ExecuteError

            
    def understand_input_parameters(self):
        if self.extra_theme == "":
            self.run_normal_pipeline()
        else:
            self.run_extra_pipeline()

    
    def run_extra_pipeline(self):
        self.create_excel_directory()
        self.themelist_check()
        if self.themelist_check == True:
            arcpy.AddWarning("O tema foi selecionado como Extra apesar de seus metadados estarem presentes na database da ferramenta. Serão utilizadas as fields que você definiu para a análise.")
        fields_to_dissolve = self.extra_theme_field
        unaltered_fields_to_keep = fields_to_dissolve + self.extra_theme_analysis
        if "NM_UF" in unaltered_fields_to_keep:
            fields_to_dissolve.append("NM_UF")
        if "NM_MUN" in unaltered_fields_to_keep:
            fields_to_dissolve.append("NM_MUN")
        if self.circuito_duplo == 'true':
            unaltered_fields_to_keep.append('Circuito')
        formatted_feature_class_instance = FormatFeatureClass(analyzed_product=self.analyzed_product,
                                                            feature_class=self.extra_theme,
                                                            fields_to_dissolve=fields_to_dissolve,
                                                            workspace=self.workspace,
                                                            storage_dataset=self.storage_dataset)
        formatted_feature_class = formatted_feature_class_instance.get_formatted_feature_class()
        theme_shapetype = arcpy.Describe(formatted_feature_class).shapeType
        if "Distancia" in unaltered_fields_to_keep:
            fields_to_keep = [field for field in unaltered_fields_to_keep if field not in ["Area", "Extensao"]]
            NearAnalysis_Instance = NearAnalysis(self.analyzed_product, formatted_feature_class, self.storage_dataset, self.geodesic)
            table_description = fr"Distancia do tema {os.path.basename(self.extra_theme)} em relação a linha {os.path.basename(self.analyzed_product)}"
            quantified_fc = NearAnalysis_Instance.nearest_feature_class()
            self.to_excel(quantified_fc, fields_to_keep, self.workbook_distancia, table_description, "Distancia")

        if "Area" in unaltered_fields_to_keep:
            if "Vertices" in unaltered_fields_to_keep:
                product_area = self.analyzed_product_area
                product = self.analyzed_product
            elif "Vertices" not in unaltered_fields_to_keep:
                product_area = self.dissolved_product_area_path
                product = self.dissolved_product_path
            fields_to_keep = [field for field in unaltered_fields_to_keep if field not in ["Distancia", "Extensao"]]
            InterceptionAnalysis_Instance = InterceptionAnalysis(self.analyzed_product, self.analyzed_product_area, formatted_feature_class, self.storage_dataset, self.geodesic)
            quantified_fc = InterceptionAnalysis_Instance.area_intersect_feature_class()
            if theme_shapetype == "Polygon":
                table_description = fr"Área do poligono do tema {os.path.basename(self.extra_theme)} interceptada pelo poligono de interesse, que no caso é {os.path.basename(self.analyzed_product_area)}"
                self.to_excel(quantified_fc, fields_to_keep, self.workbook_area, table_description, "Area")
            else:
                arcpy.AddWarning(fr"O tema {os.path.basename(self.extra_theme)} é do tipo {theme_shapetype}, não é possível realizar a análise de área")
            
        if "Extensao" in unaltered_fields_to_keep:
            fields_to_keep = [field for field in unaltered_fields_to_keep if field not in ["Distancia", "Area"]]
            if "Vertices" in unaltered_fields_to_keep:
                product_area = self.analyzed_product_area
                product = self.analyzed_product
            elif "Vertices" not in unaltered_fields_to_keep:
                product_area = self.dissolved_product_area_path
                product = self.dissolved_product_path
            if theme_shapetype == "Polygon":
                InterceptionAnalysis_Instance = InterceptionAnalysis(product, product_area, formatted_feature_class, self.storage_dataset, self.geodesic)
                quantified_fc = InterceptionAnalysis_Instance.extension_intersect_feature_class()
                table_description = fr"Extensão da linha {os.path.basename(self.analyzed_product)} que intercepta o poligono do tema {os.path.basename(self.extra_theme)}"
                self.to_excel(quantified_fc, fields_to_keep, self.workbook_extensao, table_description, "Extensao")
            elif theme_shapetype == "Polyline":
                InterceptionAnalysis_Instance = InterceptionAnalysis(product, product_area, formatted_feature_class, self.storage_dataset, self.geodesic)
                quantified_fc = InterceptionAnalysis_Instance.extension_by_line_intersect_feature_class()
                table_description = fr"Pontos em que a linha do tema {os.path.basename(self.analyzed_product)} intercepta o poligono de interesse, que no caso é: {os.path.basename(self.extra_theme)}"
                self.to_excel(quantified_fc, fields_to_keep, self.workbook_extensao, table_description, "Extensao")


    def to_excel(self, feature_class, related_field, excel_file, table_description, category):
        xlsx_conversion = XLSXConversion(feature_class, related_field, excel_file, table_description, category)
        xlsx_conversion.get_complete_sheet() ##instanciar direto na funcao run_normal_pipeline

    def dummy_dissolve(self):
        dissolved_product_path = os.path.join(self.workspace, "dissolved_product.shp")
        dissolved_product_area_path = os.path.join(self.workspace, "dissolved_product_area.shp")
        if not os.path.exists(dissolved_product_path):
            mn.Dissolve(self.analyzed_product, dissolved_product_path)
        if not os.path.exists(dissolved_product_area_path):
            mn.Dissolve(self.analyzed_product_area, dissolved_product_area_path)

        return dissolved_product_area_path, dissolved_product_path

    def run_normal_pipeline(self): #$###### ADICIONAR O CAMPO DE DISSOLVE DO PRODUTO
        self.create_excel_directory()
        self.themelist_check()
        for theme in self.theme_list:
            fields_to_dissolve_instance = FieldsToDissolve(theme)
            fields_to_dissolve = fields_to_dissolve_instance.fields_to_dissolve_from_feature_class()
            unaltered_fields_to_keep = FieldsToKeep(theme).fields_to_keep()
            if "NM_UF" in unaltered_fields_to_keep:
                fields_to_dissolve.append("NM_UF")
            if "NM_MUN" in unaltered_fields_to_keep:
                fields_to_dissolve.append("NM_MUN")
            if self.circuito_duplo == 'true':
                unaltered_fields_to_keep.append('Circuito')
            formatted_feature_class_instance = FormatFeatureClass(analyzed_product=self.analyzed_product,
                                                feature_class=theme,
                                                fields_to_dissolve=fields_to_dissolve,
                                                workspace=self.workspace,
                                                storage_dataset=self.storage_dataset)
            formatted_feature_class = formatted_feature_class_instance.get_formatted_feature_class()
            theme_shapetype = arcpy.Describe(formatted_feature_class).shapeType
            if "Distancia" in unaltered_fields_to_keep:
                fields_to_keep = [field for field in unaltered_fields_to_keep if field not in ["Area", "Extensao"]]
                NearAnalysis_Instance = NearAnalysis(self.analyzed_product, formatted_feature_class, self.storage_dataset, self.geodesic)
                table_description = fr"Distancia do tema {os.path.basename(theme)} em relação a linha {os.path.basename(self.analyzed_product)}"
                quantified_fc = NearAnalysis_Instance.nearest_feature_class()
                self.to_excel(quantified_fc, fields_to_keep, self.workbook_distancia, table_description, "Distancia")

            if "Area" in unaltered_fields_to_keep:
                if "Vertices" in unaltered_fields_to_keep:
                    product_area = self.analyzed_product_area
                    product = self.analyzed_product
                elif "Vertices" not in unaltered_fields_to_keep:
                    product_area = self.dissolved_product_area_path
                    product = self.dissolved_product_path
                fields_to_keep = [field for field in unaltered_fields_to_keep if field not in ["Distancia", "Extensao"]]
                InterceptionAnalysis_Instance = InterceptionAnalysis(product, product_area, formatted_feature_class, self.storage_dataset, self.geodesic)
                quantified_fc = InterceptionAnalysis_Instance.area_intersect_feature_class()
                if theme_shapetype == 'Polygon':
                    table_description = fr"Área do poligono do tema {os.path.basename(theme)} interceptada pelo poligono de interesse, que no caso é: {os.path.basename(self.analyzed_product_area)}"
                    self.to_excel(quantified_fc, fields_to_keep, self.workbook_area, table_description, "Area")
                else:
                    arcpy.AddWarning(fr"O tema {os.path.basename(self.extra_theme)} é do tipo {theme_shapetype}, não é possível realizar a análise de área")

            if "Extensao" in unaltered_fields_to_keep:
                if "Vertices" in unaltered_fields_to_keep:
                    product_area = self.analyzed_product_area
                    product = self.analyzed_product
                elif "Vertices" not in unaltered_fields_to_keep:
                    product_area = self.dissolved_product_area_path
                    product = self.dissolved_product_path
                fields_to_keep = [field for field in unaltered_fields_to_keep  if field not in ["Distancia", "Area"]]
                if theme_shapetype == "Polygon":
                    InterceptionAnalysis_Instance = InterceptionAnalysis(product, product_area, formatted_feature_class, self.storage_dataset, self.geodesic)
                    quantified_fc = InterceptionAnalysis_Instance.extension_intersect_feature_class()
                    table_description = fr"Extensão da linha {os.path.basename(self.analyzed_product)} que intercepta o poligono do tema {os.path.basename(theme)}"
                    self.to_excel(quantified_fc, fields_to_keep , self.workbook_extensao, table_description, "Extensao")
                elif theme_shapetype == "Polyline":
                    InterceptionAnalysis_Instance = InterceptionAnalysis(product, product_area, formatted_feature_class, self.storage_dataset, self.geodesic)
                    quantified_fc = InterceptionAnalysis_Instance.extension_by_line_intersect_feature_class()
                    table_description = fr"Pontos em que a linha do tema {os.path.basename(self.analyzed_product)} intercepta o poligono de interesse, que no caso é: {os.path.basename(theme)}"
                    self.to_excel(quantified_fc, fields_to_keep, self.workbook_extensao, table_description, "Extensao")


#if __name__ == "__main__":
#    pipeline = Pipeline(analyzed_product, analyzed_product_area,
#                 theme_list, extra_theme, extra_theme_field, 
#                 extra_theme_analysis, geodesic, excel_file_folder)
#    pipeline.understand_input_parameters()
#    pipeline.delete_workspace_folder()
#    pipeline.delete_dataset()
