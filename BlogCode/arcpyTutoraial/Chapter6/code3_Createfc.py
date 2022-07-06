# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              Code1
# Author:            Hygnic
# Created on:        2021/8/31 20:09
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os

arcpy.env.overwriteOutput = True
wk = os.path.abspath("../SHP")
arcpy.env.workspace = wk

lyr = "../SHP/Boroughs.shp"
lyr_no_prj = "../SHP/Boroughs_no_prj.shp"


cf_m = arcpy.CreateFeatureclass_management

# 方法1
cf_m(wk, "blank", "Polygon", spatial_reference=2263)

# 方法2
sr = arcpy.SpatialReference(2263)
cf_m(wk, "blank", "Polygon", spatial_reference=sr)

# 方法3
prj_file = "../SHP/Boroughs.prj"
cf_m(wk, "blank", "Polygon", spatial_reference=prj_file)

# 方法4
sr_strings = arcpy.SpatialReference(2263).exportToString()
cf_m(wk, "blank", "Polygon", spatial_reference=sr_strings)

# 方法5
new_sr = arcpy.CreateSpatialReference_management(2263)
cf_m(wk, "blank", "Polygon", spatial_reference=new_sr)

# 方法6
cf_m(wk, "blank", "Polygon", spatial_reference=lyr)