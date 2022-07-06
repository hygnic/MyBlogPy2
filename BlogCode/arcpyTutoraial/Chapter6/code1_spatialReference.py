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
arcpy.env.workspace = os.path.abspath("../SHP")

lyr = "../SHP/Boroughs.shp"
lyr_no_prj = "../SHP/Boroughs_no_prj.shp"
raster_lyr = "../Raster/N31E107.tif"

sr = arcpy.Describe(lyr).spatialReference # 2263
sr_raster = arcpy.Describe(raster_lyr).spatialReference # 4326
sr_no_prj = arcpy.Describe(lyr_no_prj).spatialReference


new_create_sr = arcpy.SpatialReference(3857)
prj_file = "../SHP/Boroughs.prj"
new_create_sr1 = arcpy.SpatialReference(prj_file)
new_create_sr2 = arcpy.SpatialReference("Hawaii Albers Equal Area Conic")


print sr_no_prj.name

print sr_raster.factoryCode
print sr_raster.name
print sr_raster.type

print new_create_sr.factoryCode
print new_create_sr.name
print new_create_sr.type
