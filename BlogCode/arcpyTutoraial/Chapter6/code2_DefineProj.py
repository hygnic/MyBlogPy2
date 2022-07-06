# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              Code1
# Author:            Hygnic
# Created on:        2021/9/1 20:22
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
arcpy.env.workspace = os.path.abspath("../SHP")

lyr = "../SHP/Boroughs.shp"
lyr_no_prj = "../SHP/Boroughs_no_prj.shp"

# 方法1
sr = arcpy.SpatialReference(2263)
arcpy.DefineProjection_management(lyr_no_prj, sr)

# 方法2
arcpy.DefineProjection_management(lyr_no_prj, 2263)

# 方法3
prj_file = "../SHP/Boroughs.prj"
arcpy.DefineProjection_management(lyr_no_prj, prj_file)

# 方法4
sr_strings = arcpy.SpatialReference(2263).exportToString()
arcpy.DefineProjection_management(lyr_no_prj, sr_strings)

# 方法5
new_sr = arcpy.CreateSpatialReference_management(2263)
arcpy.DefineProjection_management(lyr_no_prj, new_sr)