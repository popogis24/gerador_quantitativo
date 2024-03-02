import os
import arcpy
import arcpy.management as mn
import arcpy.analysis as an
import arcpy.conversion as cs
#from refact_gerador.config import settings
arcpy.env.overwriteOutput = True

class FormatFeatureClass():
    arcpy.env.overwriteOutput = True
    def __init__(self, analyzed_product=str, feature_class=str, fields_to_dissolve=str, workspace=str, storage_dataset=str):
        
        self.analyzed_product = analyzed_product
        self.feature_class = feature_class
        self.fields_to_dissolve = fields_to_dissolve
        self.storage_dataset = storage_dataset
        self.workspace = workspace
        os.makedirs(self.workspace, exist_ok=True)

        self.feature_class_name = os.path.basename(self.feature_class)
    
    def format_fields(self):
        formatted_field = self.fields_to_dissolve.split(";")
        return formatted_field

    def repair_geometry(self):
        mn.RepairGeometry(self.feature_class)
    
    def clip_feature_class(self):
        area_of_interest = an.PairwiseBuffer(
            in_features=self.analyzed_product,
            out_feature_class= "buffer",
            buffer_distance_or_field=50000,
            dissolve_option="ALL")

        clipped_feature_class = an.PairwiseClip(
            in_features=self.feature_class,
            clip_features=area_of_interest,
            out_feature_class=fr"{self.feature_class_name}_clipped_data")
        return clipped_feature_class

    def set_political_boundaries(self):
        uf_address = r'C:\refact_gerador\ibge\Divisao_Estadual.shp'
        feature_class_with_state_boundaries = an.PairwiseIntersect(
            in_features=[self.clip_feature_class(), uf_address],
            out_feature_class=fr"{self.feature_class_name}_byUF")
        
        municipio_address = r'C:\refact_gerador\ibge\Divisao_Municipal.shp'
        feature_class_with_municipal_boundaries = an.PairwiseIntersect(
            in_features=[feature_class_with_state_boundaries, municipio_address],
            out_feature_class=fr"{self.feature_class_name}_byMunicipio")

        return feature_class_with_municipal_boundaries
    
    def dissolve(self):
        dissolved_theme = an.PairwiseDissolve(in_features=self.set_political_boundaries(),
                            out_feature_class=fr"{self.feature_class_name}_dissolved",
                            dissolve_field=self.fields_to_dissolve, # SE TIVER OU SE TIVER MUNICIPIO, ADD
        )
        return dissolved_theme

    def store_shapefile_in_database(self):
        formatted_feature_class = cs.FeatureClassToFeatureClass(
            in_features = self.dissolve(),
            out_path=self.storage_dataset,
            out_name=fr'{self.feature_class_name}_')
        
        arcpy.AddMessage(f"Shapefile {self.feature_class_name} stored in {self.storage_dataset}")
        return formatted_feature_class

    def get_formatted_feature_class(self):
        #arcpy.env.workspace = self.storage_dataset
        #list_fc_storage_dataset = arcpy.ListFeatureClasses()
        #if self.feature_class+"_" in list_fc_storage_dataset:
        #    mn.Delete(self.feature_class+"_")
        arcpy.env.workspace = self.workspace
        self.repair_geometry()
        formatted_feature_class = self.store_shapefile_in_database()

        return formatted_feature_class
