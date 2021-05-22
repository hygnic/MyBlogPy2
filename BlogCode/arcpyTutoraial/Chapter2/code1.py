# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code1
# Author:            Hygnic
# Created on:        2021/5/12 11:10
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os

cws = os.getcwd()
# 设置工作空间
arcpy.env.workspace = cws
# 可以覆盖同名文件
arcpy.env.overwriteOutput = True
arcpy.CopyFeatures_management("../SHP/Boroughs.shp", "out.shp")

raster_p = "../Raster/N31E107.tif"
new_raster = arcpy.sa.Slope(raster_p)
new_raster.save("../NYC.gdb/qw")