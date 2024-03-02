import os
import arcpy
import arcpy.management as mn
import arcpy.analysis as an
#from refact_gerador.config import settings
arcpy.env.overwriteOutput = True

class NearAnalysis():
    def __init__(self, analyzed_product=str, formatted_feature_class=str, storage_dataset=str, geodesic=str):
        self.analyzed_product = analyzed_product
        self.formatted_feature_class = formatted_feature_class
        self.storage_dataset = storage_dataset
        arcpy.env.workspace = storage_dataset
        self.buffer_distance = 10000
        self.geodesic = geodesic
    
    def nearest_feature_class(self):
        temp_formatted_feature_class = arcpy.management.CopyFeatures(self.formatted_feature_class, f'{self.formatted_feature_class}_temp')
        if self.geodesic == 'true':
            arcpy.analysis.Near(in_features = temp_formatted_feature_class, near_features = self.analyzed_product, search_radius = self.buffer_distance, method = 'GEODESIC')
        else:
            arcpy.analysis.Near(in_features = temp_formatted_feature_class, near_features = self.analyzed_product, search_radius = self.buffer_distance)
        
        expression = "round(!NEAR_DIST! / 1000.0, 3)"
        arcpy.CalculateField_management(temp_formatted_feature_class, 'Distancia', expression, "PYTHON", field_type = "FLOAT")
        joinedfc = arcpy.management.JoinField(in_data=temp_formatted_feature_class, in_field='NEAR_FID', join_table=self.analyzed_product, join_field='OBJECTID')
        selectfc = arcpy.management.SelectLayerByAttribute(in_layer_or_view=joinedfc, selection_type="NEW_SELECTION", where_clause="NEAR_FID <> -1")
        nearest_features_from_product = arcpy.CopyFeatures_management(selectfc, fr'{self.formatted_feature_class}_Distance')
        nearest_features_from_product = os.path.join(self.storage_dataset, f'{self.formatted_feature_class}_Distance')

        return nearest_features_from_product
