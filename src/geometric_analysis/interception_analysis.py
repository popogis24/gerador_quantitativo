import os
import arcpy
import arcpy.management as mn
import arcpy.analysis as an
#from refact_gerador.config import settings
arcpy.env.overwriteOutput = True

class InterceptionAnalysis():
    def __init__(self, analyzed_product=str, analyzed_product_area= str, formatted_feature_class=str, storage_dataset=str, geodesic=str):
        self.analyzed_product = analyzed_product
        self.analyzed_product_area = analyzed_product_area
        self.formatted_feature_class = formatted_feature_class
        self.geodesic = geodesic
        self.storage_dataset = storage_dataset
        arcpy.env.workspace = storage_dataset
    
    def extension_intersect_feature_class(self):
        expression_len = ''
        if self.geodesic == 'true':
            expression_len = '!SHAPE.geodesicLength@KILOMETERS!'
        else:
            expression_len = '!shape.length@kilometers!'
        extension_intersected_feature_class = an.PairwiseIntersect(
            in_features=[self.formatted_feature_class, self.analyzed_product],
            out_feature_class=fr'{self.formatted_feature_class}_extension')
        
        mn.CalculateField(in_table= extension_intersected_feature_class,
                                        field='Extensao',
                                        expression=expression_len,
                                        field_type = "FLOAT")
        
        arcpy.management.CalculateField(in_table= extension_intersected_feature_class,
                                        field='Extensao',
                                        expression='round(!Extensao!, 3)',
                                        field_type = "FLOAT")
        
        
        extension_intersected_feature_class = os.path.join(self.storage_dataset, f'{self.formatted_feature_class}_extension')
        return extension_intersected_feature_class
    
    def extension_by_line_intersect_feature_class(self):
        expression_len = ''
        if self.geodesic == 'true':
            expression_len = '!SHAPE.geodesicLength@KILOMETERS!'
        else:
            expression_len = '!shape.length@kilometers!'
        
        extension_intersected_feature_class = an.PairwiseIntersect(
            in_features=[self.formatted_feature_class, self.analyzed_product_area],
            out_feature_class=fr'{self.formatted_feature_class}_extensionbyline')
        
        arcpy.management.CalculateField(in_table= extension_intersected_feature_class,
                                        field='Extensao',
                                        expression=expression_len,
                                        field_type = "FLOAT")
        
        mn.CalculateField(in_table= extension_intersected_feature_class,
                                field='Extensao',
                                expression='round(!Extensao!, 3)',
                                field_type = "FLOAT")
        
        
        extension_intersected_feature_class = os.path.join(self.storage_dataset, f'{self.formatted_feature_class}_extensionbyline')
        return extension_intersected_feature_class
    
    
    def area_intersect_feature_class(self):
        if self.geodesic == 'true':
            expression_area = '!SHAPE.geodesicArea@HECTARES!'
        else:
            expression_area = '!shape.area@hectares!'
        
        area_intersected_feature_class = an.PairwiseIntersect(
            in_features=[self.formatted_feature_class, self.analyzed_product_area],
            out_feature_class=fr'{self.formatted_feature_class}_area')
        
        mn.CalculateField(in_table= area_intersected_feature_class,
                                        field='Area',
                                        expression=expression_area,
                                        field_type="FLOAT")
        mn.CalculateField(in_table= area_intersected_feature_class,
                                        field='Area',
                                        expression='round(!Area!, 3)',
                                        field_type="FLOAT")

        area_intersected_feature_class = os.path.join(self.storage_dataset, f'{self.formatted_feature_class}_area')
        return area_intersected_feature_class