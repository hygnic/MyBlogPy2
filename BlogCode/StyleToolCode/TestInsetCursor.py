# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              TestInsetCursor
# Author:            Hygnic
# Created on:        2022/4/7 20:40
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import os
import numpy as np
import arcpy



arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True
arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace,
                                    out_name="inset.shp",
                                    geometry_type="POLYGON",
                                    spatial_reference=3857)


poly2 = [[10, 20], [30, 20], [40, 60], [10, 20]]
new1 = arcpy.Polygon(
    arcpy.Array([arcpy.Point(20.0, 20.0), arcpy.Point(30.0, 20.0),
                 arcpy.Point(30.0, 10.0), arcpy.Point(20.0, 10.0)]))

cursor = arcpy.da.InsertCursor("inset.shp", ['SHAPE@'])
cursor.insertRow([new1])
# cursor.insertRow([f])
