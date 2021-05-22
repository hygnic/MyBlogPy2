# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code1
# Author:            Hygnic
# Created on:        2021/5/21 9:43
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os

arcpy.env.workspace = os.getcwd()

# lyr_p = "../SHP/Boroughs.shp"
lyr_p = "G:/MoveOn/arcpyTutoraial/SHP/Boroughs.shp"
# lyr_p = "../NYC.gdb/Boroughs"

with arcpy.da.UpdateCursor(lyr_p, "SHAPE@") as cursor:
    for row in cursor:
        print row[0]
        

"""
import arcpy
import os

arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

lyr_p = "../SHP/Boroughs.shp"
arcpy.CopyFeatures_management(lyr_p, "out.shp")
"""